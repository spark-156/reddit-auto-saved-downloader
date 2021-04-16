import praw
import os
import json

try:
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    REDDIT_USERNAME = os.environ["REDDIT_USERNAME"]
    REDDIT_PASSWORD = os.environ["REDDIT_PASSWORD"]
    # Log all env variables
    print(
        f"[Log] REDDIT_USERNAME = {REDDIT_USERNAME}\n[Log] CLIENT_ID = {CLIENT_ID} \n[Log] CLIENT_SECRET = {CLIENT_SECRET}")
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


        # read file
with open("saved_posts.json", "r") as saved_posts_file:
    saved_posts = json.load(saved_posts_file)

# get all saved items and check if downloaded already
i = 0
saved = reddit.user.me().saved(limit=5)
for item in saved:
    post = praw.models.Submission(reddit, item.id)
    if post.id in saved_posts:  # if guard
        continue
    saved_posts[post.id] = {"url": post.url,
                            "title": post.title, "permalink": post.permalink}
    i += 1

# Logging to user
if i:
    print(f"[Log] found {i} unique posts, downloading now")
else:
    print(f"[Log] found no unique posts, nothing to download waiting for next cronjob")

# save file at end of script
with open("saved_posts.json", "w") as saved_posts_file:
    json.dump(saved_posts, saved_posts_file)


# init file if not exist
if not os.path.isfile("saved_posts.json"):
    with open("saved_posts.json", "w") as saved_posts_file:
        json.dump({}, saved_posts_file)
