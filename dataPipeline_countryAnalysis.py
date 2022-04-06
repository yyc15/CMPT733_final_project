from API import getYoutubeTrendingVideo as api
import uploadYoutubeData as upload
from countryAnalysis import * 

# print('---------------------------------------------------------------')
# print("getting api data...")
# api.get_data()
# print("api data downloaded.")

# print("uploading api data to drive...")
# upload.uploadDataToDrive("api")
# print("api data uploaded.\n")

print('---------------------------------------------------------------')
print('Data analysing...')
analysis()
print('Data analysis completed.')

# upload.uploadDataToDrive('tableau')