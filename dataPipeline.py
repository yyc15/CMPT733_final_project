from API import getYoutubeTrendingVideo as api
import uploadYoutubeData as upload

print("getting api data...")
api.get_data()
print("api data downloaded.")

print("uploading api data to drive...")
upload.uploadDataToDrive("api")
print("api data uploaded.")

