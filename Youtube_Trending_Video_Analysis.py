import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import re
from API import YouTubeAPI_utility as api
import Preprocess_EDA as eda
import pytz
from datetime import datetime, timedelta

df = eda.integrate_clean_data()

us_df = df[(df['country']=='US')]
gb_df = df[(df['country']=='GB')]


us_df_unique_id = us_df.drop_duplicates(subset=['video_id'], keep='first')
gb_df_unique_id = gb_df.drop_duplicates(subset=['video_id'], keep='first')

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

#Analysis from trending date >= 2021-01-01
us_df_unique_id['trending_date'] = us_df_unique_id['trending_date'].apply(lambda x: find_number(x))
us_df_unique_id['trending_date'] = pd.to_datetime(us_df_unique_id['trending_date'], format='%Y%m%d%H%M%S')
us_df_unique_id = us_df_unique_id[(us_df_unique_id['trending_date']>='2021-01-01')]
us_df_unique_id = us_df_unique_id.sort_values(by=['trending_date'], ascending=True)
us_df_unique_id['published_datetime'] = us_df_unique_id['publishedAt'].apply(lambda x: find_number(x))
us_df_unique_id['published_datetime'] = us_df_unique_id['published_datetime'].str.slice(0, 8) + us_df_unique_id['published_datetime'].str.slice(8, 15)
us_df_unique_id['published_datetime'] = pd.to_datetime(us_df_unique_id['published_datetime'], format='%Y%m%d%H%M%S')
us_df_unique_id['published_datetime'] = us_df_unique_id['published_datetime'].apply(lambda x: changeTimeZone('US',x))
us_df_unique_id['publishDate'] = pd.to_datetime(us_df_unique_id['published_datetime']).dt.date
us_df_unique_id['publishTime'] = pd.to_datetime(us_df_unique_id['published_datetime']).dt.time
us_df_unique_id['published_weekday'] = us_df_unique_id['publishDate'].apply(lambda x: getWeekdayTxt(x))
us_df_unique_id['published_hour'] = pd.to_datetime(us_df_unique_id['publishTime'], format='%H:%M:%S').dt.strftime('%I %p')

#us_df_check = us_df_unique_id[['publishedAt','published_datetime','publishTime','published_weekday','published_hour']]
#print(us_df_check.head(2))

#publish day of week related on trending videos list
weekday_us_df =  us_df_unique_id[['video_id','published_weekday']].groupby('published_weekday', as_index=False).count()
weekday_us_df['published_weekday']=pd.Categorical(weekday_us_df['published_weekday'], ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"])
weekday_us_df = weekday_us_df.sort_values('published_weekday')
weekday_us_trending_graph = weekday_us_df.plot.bar(x='published_weekday', y='video_id', figsize=(15,5), title='Number Of Trending Video Published Day of Week', alpha=0.5)    

#publish hour  related on trending videos list
hour_us_df =  us_df_unique_id[['video_id','published_hour']].groupby('published_hour', as_index=False).count()
hour_us_df['published_hour']=pd.Categorical(hour_us_df['published_hour'], ["12 AM", "01 AM", "02 AM","03 AM","04 AM","05 AM","06 AM","07 AM","08 AM","09 AM","10 AM","11 AM",
                                                                              "12 PM", "01 PM", "02 PM","03 PM","04 PM","05 PM","06 PM","07 PM","08 PM","09 PM","10 PM","11 PM"])
hour_us_df = hour_us_df.sort_values('published_hour')
hour_us_trending_graph = hour_us_df.plot.bar(x='published_hour', y='video_id', figsize=(15,5), title='Number Of Trending Video Published Hour', alpha=0.5)      

#publish day of week and hour related on trending videos list
weekday_hour_us_df = us_df_unique_id[['video_id','published_weekday','published_hour','view_count','likes']].groupby(['published_weekday','published_hour'], as_index=False).count()
weekday_hour_us_df['published_weekday']=pd.Categorical(weekday_hour_us_df['published_weekday'], ["Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday","Sunday"])
weekday_hour_us_df['published_hour']=pd.Categorical(weekday_hour_us_df['published_hour'], ["12 AM", "01 AM", "02 AM","03 AM","04 AM","05 AM","06 AM","07 AM","08 AM","09 AM","10 AM","11 AM",
                                                                                                 "12 PM", "01 PM", "02 PM","03 PM","04 PM","05 PM","06 PM","07 PM","08 PM","09 PM","10 PM","11 PM"])
weekday_hour_us_df = weekday_hour_us_df.sort_values(['published_weekday','published_hour'])
weekday_hour_us_df["published_weekday_hour"] = weekday_hour_us_df["published_weekday"].astype(str)+ " " + weekday_hour_us_df["published_hour"].astype(str)
weekday_hour_us_trending_graph = weekday_hour_us_df.plot.bar(x='published_weekday_hour', y='video_id', figsize=(40,10), title='Number Of Trending Video Published Weekday & Hour', alpha=0.5)  

#top 10 publish day of week and hour related on trending videos list
weekday_hour_us_df = weekday_hour_us_df.sort_values('video_id', ascending=False)
top_10_weekday_hour_us_df = weekday_hour_us_df.head(10)
top_10_weekday_hour_us_trending_graph = top_10_weekday_hour_us_df.plot.bar(x='published_weekday_hour', y='video_id', figsize=(15,5), title='Top 10 Published Weekday & Hour of Trending Videos', alpha=0.5)  

#plt.show() 


view_corr = weekday_hour_us_df.published_weekday_hour.str.get_dummies().corrwith(weekday_hour_us_df.view_count/weekday_hour_us_df.view_count.max())
print (view_corr)

likes_corr = weekday_hour_us_df.published_weekday_hour.str.get_dummies().corrwith(weekday_hour_us_df.likes/weekday_hour_us_df.likes.max())
print (likes_corr)