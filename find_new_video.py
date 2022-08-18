import json
from googleapiclient.discovery import build

with open('config.json', 'r') as config:
    data = json.load(config)

API_KEY = data['api_key']
CHANNEL_ID = data['channel_id']
LATEST_VID_ID = data['latest_vid_id']
UPLOADS_ID = data['uploads_id']

youtube = build('youtube', 'v3', developerKey=API_KEY)

if not UPLOADS_ID:
    request = youtube.channels().list(
    part='contentDetails',
    forUsername=CHANNEL_ID
    )
    response = request.execute()
    UPLOADS_ID = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def get_new_video_id(uploads_id, latest_video_id):
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_id
    )
    response = request.execute()
    newest_video_id = response['items'][0]['contentDetails']['videoId']
    if newest_video_id == latest_video_id:
        return False
    else:
        return newest_video_id


if __name__ == "__main__":
    new_vid = get_new_video_id(UPLOADS_ID, LATEST_VID_ID)
    if new_vid:
        print(f"Found new video {new_vid}")
    else:
        print("No new video.")
