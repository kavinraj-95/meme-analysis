import pandas as pd
import matplotlib.pyplot as plt

def time_series_analysis(input_csv="distracted_boyfriend_text.csv"):
    df = pd.read_csv(input_csv)
    df["created_dt"] = pd.to_datetime(df["created_utc"], unit="s")

    daily = df.groupby(df["created_dt"].dt.date).agg(
        avg_score=("score", "mean"),
        post_count=("id", "count"),
        avg_sentiment=("sentiment", "mean")
    ).reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(daily["created_dt"], daily["post_count"], label="Posts per day")
    plt.legend()
    plt.savefig("time_series_posts.png")

    plt.figure(figsize=(10, 5))
    plt.plot(daily["created_dt"], daily["avg_sentiment"], label="Avg sentiment", linestyle="--")
    plt.legend()
    plt.savefig("time_series_sentiment.png")

    return daily

if __name__ == "__main__":
    daily = time_series_analysis()
    daily.to_csv("distracted_boyfriend_timeseries.csv", index=False)

