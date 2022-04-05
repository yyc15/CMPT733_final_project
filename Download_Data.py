import os
import requests
import os.path
from os import path
import json


def download_file(url, filename):
    print('Downloading', filename ,'...')
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response:
                file.write(chunk)
            
def downloadData():

    downloadType("data/")
    downloadType("Tableau_Workbook/data/")
    
    print('Files Download completed')


def downloadType(folderLocation):
    with open(folderLocation + 'fileList/fileDict.json') as json_file:
        csvDataDict = json.load(json_file)
    
    if path.isdir(folderLocation) == False:
        os.mkdir(folderLocation)

    for fileName, fileId in csvDataDict.items():
        url = 'https://drive.google.com/u/2/uc?id='+fileId+'&export=download&confirm=t'
        location = folderLocation + fileName
        download_file(url, location)

