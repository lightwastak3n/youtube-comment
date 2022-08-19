import csv
import json
import os
from googleapiclient.discovery import build


with open('config.json', 'r') as config:
    data = json.load(config)

API_KEY = data['api_key']
VIDEO_ID = ""
if not VIDEO_ID:
    VIDEO_ID = data['video_id_get_comments']

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Create csv file for logging comments
with open(os.path.join(os.path.dirname(__file__), "all_comments.csv"), "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    headers = ["Text", "Author_name", "Author_url", "Likes", "Replies", "Time_published"]
    writer.writerow(headers)


def write_comments(response):
    new_comments = 0
    for comment in response['items']:
        text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
        author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        author_url = comment['snippet']['topLevelComment']['snippet']['authorChannelUrl']
        likes = comment['snippet']['topLevelComment']['snippet']['likeCount']
        replies = comment['snippet']['totalReplyCount']
        time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
        with open(os.path.join(os.path.dirname(__file__), "all_comments.csv"), "a") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=";")
            csv_writer.writerow([time, author, author_url, likes, replies, text, time])
        new_comments += 1
    return new_comments


def get_first_comments():
    request = youtube.commentThreads().list(
        part="id,snippet",
        order="time",
        videoId=VIDEO_ID
    )
    response = request.execute()
    next_page = response['nextPageToken']
    new_comments = write_comments(response)
    return next_page, new_comments


def get_page_comments(pageToken):
    request = youtube.commentThreads().list(
        part='id,snippet',
        pageToken=pageToken,
        order="time",
        videoId=VIDEO_ID
    )
    response = request.execute()
    new_comments = write_comments(response)
    next_page = response['nextPageToken']
    return next_page, new_comments


total_comments = 0
next_page, new_comments = get_first_comments()
total_comments += new_comments
while True:
    try:
        print(f"Downloaded {total_comments} total comments.")
        next_page, new_comments = get_page_comments(next_page)
        total_comments += new_comments
    except KeyError:
        print("Finished downloading comments.")
        break
