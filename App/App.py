import praw
import os
import json

class RedditUser:
	def __init__(self, account):
		self.saved_posts = {}
		self.reddit_username = account["username"]
		self.reddit = praw.Reddit(
				client_id=account["client_id"],
				client_secret=account["client_secret"],
				user_agent="Auto reddit saved downloader",
				password=account["password"],
				username=account["username"]
		)
		# init file if not exist
		if not os.path.isfile(f"saved_posts_{self.reddit_username}.json"):
			with open(f"saved_posts_{self.reddit_username}.json", "w") as saved_posts_file:
				json.dump({}, saved_posts_file)

	# Get all saved posts
	# @param limit - get latest {limit} amount of saved posts. Set to None if you want to get all saved posts
	# @returns nothing
	def get_saved_posts(self, limit=None):
		self.log("getting saved posts from reddit")
		with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
			self.saved_posts = json.load(saved_posts_file)

		i = 0
		saved = self.reddit.user.me().saved(limit=limit)
		for item in saved:
			submission = praw.models.Submission(self.reddit, item.id)

			# Check if post is already saved, if it is skip it
			if submission.id in self.saved_posts: # if guard
				continue
			
			self.saved_posts[submission.id] = {"title": submission.title, "url": submission.url, "subreddit": submission.subreddit.display_name, "permalink": submission.permalink}
			i += 1
		self.log(f"saving {i} saved posts to local cache")
		with open (f"saved_posts_{self.reddit_username}.json", "w") as saved_posts_file:
			json.dump(self.saved_posts, saved_posts_file)

	# Get all saved posts present in json file
	# @returns nothing
	def log_cached_saved_posts(self):
		self.log("getting cached saved posts")
		with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
			self.saved_posts = json.load(saved_posts_file)
		self.log(self.saved_posts)

	# Log a message in a certain format
	# @returns nothing
	def log(self, message):
		print(f"[Log] {message}")
	

with open("reddit_accounts.json", "r") as reddit_accounts_file:
	reddit_accounts = json.load(reddit_accounts_file)

for account in reddit_accounts:
	user = RedditUser(account)
	user.get_saved_posts(20)
	user.log_cached_saved_posts()

