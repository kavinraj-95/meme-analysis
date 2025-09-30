import pandas as pd
import matplotlib.pyplot as plt
import os

base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok=True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")
TEXT_PATH = os.path.join(results_dir, "distracted_boyfriend_text.csv")
TIME_SERIES_PATH = os.path.join(results_dir, "distracted_boyfriend_timeseries.csv")
SOCIAL_NW_PATH = os.path.join(results_dir, "distracted_boyfriend_network.gexf")

def time_series_analysis(input_csv=TEXT_PATH):
    # Load text analysis results
    df = pd.read_csv(input_csv)
    df["created_dt"] = pd.to_datetime(df["created_utc"], unit="s")

    # Aggregate by date
    daily = df.groupby(df["created_dt"].dt.date).agg(
        avg_score=("score", "mean"),
        post_count=("id", "count"),
        avg_sentiment=("sentiment", "mean")
    ).reset_index()

    # Rename columns for clarity in Tableau/Power BI
    daily.rename(columns={"created_dt": "date"}, inplace=True)

    # Save clean CSV for visualization
    daily.to_csv(TIME_SERIES_PATH, index=False)

    # ---- Visualization 1: Number of posts per day ----
    plt.figure(figsize=(12, 6))
    plt.plot(daily["date"], daily["post_count"], label="Number of Posts per Day")
    plt.title("'Distracted Boyfriend' Meme: Posts per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Posts")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    SERIES_PNG_PATH = os.path.join(results_dir, "time_series_posts.png")
    plt.savefig(SERIES_PNG_PATH, bbox_inches="tight")
    plt.close()

    # ---- Visualization 2: Average sentiment score ----
    plt.figure(figsize=(12, 6))
    plt.plot(daily["date"], daily["avg_sentiment"], label="Average Sentiment Score",
             linestyle="--", color="orange")
    plt.title("'Distracted Boyfriend' Meme: Average Sentiment Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    SENTIMENT_PNG_PATH = os.path.join(results_dir, "time_series_sentiment.png")
    plt.savefig(SENTIMENT_PNG_PATH, bbox_inches="tight")
    plt.close()

    return daily
