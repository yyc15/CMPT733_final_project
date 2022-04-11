# YouTube Trending Video Analysis
What are the elements to be listed on the YouTube trending video list so that the videos can reach as many audiences as possible with higher numbers of views, likes, and comments?

The data analysis dashboard and online product will try to answer the question with the latest years trending video information.

### 1. YouTube dataset API
The dataset is updated on demand. Currently the result is from 2021/01/01 to 2022/04/06. 
Check the folder data for the original dataset. 

getYoutubeTrendingVideo.py : Main program for dragging youtube trending list data

dataPipeline.py : Combine with getYoutubeTrendingVideo.py to get api data and combine the eixting data and upload to google drive

Google.py : Google drive setting

Download_Data.py : Download data from google drive


### 2. Exploratory Data Analysis
#### Before feeding into Tableau:


Preprocess_EDA.py :  Process data

publishDatetimeAnalysis.py :  Main program for analysis of publish date time 

contryAnalysis.py : Main program for analysis of category, tags and titles

culturalAnalysis.py : Main program for analysis of common elements

uploadYoutubeData.py : Upload data function


Tableau workbook contains the detailed analysis based on countries and categories. The ready-to-view dashboard is embeded here: https://yt-trending-video-analysis.herokuapp.com/

### 3. Machine Learning
Modeling_Clustering_numbers.py: Hierarchical clustering method with numberical & categorical variables to subset the categories. 
Modeling_Clustering_text.py: KMeans clustering method with text mining for a deeper dive of each category. 


### 4. How to run the Data Product
Go to our [web page](https://yt-trending-video-analysis.herokuapp.com/) for a tour of your category of interest. There are also hot videos to view for insparition. 

In order to run the web application on the local computers:
 * Go to ‘Web’ folder.
 * Double Click on the index.html.


### Credits:
[Wanyi Su](https://www.linkedin.com/in/wanyisu/)

[Wei (Joann) Zhang](https://www.linkedin.com/in/joannzhang1818/)

[Yin Yu Kevani Chow](linkedin.com/in/kevanichow/)

[Zeyu Hu](https://www.linkedin.com/in/zeyu-hu-64322395/)

[Jinyao (Timmy) Lu](https://www.linkedin.com/in/timmyluuu/)
