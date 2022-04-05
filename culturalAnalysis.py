import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import re
from API import YouTubeAPI_utility as api
import uploadYoutubeData as upload
import Preprocess_EDA as eda
import pytz
from datetime import datetime, timedelta
import countryAnalysis as text


def analysis():
    df = eda.integrate_clean_data()
    if 'tags' in df.columns:
        df = df.drop(['tags'], axis=1)
    df_unique_id_by_country = df.drop_duplicates(subset=['video_id', 'country'], keep='first')
    df_unique_id = df.drop_duplicates(subset=['video_id'], keep='first')
    for index, row in df_unique_id.iterrows():
       df_temp = df_unique_id_by_country[(df_unique_id_by_country['video_id']==row['video_id'])]
       country_list = str(df_temp['country'].tolist())
       df_unique_id.at[index,'trending_country_list'] = country_list
    print(df_unique_id.head(10))
    # only on one country
    df_one_country = df_unique_id[(df_unique_id['trending_country_list']=="['US']") | (df_unique_id['trending_country_list']=="['CA']") | (df_unique_id['trending_country_list']=="['GB']")]
    df_one_country.to_csv(r'Tableau_Workbook/data/trending_one_country.csv')

    # all country
    df_all_country = df_unique_id[(df_unique_id['trending_country_list']=="['US', 'CA', 'GB']")]
    df_all_country.to_csv(r'Tableau_Workbook/data/trending_all_country.csv')

    #all country tags and titles
    text.title_tags(df_all_country, w='all_country')
    text.prepare_title_data_Tableau(csv_name='title_tags_all_country_df', tableau_df_name='all_country_title_df')
    text.prepare_tag_data_Tableau(csv_name='title_tags_all_country_df', tableau_df_name='all_country_tags_df')

    # similar country
    df_similar_country = df_unique_id[(df_unique_id['trending_country_list']=="['US', 'CA']")]
    df_similar_country.to_csv(r'Tableau_Workbook/data/trending_similar_country.csv')
    text.title_tags(df_similar_country, w='similar_country')
    text.prepare_title_data_Tableau(csv_name='title_tags_similar_country_df', tableau_df_name='similar_country_title_df')
    text.prepare_tag_data_Tableau(csv_name='title_tags_similar_country_df', tableau_df_name='similar_country_tags_df')

    # different country
    df_diff_country = df_unique_id[(df_unique_id['trending_country_list']=="['US', 'GB']") | (df_unique_id['trending_country_list']=="['CA', 'GB']")]
    df_diff_country.to_csv(r'Tableau_Workbook/data/trending_different_country.csv')
    df_US_GB_country = df_unique_id[(df_unique_id['trending_country_list']=="['US', 'GB']")]
    text.title_tags(df_US_GB_country, w='us_gb_country')
    text.prepare_title_data_Tableau(csv_name='title_tags_us_gb_country_df', tableau_df_name='us_gb_country_title_df')
    text.prepare_tag_data_Tableau(csv_name='title_tags_us_gb_country_df', tableau_df_name='us_gb_country_tags_df')
    df_CA_GB_country = df_unique_id[(df_unique_id['trending_country_list']=="['CA', 'GB']")]
    text.title_tags(df_CA_GB_country, w='ca_gb_country')
    text.prepare_title_data_Tableau(csv_name='title_tags_ca_gb_country_df', tableau_df_name='ca_gb_country_title_df')
    text.prepare_tag_data_Tableau(csv_name='title_tags_ca_gb_country_df', tableau_df_name='ca_gb_country_tags_df')

    upload.uploadDataToDrive("tableau")

analysis()

