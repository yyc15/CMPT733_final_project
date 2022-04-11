import Download_Data as dd
import Preprocess_EDA as eda
import uploadYoutubeData as upload
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import math
from nltk.tokenize import word_tokenize
import string
import emoji
from emoji import UNICODE_EMOJI
import functools
import operator
import nltk
nltk.download('omw-1.4')
# uncomment for Jupyter notebook
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"
# from IPython.display import display


def cat_df(df1, cat_cols = ['category', 'country', 'view_count', 'dislikes', 'likes', 'comment_count'] ):

    df_cat = df1[cat_cols]  # specify "cat_cols" if needed
    df_cat1 = df_cat.melt(id_vars=['country', 'category'], value_vars=['view_count', 'dislikes', 'likes', 'comment_count'], var_name='metrics', value_name='value')
    df_cat1.to_csv(r'Tableau_Workbook/data/category_metrics_corr_df.csv') 
    # upload.uploadDataToDrive('tableau')


lemma = nltk.wordnet.WordNetLemmatizer()

def get_terms(t):
    
    stop_words = set(stopwords.words('english'))
    ###addded###
    add_stp = ['com', 'www', 'http', 'video', 'short', 'de', 'youtube', 'tiktok']
    for w in add_stp:
        stop_words.add(w)
    ###----###
    #porter = PorterStemmer()
    words = []

    if not isinstance(t, list) and math.isnan(t):
        return None
    
    for i in t:
        terms = word_tokenize(i)
        for j in terms:
            # remove punctuation
            j = j.translate(str.maketrans('', '', string.punctuation))   
            # split multiple consecutive emoji
            split_j = emoji.get_emoji_regexp().split(j)
            split_whitespace = [substr.split() for substr in split_j]
            j_split = functools.reduce(operator.concat, split_whitespace)
            for item in j_split:
                item = item.lower()
                if item != '' and len(item) > 1 and item not in stop_words:
                    # deal with emoji
                    if item in UNICODE_EMOJI['en']:
                        words.append('emoji_symbol')
                    else:
                        #stemming
                        #stemmed_i = porter.stem(item)
                        #lemmatization
                        stemmed_i = lemma.lemmatize(item)
                        words.append(stemmed_i)  # now words is a list
    return words


def title_tags(dataframe, w = 'all', tag_cols = ['country', 'tags_lst', 'title_lst']):

    # tag_cols = ['country', 'tags_lst', 'title_lst']  # specify columns for tags if needed
    tags_df = dataframe[tag_cols]
    tags_df['tags_lst_processed'] = tags_df['tags_lst'].apply(lambda x: get_terms(x))
    tags_df['title_lst_processed'] = tags_df['title_lst'].apply(lambda x: get_terms(x))
    
    tags_df.to_csv(f'Tableau_Workbook/data/title_tags_{w}_df.csv') 
    # upload.uploadDataToDrive('tableau')
    return tags_df


def get_df_by_country(df1, c):
    df_country = df1.loc[df1['country'] == c]
    return df_country


def convert_lst(sublist):
    
    sublist0 = sublist.lstrip('[\'').rstrip('\']')
    sublist1 = sublist0.split('\', \'')
    return sublist1


def prepare_title_data_Tableau(country, csv_name, tableau_df_name):
    df_country = pd.read_csv(f'./Tableau_Workbook/data/{csv_name}.csv')
    df_country['title_lst_processed'] = df_country['title_lst_processed'].apply(lambda x: convert_lst(x))
    country_titles = pd.value_counts(np.hstack(df_country['title_lst_processed'].dropna()))
    country_title_freq = pd.DataFrame({f'{country}_title_words':country_titles.index, 'counts': country_titles.values})
    country_title_freq.to_csv(f'Tableau_Workbook/data/{tableau_df_name}.csv')
    # upload.uploadDataToDrive('tableau')


def prepare_tag_data_Tableau(country, csv_name, tableau_df_name):
    df_country = pd.read_csv(f'./Tableau_Workbook/data/{csv_name}.csv')
    df_country['tags_lst_processed'] = df_country['tags_lst_processed'].dropna().apply(lambda x: convert_lst(x))
    country_tags = pd.value_counts(np.hstack(df_country['tags_lst_processed'].dropna()))
    country_tags_freq = pd.DataFrame({f'{country}_tag_words':country_tags.index, 'counts': country_tags.values})
    country_tags_freq.to_csv(f'Tableau_Workbook/data/{tableau_df_name}.csv') 
    # upload.uploadDataToDrive('tableau')


def analysis():
    ## Download up-to-date data from Youtube api
    # dd.downloadData()
    df = eda.integrate_clean_data()
    df1 = df

    ## Get csv file for category/country analysis
    cat_df(df1)

    ## Get title, tags csv for each country
    df_us = get_df_by_country(df1, 'US')
    df_ca = get_df_by_country(df1, 'CA')
    df_gb = get_df_by_country(df1, 'GB')
    title_tags(df_us, w='us')
    title_tags(df_ca, w='ca')
    title_tags(df_gb, w='gb')

    prepare_title_data_Tableau('US', csv_name='title_tags_us_df', tableau_df_name='US_title_df')
    prepare_title_data_Tableau('CA', csv_name='title_tags_ca_df', tableau_df_name='CA_title_df')
    prepare_title_data_Tableau('GB', csv_name='title_tags_gb_df', tableau_df_name='GB_title_df')

    prepare_tag_data_Tableau('US', csv_name='title_tags_us_df', tableau_df_name='US_tags_df')
    prepare_tag_data_Tableau('CA', csv_name='title_tags_ca_df', tableau_df_name='CA_tags_df')
    prepare_tag_data_Tableau('GB', csv_name='title_tags_gb_df', tableau_df_name='GB_tags_df')

    upload.uploadDataToDrive('tableau')

analysis()