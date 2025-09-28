# social_network.py
import praw
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from dotenv import load_dotenv 
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

def build_social_graph(client_id, client_secret, user_agent, input_csv="distracted_boyfriend_posts.csv", max_comments=50):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    df = pd.read_csv(input_csv)
    G = nx.DiGraph()

    for _, row in df.iterrows():
        submission = reddit.submission(id=row["id"])
        submission.comments.replace_more(limit=0)
        for comment in submission.comments[:max_comments]:
            if comment.author and row["author"] and comment.author.name != row["author"]:
                G.add_edge(comment.author.name, row["author"])

    nx.draw(G, with_labels=False, node_size=30, alpha=0.7)
    plt.savefig("social_graph.png")
    return G

if __name__ == "__main__":
    G = build_social_graph(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    nx.write_gexf(G, "distracted_boyfriend_network.gexf")

