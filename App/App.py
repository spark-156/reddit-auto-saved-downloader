import praw
import os
import json

try:
	CLIENT_ID = os.environ["CLIENT_ID"]
	CLIENT_SECRET = os.environ["CLIENT_SECRET"]
	REDDIT_USERNAME = os.environ["REDDIT_USERNAME"]
	REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]
	# Log all env variables
	print(f"[Log] REDDIT_USERNAME = {REDDIT_USERNAME}\n[Log] CLIENT_ID = {CLIENT_ID} \n[Log] CLIENT_SECRET = {CLIENT_SECRET}")
except:
	print(f"[Error] Must set all environment variables!")
	exit()


reddit = praw.Reddit(
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	user_agent="Auto reddit saved downloader",
	username=REDDIT_USERNAME,
	password=REDDIT_PASSWORD,
)

with open("saved_posts.json", "r") as saved_posts_file:
	saved_posts = json.load(saved_posts_file)

saved = reddit.user.me().saved(limit=None)
for item in saved:
	post = praw.models.Submission(reddit, item.id)
	saved_posts[post.id] = post.url
	print(post.id, post.url)

with open("saved_posts.json", "w") as saved_posts_file:
	json.dump(saved_posts, saved_posts_file)

