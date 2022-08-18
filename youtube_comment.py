import json
import find_new_video
from google_apis import create_service
from time import sleep

with open('config.json', 'r') as config:
    data = json.load(config)

COMMENT = data['comment']
CLIENT_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)


def post_comment(videoid, message):
    request_body = {
        'snippet': {
            'videoId': videoid,
            'topLevelComment': {
                'snippet': {
                    'textOriginal': message
                }
            }
      }
    }
    response = service.commentThreads().insert(
        part='snippet',
        body=request_body
    ).execute()
    print(response)
    print("Comment posted.")


while True:
    new_video = find_new_video.get_new_video_id(find_new_video.UPLOADS_ID, find_new_video.LATEST_VID_ID)
    if new_video:
        post_comment(new_video, COMMENT)
    else:
        print("No new video found.")
    sleep(1)
