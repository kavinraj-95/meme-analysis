import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok = True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")
TEXT_PATH = os.path.join(results_dir, "distracted_boyfriend_text.csv")
TIME_SERIES_PATH = os.path.join(results_dir, "distracted_boyfriend_timeseries.csv")
SOCIAL_NW_PATH = os.path.join(results_dir, "distracted_boyfriend_network.gexf")


def time_series_analysis(input_csv = TEXT_PATH):
    df = pd.read_csv(input_csv)
    df["created_dt"] = pd.to_datetime(df["created_utc"], unit="s")

    daily = df.groupby(df["created_dt"].dt.date).agg(
        avg_score=("score", "mean"),
        post_count=("id", "count"),
        avg_sentiment=("sentiment", "mean")
    ).reset_index()

    plt.figure(figsize=(12, 6))
    plt.plot(daily["created_dt"], daily["post_count"], label="Number of Posts per Day")
    plt.title("'Distracted Boyfriend' Meme: Posts per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.grid(True)
    plt.legend()
    SERIES_PNG_PATH = os.path.join(results_dir, "time_series_posts.png")
    plt.savefig(SERIES_PNG_PATH)
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(daily["created_dt"], daily["avg_sentiment"], label="Average Sentiment Score", linestyle="--", color="orange")
    plt.title("'Distracted Boyfriend' Meme: Average Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.grid(True)
    plt.legend()
    SENTIMENT_PNG_PATH = os.path.join(results_dir, "time_series_sentiment.png")
    plt.savefig(SENTIMENT_PNG_PATH)
    plt.close()

    return daily

 

