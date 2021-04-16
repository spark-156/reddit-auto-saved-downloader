import praw
import os
import json
class RedditUser:
    def __init__(self, reddit_username, reddit_password, client_id, client_secret):
			self.saved_posts = {}

			# init praw instance
			self.reddit = praw.Reddit(
					client_id=client_id,
					client_secret=client_secret,
					user_agent="Auto reddit saved downloader",
					reddit_password=reddit_password,
					reddit_username=reddit_username
			)

			# init file if not exist
			if not os.path.isfile(f"saved_posts_{reddit_username}.json"):
					with open(f"saved_posts_{reddit_username}.json", "w") as saved_posts_file:
							json.dump({}, saved_posts_file)

		# Get all saved posts
		# @param limit - get latest {limit} amount of saved posts. Set to None if you want to get all saved posts
		# @returns nothing
		def get_saved_posts(limit=None):
			with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
				self.saved_posts = json.load(saved_posts_file)

			i = 0
			for item in self.reddit.user.me().saved(limit=limit):
				submission = praw.models.Submission(self.reddit, item.id)

				# Check if post is already saved, if it is skip it
				if submission.id in saved_posts: # if guard
					continue
				
				self.saved_posts[submission.id] = submission
				i += 1
			
			with open (f"saved_posts_{self.reddit_username}.json", "w"):
				json.dump(self.saved_posts, saved_posts_file)

		# Get all saved posts present in json file
		# @return dictionary with all post id's as keys and submission object as values.
		def get_cached_saved_posts():
			with open(f"saved_posts_{self.reddit_username}", "r") as saved_posts_file:
				self.saved_posts = json.load(saved_posts_file)

			return self.saved_posts

