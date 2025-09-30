from web_scraping import *
from text_analysis import *
from time_series import *
from social_nw import *
import os
import pandas as pd
import networkx as nx   # required for saving graph

# ----------------------------------------------------
# Setup paths
# ----------------------------------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok=True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")
TEXT_PATH = os.path.join(results_dir, "distracted_boyfriend_text.csv")
TIME_SERIES_PATH = os.path.join(results_dir, "distracted_boyfriend_timeseries.csv")
SOCIAL_NW_PATH = os.path.join(results_dir, "distracted_boyfriend_network.gexf")
MASTER_PATH = os.path.join(results_dir, "meme_master_dataset.csv")

# ----------------------------------------------------
# 1. Web Scraping
# ----------------------------------------------------
print("🔹 Scraping Reddit posts...")
df_posts = scrape_distracted_boyfriend(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
df_posts.to_csv(POSTS_PATH, index=False)
print(f"✅ Saved posts data to {POSTS_PATH}")

# ----------------------------------------------------
# 2. Text Analysis
# ----------------------------------------------------
print("🔹 Running text analysis...")
df_text, freq = analyze_text()
print("Top Words:", freq[:10])  # top 10 words
df_text.to_csv(TEXT_PATH, index=False)
print(f"✅ Saved text analysis results to {TEXT_PATH}")

# ----------------------------------------------------
# 3. Time Series Analysis
# ----------------------------------------------------
print("🔹 Running time series analysis...")
df_time = time_series_analysis()
df_time.to_csv(TIME_SERIES_PATH, index=False)
print(f"✅ Saved time series results to {TIME_SERIES_PATH}")

# ----------------------------------------------------
# 4. Social Network Analysis
# ----------------------------------------------------
print("🔹 Building social network graph...")
graph = build_social_graph(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
nx.write_gexf(graph, SOCIAL_NW_PATH)
print(f"✅ Saved social network graph to {SOCIAL_NW_PATH}")

# ----------------------------------------------------
# 5. Combine All Results into One Master CSV
# ----------------------------------------------------
print("🔹 Creating combined dataset...")

# Reload CSVs to ensure consistency
posts_df = pd.read_csv(POSTS_PATH)
text_df = pd.read_csv(TEXT_PATH)
time_df = pd.read_csv(TIME_SERIES_PATH)

# Ensure datetime columns exist
posts_df["created_dt"] = pd.to_datetime(posts_df["created_utc"], unit="s").dt.date
text_df["created_dt"] = pd.to_datetime(text_df["created_utc"], unit="s").dt.date

# Merge posts + text analysis on post ID
combined = posts_df.merge(text_df, on="id", suffixes=("_post", "_text"))

# Merge with daily aggregated time series
time_df["date"] = pd.to_datetime(time_df["date"]).dt.date
combined = combined.merge(time_df, left_on="created_dt_post", right_on="date", how="left")

# Save master dataset
combined.to_csv(MASTER_PATH, index=False)
print(f"✅ Saved master dataset to {MASTER_PATH}")

print("🎉 Pipeline completed successfully!")
