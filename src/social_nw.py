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

base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok = True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")


def build_social_graph(client_id, client_secret, user_agent, input_csv = POSTS_PATH, max_comments=50):
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    df = pd.read_csv(input_csv)
    graph = nx.DiGraph()

    for _, row in df.iterrows():
        submission = reddit.submission(id=row["id"])
        submission.comments.replace_more(limit=0)
        for comment in submission.comments[:max_comments]:
            if comment.author and row["author"] and comment.author.name != row["author"]:
                graph.add_edge(comment.author.name, row["author"])

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, k=0.15, iterations=20)
    
    node_degrees = dict(graph.degree())
    node_sizes = [v * 100 for v in node_degrees.values()]
    
    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, alpha=0.7)
    nx.draw_networkx_edges(graph, pos, alpha=0.4)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    
    plt.title("Social Network of Reddit Users Commenting on 'Distracted Boyfriend' Meme Posts")
    plt.xlabel("Users")
    plt.ylabel("Connections")
    
    GRAPH_PATH = os.path.join(results_dir, "social_graph.png")
    plt.savefig(GRAPH_PATH)
    plt.close()
    return graph
 

