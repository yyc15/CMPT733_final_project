from Download_Data import *
downloadData()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import pytz
import os
# %matplotlib inline # uncomment for Jupyter

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 50)
pd.set_option('display.max_colwidth', 50)

# extract category and corresponding id out of json file
def extract_catid_js(jsfile):
    with open(jsfile,'r') as f:
        cat = json.loads(f.read())
    df = pd.json_normalize(cat, record_path='items')
    df = df.rename(columns={"snippet.title": "category",
                           'id': 'categoryId'})
    outdf = df[['categoryId', 'category']].drop_duplicates()
    return outdf

# merge category data into main dataset
def merge_cat(maindf, catdf):
    maindf['categoryId'] = maindf['categoryId'].astype(int)
    catdf['categoryId'] = catdf['categoryId'].astype(int)
    df = maindf.merge(catdf, how = 'left', on = 'categoryId')
    return df

# read the data of a specific country, add country column, join the category and return a df
def read_merge(filename, country):
    df = pd.read_csv(os.path.join('data', filename))
    # drop meaningless columns
    df1 = df.drop(['channelId', 'thumbnail_link'], axis = 'columns')
    # add country column
    df1['country'] = country
    # merge with cat id
    cat = extract_catid_js('data/US_category_id.json')
    merge_df = merge_cat(df1, cat)
    return merge_df

# convert UTC (+00:00) Time zone to eastern time zone (considering Day Light Saving)
def changeTimeZone(time):
    utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    timezone = pytz.timezone("UTC")
    utc = timezone.localize(utc)
    eastern_timezone = pytz.timezone("US/Eastern")
    output_time = utc.astimezone(eastern_timezone)
    return output_time

# combine & clean the US & CA & GB datasets
def integrate_clean_data():
    # read US data
    us = read_merge('US_youtube_trending_data.csv', 'US')
    # convert UTC (+00:00) Time zone to eastern time zone for US & CA
    us['publishedAt'] = us['publishedAt'].apply(changeTimeZone)

    # read CA data
    ca = read_merge('CA_youtube_trending_data.csv', 'CA')
    # convert UTC (+00:00) Time zone to eastern time zone for US & CA
    ca['publishedAt'] = ca['publishedAt'].apply(changeTimeZone)

    # read GB data
    gb = read_merge('GB_youtube_trending_data.csv', 'GB')
    # no time zone conversion for Great Britain
    gb['publishedAt'] = gb['publishedAt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))

    # merge two countries
    df_list = [us, ca, gb]
    df = pd.concat(df_list).reset_index(drop=True)

    # create date and time features
    df['publishDate'] = df['publishedAt'].apply(lambda x: x.date())
    df['publishTime'] = df['publishedAt'].apply(lambda x: x.time())
    df['trendingDate'] = pd.to_datetime(df['trending_date']).dt.date  # there was no trending time

    # subset data from 2021-01-01
    df = df.loc[pd.to_datetime(df['trendingDate']) >= '2021-01-01',]

    # title & tags
    df.replace(to_replace=['[None]'], value=np.nan, inplace=True)
    df['title_lst'] = df['title'].str.strip(' *#\'\",$@!\n\t').str.split(pat="|")
    df['tags_lst'] = df['tags'].str.strip(' *#\'\",$@!\n\t').str.split(pat="|")

    return df
