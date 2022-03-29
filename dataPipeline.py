from API import getYoutubeTrendingVideo as api
import uploadYoutubeData as upload
import publishDatetimeAnalysis as publishDatetime

print("getting api data...")
api.get_data()
print("api data downloaded.")

print("uploading api data to drive...")
upload.uploadDataToDrive("api")
print("api data uploaded.")


print("Data analysing...")
publishDatetime.analysis()
print("Data analysis completed.")