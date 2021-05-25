import praw
import os
import json
import crython
from datetime import datetime


def log(message, log_type="Log"):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"{current_time} [{log_type}] {message}")


class RedditUser:
    def __init__(self, account, limit):
        if not limit == None:
            self.limit = int(limit)
        else:
            self.limit = limit

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
    def get_saved_posts(self):
        with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
            self.saved_posts = json.load(saved_posts_file)
            self.cache = self.saved_posts.copy()

        i = 0
        saved = self.reddit.user.me().saved(limit=self.limit)
        log("Gotten all saved posts, comparing to cached now")
        for item in saved:
            # Skip everything that does not have a url or is not a submission
            try:
                # Check if post is already saved, if it is delete it
                if item.id in self.cache:  # if guard
                    del self.cahce.item.id
                    continue

                submission = praw.models.Submission(self.reddit, item.id)

                self.saved_posts[submission.id] = {
                    "title": submission.title,
                    "url": submission.url,
                    "subreddit": submission.subreddit.display_name,
                    "permalink": submission.permalink
                }
                i += 1
            except:
                continue

        if i > 0:
            log(f"Saving {i} newly saved posts to local cache")
        else:
            log("No newly saved posts found")

        with open(f"saved_posts_{self.reddit_username}.json", "w") as saved_posts_file:
            json.dump(self.saved_posts, saved_posts_file)



# Get all environment variables and confirm their validity
limit = os.environ.get("limit", None)
cronjob = os.environ.get("cronjob", "0 0 */2 * * * *")
username = os.environ.get("username", None)
password = os.environ.get("password", None)
client_id = os.environ.get("client_id", None)
client_secret = os.environ.get("client_secret", None)


# Checking if limit env var is set correctly
if len(limit) == 0:
    log("Limit not set, defaulting to None")
    limit = None
elif not limit.isdigit():
    log("Environment variable limit is nog an integer, please do not use floats or text. Limit must be set to a number such as 980 or 254", "Fatal error")
    exit()
elif len(limit) > 0:
    try:
        limit = int(limit)
    except:
        log("Environment variable limit is nog an integer, please do not use floats or text. Limit must be set to a number such as 980 or 254", "Fatal error")
        exit()
else:
    log("could not find anythhing about limit environment variable, defaulting to None")
    limit = None


# checking if cronjob var is set correctly
if len(cronjob) == 0:
    log("Environment variable cronjob not set, defaulting to every two hours aka: '0 0 */2 * * * *'")
    cronjob="0 0 */2 * * * *"


# Check if all env vars have been set
if not (username & password & client_id & client_secret):
    log("username, password, client_id and/ or client_secret haven't all been set. Exiting")
    exit()


# raised ValueError if cronjob is not set correctly, thus allowing me to use a simple way of checking if the var is set correctly
try:
    @crython.job(expr=cronjob)
    def update():
        log('Starting crython job')

        user = RedditUser({"username": username, "password": password, "client_id": client_id, "client_secret": client_secret}, limit)
        log(f"Getting saved posts for user: {user.reddit_username}")
        user.get_saved_posts()
        log("Waiting for next cronjob")


except ValueError: # cronjob not set correctly
    log("Cronjob was not correctly set, make sure it has 7 values and is in the following format: '* * * * * * *'", "Fatal error")
    exit()


if __name__ == '__main__':
    log(f"Environment variables:\nlimit={limit}\ncronjob={cronjob}")
    log("Waiting for first cronjob")
    crython.start()
    crython.join()  # This will block
