import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud, STOPWORDS
import seaborn as sns
import Preprocess_EDA as eda

df7 = pd.read_csv('US_youtube_trending_data.csv')
df7.description= df7.description.fillna('No description provided') 
tags0=''.join(df7.tags)
tags1= re.sub('[^a-zA-Z]', ' ', tags0)
tags1= re.sub(' +', ' ', tags1)
x,y = np.ogrid[:3000,:3000]
mask = (x-1500) ** 2 + (y-1500) ** 2 > 1300 ** 2
mask = 255 * mask.astype(int)
wordcloud= WordCloud(background_color='white', mask=mask, stopwords= set(STOPWORDS)).generate(tags1)
plt.figure(figsize=(15,5))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

df_corr= df7[['likes', 'dislikes', 'comment_count', 'view_count']]
print(df_corr.corr())
sns.heatmap(df_corr.corr(), annot= True, cmap='YlGnBu' )
plt.show()

df = eda.integrate_clean_data()
us_df = df[(df['country']=='US')]
gb_df = df[(df['country']=='GB')]
us_df_unique_id = us_df.drop_duplicates(subset=['video_id'], keep='first')
gb_df_unique_id = gb_df.drop_duplicates(subset=['video_id'], keep='first')
pd.set_option('max_columns', None)
df_cat = gb_df_unique_id.groupby('category').count()
df_cat = df_cat.sort_values(by=['view_count'], ascending=False)
plot = df_cat.plot.pie(y='likes', figsize=(10, 10))
plt.show()
plot2 = df_cat.plot.pie(subplots=True, y='view_count', figsize=(10, 10))
plt.show()