import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import re
from API import YouTubeAPI_utility as api
import Download_Data as dd
import uploadYoutubeData as upload
import Preprocess_EDA as eda
import pytz
from datetime import datetime, timedelta



def getWeekdayTxt(date):
    
    weekday=""
    if date.isoweekday()== 1:
        weekday = "Monday"
    elif date.isoweekday()== 2:
        weekday = "Tuesday"    
    elif date.isoweekday()== 3:
        weekday = "Wednesday"
    elif date.isoweekday()== 4:
        weekday = "Thursday"
    elif date.isoweekday()== 5:
        weekday = "Friday"
    elif date.isoweekday()== 6:
        weekday = "Saturday"
    elif date.isoweekday()== 7:
        weekday = "Sunday"
    
    return weekday

def find_number(text):
    
    num = re.findall(r'[0-9]+',text)
    
    return "".join(num)

def changeTimeZone(country, time):
    timezone = pytz.timezone("UTC")
    time = timezone.localize(time)
    output_time = None 
    if country == 'US' :
        eastern_timezone = pytz.timezone("US/Pacific")
        output_time = time.astimezone(eastern_timezone)
    return output_time


def analysis():
    #dd.downloadData()
    df = eda.integrate_clean_data()
    if 'tags' in df.columns:
        df = df.drop(['tags'], axis=1)
    #Analysis from trending date >= 2021-01-01
    df['trending_date'] = df['trending_date'].apply(lambda x: find_number(x))
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%Y%m%d%H%M%S')
    df = df[(df['trending_date']>='2021-01-01')]
    df = df.sort_values(by=['trending_date'], ascending=True)
    df['published_weekday'] = df['publishDate'].apply(lambda x: getWeekdayTxt(x))
    df['published_hour'] = pd.to_datetime(df['publishTime'], format='%H:%M:%S').dt.strftime('%I %p')
    df['publishDate'] = pd.to_datetime(df['publishDate']) 
    df["published_weekday_hour"] = df["published_weekday"].astype(str)+ " " + df["published_hour"].astype(str)
    df['day_for_publish_to_trendning'] = df['trending_date'] - df['publishDate']
    df.to_csv(r'Tableau_Workbook/data/publishedAt_EDA.csv')


    df_unique_id = df.drop_duplicates(subset=['video_id', 'country'], keep='first')
    df_unique_id.to_csv(r'Tableau_Workbook/data/publishedAt_unique_EDA.csv')

    #publish day of week related on trending videos list
    weekday_df =  df_unique_id[['video_id','published_weekday','country']].groupby(['country','published_weekday'], as_index=False).count()
    weekday_df['published_weekday']=pd.Categorical(weekday_df['published_weekday'], ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"])
    weekday_df = weekday_df.sort_values('published_weekday')
    #weekday_trending_graph = weekday_df.plot.bar(x='published_weekday', y='video_id', figsize=(15,5), title='Number Of Trending Video Published Day of Week', alpha=0.5)    

    #publish hour  related on trending videos list
    hour_df =  df_unique_id[['video_id','published_hour','country']].groupby(['country','published_hour'], as_index=False).count()
    hour_df['published_hour']=pd.Categorical(hour_df['published_hour'], ["12 AM", "01 AM", "02 AM","03 AM","04 AM","05 AM","06 AM","07 AM","08 AM","09 AM","10 AM","11 AM",
                                                                                "12 PM", "01 PM", "02 PM","03 PM","04 PM","05 PM","06 PM","07 PM","08 PM","09 PM","10 PM","11 PM"])
    hour_df = hour_df.sort_values('published_hour')
    #hour_trending_graph = hour_df.plot.bar(x='published_hour', y='video_id', figsize=(15,5), title='Number Of Trending Video Published Hour', alpha=0.5)      

    #publish day of week and hour related on trending videos list
    weekday_hour_df = df_unique_id[['video_id','published_weekday','published_hour','country']].groupby(['country','published_weekday','published_hour'], as_index=False).count()
    weekday_hour_df['published_weekday']=pd.Categorical(weekday_hour_df['published_weekday'], ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"])
    weekday_hour_df['published_hour']=pd.Categorical(weekday_hour_df['published_hour'], ["12 AM", "01 AM", "02 AM","03 AM","04 AM","05 AM","06 AM","07 AM","08 AM","09 AM","10 AM","11 AM",
                                                                                                    "12 PM", "01 PM", "02 PM","03 PM","04 PM","05 PM","06 PM","07 PM","08 PM","09 PM","10 PM","11 PM"])
    weekday_hour_df = weekday_hour_df.sort_values(['published_weekday','published_hour'])
    weekday_hour_df["published_weekday_hour"] = weekday_hour_df["published_weekday"].astype(str)+ " " + weekday_hour_df["published_hour"].astype(str)
    #weekday_hour_trending_graph = weekday_hour_df.plot.bar(x='published_weekday_hour', y='video_id', figsize=(40,10), title='Number Of Trending Video Published Weekday & Hour', alpha=0.5)  
    weekday_hour_df.to_csv(r'Tableau_Workbook/data/weekday_hour_df.csv')

    #top 10 publish day of week and hour related on trending videos list
    weekday_hour_df = weekday_hour_df.sort_values('video_id', ascending=False)
    top_10_weekday_hour_df = weekday_hour_df.head(10)
    #top_10_weekday_hour_trending_graph = top_10_weekday_hour_df.plot.bar(x='published_weekday_hour', y='video_id', figsize=(15,5), title='Top 10 Published Weekday & Hour of Trending Videos', alpha=0.5)  

    weekday_hour_df = weekday_hour_df.sort_values(['published_weekday','published_hour'])

    df_unique_id['published_weekday']=pd.Categorical(df_unique_id['published_weekday'], ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"])
    df_unique_id['published_hour']=pd.Categorical(df_unique_id['published_hour'], ["12 AM", "01 AM", "02 AM","03 AM","04 AM","05 AM","06 AM","07 AM","08 AM","09 AM","10 AM","11 AM",
                                                                                                    "12 PM", "01 PM", "02 PM","03 PM","04 PM","05 PM","06 PM","07 PM","08 PM","09 PM","10 PM","11 PM"])
    df_unique_id = df_unique_id.sort_values(['published_weekday','published_hour'])
    df_unique_id["published_weekday_hour"] = df_unique_id["published_weekday"].astype(str)+ " " + df_unique_id["published_hour"].astype(str)

    
    #correlation break 3 countries and combine
    us_corr_df = getCorrMatrix('US', df_unique_id)
    gb_corr_df = getCorrMatrix('GB', df_unique_id)
    ca_corr_df = getCorrMatrix('CA', df_unique_id)

    corr_df = pd.concat([us_corr_df, gb_corr_df, ca_corr_df])
    corr_df = corr_df.reset_index(drop=True)


    publishedAt_us_corr_df = getCorrDf('US', df_unique_id, weekday_hour_df)
    publishedAt_gb_corr_df = getCorrDf('GB', df_unique_id, weekday_hour_df)
    publishedAt_ca_corr_df = getCorrDf('CA', df_unique_id, weekday_hour_df)

    publishedAt_corr_df = pd.concat([publishedAt_us_corr_df, publishedAt_gb_corr_df, publishedAt_ca_corr_df])
    publishedAt_corr_df = publishedAt_corr_df.reset_index(inplace=False)
    """
    view_corr = df_unique_id['published_weekday_hour'].str.get_dummies().corrwith(df_unique_id['view_count']/df_unique_id['view_count'].max())
    view_corr_df = pd.DataFrame(view_corr, columns=['view_corr'])
    view_corr_df = view_corr_df.reset_index()
    view_corr_df = view_corr_df.rename(columns={"index": "published_weekday_hour"})
    #display(view_corr_df)


    like_corr = df_unique_id['published_weekday_hour'].str.get_dummies().corrwith(df_unique_id['likes']/df_unique_id['likes'].max())
    like_corr_df = pd.DataFrame(like_corr, columns=['like_corr'])
    like_corr_df = like_corr_df.reset_index()
    like_corr_df = like_corr_df.rename(columns={"index": "published_weekday_hour"})
    #display(like_corr_df)
    

    publishedAt_corr_df = weekday_hour_df.merge(view_corr_df, how = 'inner', on = ['published_weekday_hour'])
    publishedAt_corr_df = publishedAt_corr_df.merge(like_corr_df, how = 'inner', on = ['published_weekday_hour'])
    #display(publishedAt_corr_df)
    """
    corr_df.to_csv(r'Tableau_Workbook/data/corr_df.csv')
    publishedAt_corr_df.to_csv(r'Tableau_Workbook/data/publishedAt_corr_df.csv')
    
    upload.uploadDataToDrive("tableau")

def getCorrDf(country, df, df_merge):
    
    country_df = df.loc[df['country']==country]
    country_df_merge = df_merge.loc[df_merge['country']==country]

    view_corr = country_df['published_weekday_hour'].str.get_dummies().corrwith(country_df['view_count']/country_df['view_count'].max())
    view_corr_df = pd.DataFrame(view_corr, columns=['view_corr'])
    view_corr_df = view_corr_df.reset_index()
    view_corr_df = view_corr_df.rename(columns={"index": "published_weekday_hour"})


    like_corr = country_df['published_weekday_hour'].str.get_dummies().corrwith(country_df['likes']/country_df['likes'].max())
    like_corr_df = pd.DataFrame(like_corr, columns=['like_corr'])
    like_corr_df = like_corr_df.reset_index()
    like_corr_df = like_corr_df.rename(columns={"index": "published_weekday_hour"})

    corr_df = country_df_merge.merge(view_corr_df, how = 'inner', on = ['published_weekday_hour'])
    result_df = corr_df.merge(like_corr_df, how = 'inner', on = ['published_weekday_hour'])
    
    return result_df


def getCorrMatrix(country, df):
    country_df = df.loc[df['country']==country]
    country_df = country_df[['likes','view_count','comment_count']]
    df_corr = country_df.corr(method ='pearson')
    result_df = df_corr.stack().reset_index()
    result_df.columns = ['correlation_factor1','correlation_factor2','correlation']
    result_df['country'] = country
    result_df = result_df.reset_index(drop=True)
    return result_df

analysis()