from web_scraping import *
from text_analysis import *
from time_series import *
from social_nw import *
import os

base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok = True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")
TEXT_PATH = os.path.join(results_dir, "distracted_boyfriend_text.csv")
TIME_SERIES_PATH = os.path.join(results_dir, "distracted_boyfriend_timeseries.csv")
SOCIAL_NW_PATH = os.path.join(results_dir, "distracted_boyfriend_network.gexf")

# Web Scraping
df = scrape_distracted_boyfriend(CLIENT_ID , CLIENT_SECRET, USER_AGENT)
df.to_csv(POSTS_PATH, index = False)

# Text Analysis 
df, freq = analyze_text()
print("Top Words:", freq)
df.to_csv(TEXT_PATH, index = False)

# Time Series 
daily = time_series_analysis()
daily.to_csv(SOCIAL_NW_PATH, index = False)

# Social Network Analysis
graph = build_social_graph(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
nx.write_gexf(graph, SOCIAL_NW_PATH)
