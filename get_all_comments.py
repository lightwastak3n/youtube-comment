# Requirements:
# pip install google_api_python_client

import csv

from googleapiclient.discovery import build
from time import sleep


API_KEY = "AIzaSyCRNfIhCXAi1pSCugU5pdWKHM9M2SmTv3c"
VIDEO_ID = "aIciGms2y6A"
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Create csv file for logging comments
with open("all_comments.csv", "w") as csvfile:
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
        with open("all_comments.csv", "a") as csvfile:
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
    # sleep(1)
    try:
        print(f"Downloaded {total_comments} total comments.")
        next_page, new_comments = get_page_comments(next_page)
        total_comments += new_comments
    except KeyError:
        print("Finished downloading comments.")
        break
