import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import datetime
# %matplotlib inline # uncomment for Jupyter
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)


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


# combine the US & GB datasets
def integrate_clean_data():
    us = pd.read_csv('../data/US_youtube_trending_data.csv')
    us['country'] = 'US'
    uscat = extract_catid_js('../data/US_category_id.json')
    us_merge = merge_cat(us, uscat)

    gb = pd.read_csv('../data/GB_youtube_trending_data.csv')
    gb['country'] = 'GB'
    #     gbcat = extract_catid_js('GB_category_id.json') # data deficiency
    gb_merge = merge_cat(gb, uscat)

    # merge two countries
    df_list = [us_merge, gb_merge]
    df = pd.concat(df_list).reset_index(drop=True)

    # create date and time features
    df['publishDate'] = pd.to_datetime(df['publishedAt']).dt.date
    df['publishTime'] = pd.to_datetime(df['publishedAt']).dt.time
    df['trendingDate'] = pd.to_datetime(df['trending_date']).dt.date  # there was no trending time

    # subset data from 2021-01-01
    df = df.loc[pd.to_datetime(df['trendingDate']) >= '2021-01-01',]

    # title & tags
    df.replace(to_replace=['[None]'], value=np.nan, inplace=True)
    df['title_lst'] = df['title'].str.strip(' *#\'\",$@!\n\t').str.split(pat="|")
    df['tags_lst'] = df['tags'].str.strip(' *#\'\",$@!\n\t').str.split(pat="|")

    # drop meaningless columns
    df1 = df.drop(['channelId', 'thumbnail_link'], axis='columns')

    return df1

# process with he youtube trending data (since the saved csv file distorts result)
df = integrate_clean_data()
print(df.head(3))
