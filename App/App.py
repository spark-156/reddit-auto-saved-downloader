import praw
import os
import json
import crython

limit = os.environ.get("limit", None)
cronjob = os.environ.get("cronjob", "0 */2 * * * * *")

# # Setup logging for praw
# import logging

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)


class RedditUser:
    def __init__(self, account, limit):
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
        log("Getting saved posts from reddit")
        with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
            self.saved_posts = json.load(saved_posts_file)

        i = 0
        saved = self.reddit.user.me().saved(limit=self.limit)
        log("Gotten all saved posts")
        for item in saved:
            # Skip everything that does not have a url or is not a submission
            try:
                # Check if post is already saved, if it is skip it
                if item.id in self.saved_posts:  # if guard
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
        log(f"Saving {i} saved posts to local cache")
        with open(f"saved_posts_{self.reddit_username}.json", "w") as saved_posts_file:
            json.dump(self.saved_posts, saved_posts_file)

    # Get all saved posts present in json file
    # @returns nothing
    def log_cached_saved_posts(self):
        log("getting cached saved posts")
        with open(f"saved_posts_{self.reddit_username}.json", "r") as saved_posts_file:
            self.saved_posts = json.load(saved_posts_file)
        log(self.saved_posts)

# Log a message in a certain format
# @returns nothing
def log(message):
    print(f"[Log] {message}")


@crython.job(expr=cronjob)
def update():
    log("Opening all given accounts")
    with open("reddit_accounts.json", "r") as reddit_accounts_file:
        reddit_accounts = json.load(reddit_accounts_file)

    for account in reddit_accounts:
        log("Starting prawn")
        user = RedditUser(account, limit)
        log(f"Getting saved posts for user: {user.reddit_username}")
        user.get_saved_posts()
        # user.log_cached_saved_posts()


if __name__ == '__main__':
    print('[Log] Waiting for crython job')
    crython.start()
    crython.join()  # This will block
