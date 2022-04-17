import os
import praw


def get_reddit():
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
    )
    return reddit

def get_subreddit(subreddit):
    reddit = get_reddit()
    return reddit.subreddit(subreddit)

def get_threads(subreddit, limit=10):
    threads = get_subreddit(subreddit).search(
        'flair:"Daily+Discussion"', limit=limit)
    return threads

