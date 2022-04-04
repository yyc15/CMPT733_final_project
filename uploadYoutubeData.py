from math import gcd
import os
import os.path
from os import path
import json
import pickle
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import gspread


CLIENT_SECRET_FILE ='OAuth/google_drive_client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']


def auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service, access_token, gc
    service = build('drive', 'v3', credentials=creds)
    access_token = creds.token
    gc = gspread.authorize(creds)

def uploadFile(dataType, filename, PARENTS, FILE_ID):

    if dataType == "api":
        filepath = os.path.join('data/',filename)

    elif dataType =="tableau":
        filepath = os.path.join('Tableau_Workbook/data/',filename)
    
    else:
        filepath = os.path.join('data/',filename)
    
    print("Uploading", filepath , "...")
    filesize = os.path.getsize(filepath)

    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    
    if FILE_ID =="":
        params = {
            "name": filename,
            "mimeType": "text/csv",
            "parents": PARENTS
        }   
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
            headers=headers,
            data=json.dumps(params)
        )
    else:
        params = {
            "name": filename,
            "mimeType": "text/csv",
        }
        r = requests.patch(
            "https://www.googleapis.com/upload/drive/v3/files/"+FILE_ID+"?uploadType=resumable",
            headers=headers,
            data=json.dumps(params)
        )
    #print(r)

    location = r.headers['Location']

    headers = {"Content-Range": "bytes 0-" + str(filesize - 1) + "/" + str(filesize)}
    r = requests.put(
        location,
        headers=headers,
        data=open(filepath, 'rb')
    )
    print(r.text)
    print(filename, "is uploaded")


    

def getDriveFile(N, PARENTS):

    resource = service.files()
    result = resource.list(
                q="'" + PARENTS[0] + "' in parents",
                pageSize=N, 
                fields="files(id, name)",
            ).execute()
    
    return result


def uploadDataToDrive(dataType):
    auth()

    if dataType == "api":
        file_path = 'data/'
        PARENTS = ['1RQmzkSvg_2lg9aVeKgRjItwskjK2O8if'] # the folder for the files to upload

    elif dataType =="tableau":
        file_path = 'Tableau_Workbook/data/'
        PARENTS = ['1rP76HfShVhHARWH8lXcQFDeFPpQEc5Mm'] # the folder for the files to upload
    
    else:
        file_path = 'data/'
        PARENTS = ['1RQmzkSvg_2lg9aVeKgRjItwskjK2O8if'] # the folder for the files to upload
    
    csv_files = os.listdir(file_path)
    result_dict = getDriveFile(50, PARENTS)
    file_list = result_dict.get('files')
    print("The files in local data folder", csv_files)

    if len(file_list)>0:
        print("The files in google drive folder", file_list)
        print("Update files in google drive folder...")
        
        fileIdlist = []
        for file in file_list:
            fileIdlist.append(file['id'])

        for file in file_list:
            if file['name'] != '.DS_Store':
                """
                media = MediaFileUpload(filename=file_path + file['name'] , mimetype='text/csv')
        
                response = service.files().update(
                    fileId = file['id'],
                    media_body = media
                ).execute()
                
                """
                fileId=file['id']
                filename = file['name']
                print("fileId:", fileId)
                uploadFile(dataType ,filename, PARENTS, FILE_ID=fileId)
        print("Files are updated.")
    else:
        for csv_file in csv_files:
            if csv_file != '.DS_Store' and csv_file !='today_data' and csv_file !='fileList':
                uploadFile(dataType ,csv_file, PARENTS, FILE_ID="")
    
    fretchFileList()

def fretchFileList():
    auth()
    print('Fretching data list from drive...')
    writeFileListJson(['1RQmzkSvg_2lg9aVeKgRjItwskjK2O8if'], "data/fileList")
    writeFileListJson(['1rP76HfShVhHARWH8lXcQFDeFPpQEc5Mm'], "Tableau_Workbook/data/fileList")
    print('Fretching data completed.')

def writeFileListJson(driveFolderId, folderLocation):
    result = getDriveFile(50, driveFolderId)
    fileList = result.get('files')
    filedict = {}
    for file in fileList:
        fileId=file['id']
        filename = file['name']
        filedict[filename] = fileId

    if path.isdir(folderLocation) == False:
            os.mkdir(folderLocation)

    with open(folderLocation + "/fileDict.json", "w") as outfile:
        json.dump(filedict, outfile)



# available functions:
# fretchFileList()
# uploadDataToDrive("tableau")
# uploadDataToDrive("api")
