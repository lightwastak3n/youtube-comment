# What is this?
This was made for MrBeast 100M subscribers video. First comment on that video would get $10000.
`find_new_video.py` - can be used by itself to check for a newer video than the one you specified.
`youtube_comment.py` - is used to post the comment on a new video (by default checks for the new video once a second)
`get_all_comments.py` - scrapes all the comments from a specified video id and saves them to `.csv` file.

# Setup
In order to use this you need to first set it up.
1. You need a couple of packages 
	- `pip install google-api-python-client`
	- `pip install google-auth-oauthlib`
2. In order to post a comment you need access to youtube api and to your own account which is going to post that comment.
	- Go to google cloud (https://console.cloud.google.com/) and create a new project
	- Go to project dashboard and click View all products
	- Go to APIs and services and click Enable APIs and services
	- In the API library search for YouTube Data API v3
	- Enable that and open it (Manage)
	- Go to credentials
	- Create API key and OAuth Client ID (choose Desktop app)
	- Copy the API key to your `config.json` file
	- Download JSON of your OAuth, call it `client-secret.json` and save it in the sam folder as the scripts
	- Go to OAuth consent screen (https://console.cloud.google.com/apis/credentials/consent) and press PUBLISH APP
3. Fill the `config.json` with all the info. If you don't know the id of the uploads playlist of a given channel (`"uploads_id"`), just leave it empty. Here is an example of config (using this channel https://www.youtube.com/channel/UCY1kMZp36IQSyNx_9h4mpCg):
```json
{
"api_key" : "AIzaSyCRNfIhCXAi1pSCugU5pdWKHM9M2SmTv3c",
"channel_id" : "UCY1kMZp36IQSyNx_9h4mpCg",
"latest_vid_id": "h8g9wfI9nGI",
"uploads_id": "UUY1kMZp36IQSyNx_9h4mpCg",
"comment": "First",
video_id_get_comments": "xsLJZyih3Ac"
}
```

# Use
If you just want to post a comment automatically, just run `youtube_comment.py`.
When you run it for the first time you are going to have to authorize it, so that it can access your account and post your comments.
It should open in your default browser, or you can just paste the link from the terminal into your browser.
If you get "Google hasn't verified this app" just go to Advanced -> Go to (your project name) and Allow it access.

By default `youtube_comment.py` checks for a new video once a second, but you can change it if you are going to run it for long period of time since youtube api has a limited number of requests per day.

# References
- `google_apis.py` - https://learndataanalysis.org/google-py-file-source-code/