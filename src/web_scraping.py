import praw
import pandas as pd
from dotenv import load_dotenv 
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

def scrape_distracted_boyfriend(client_id, client_secret, user_agent, limit=200):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit("memes")
    query = "Distracted Boyfriend"
    posts = []

    for submission in subreddit.search(query, limit=limit):
        posts.append({
            "id": submission.id,
            "title": submission.title,
            "score": submission.score,
            "created_utc": submission.created_utc,
            "num_comments": submission.num_comments,
            "url": submission.url,
            "author": str(submission.author),
        })

    return pd.DataFrame(posts)

