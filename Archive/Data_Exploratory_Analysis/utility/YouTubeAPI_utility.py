from apiclient.discovery import build
import pandas as pd


def getDurationDf(video_ids):
    api_path = 'api_key.txt'
    with open(api_path, 'r') as file:
        api_key = file.readline()

    youtube = build('youtube','v3',developerKey = api_key)
    print(type(youtube))

    request = youtube.videos().list(part='contentDetails',id=video_ids)
    print(type(request))

    res = request.execute()
    items = res['items']
    id_list=[]
    duration_list=[]
    for video in items:
        video_id = video['id']
        duration = video['contentDetails']['duration']
        id_list.append(video_id)
        duration_list.append(duration)
    df = pd.DataFrame(
    {'video_id': id_list,
     'duration': duration_list,
    })
    return df

def getCategoryDf(regionCode='US'):
    api_path = 'api_key.txt'
    with open(api_path, 'r') as file:
        api_key = file.readline()

    youtube = build('youtube','v3',developerKey = api_key)
    print(type(youtube))

    request = youtube.videoCategories().list(part='snippet',regionCode='US')
    print(type(request))

    res = request.execute()
    items = res['items']
    id_list=[]
    name_list=[]
    for category in items:
        catergory_id = category['id']
        category_name = category['snippet']['title']
        id_list.append(catergory_id)
        name_list.append(category_name)
    df = pd.DataFrame(
    {'catergory_id': id_list,
     'category_name': name_list,
    })
    return df

    