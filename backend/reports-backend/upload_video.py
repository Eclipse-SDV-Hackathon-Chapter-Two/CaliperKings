import requests

url = 'http://127.0.0.1:3002/api/upload_video'
file_path = '/Users/mac/zzzzz/hackathon/sdv_hackathon_chapter2/final/CaliperKings/2024-11-19_15-45-21_ts_det.mp4'

with open(file_path, 'rb') as video_file:
    files = {'video': video_file}
    response = requests.post(url, files=files)

print(response.text)
