import pandas as pd
from collections import Counter
import re
import nltk
import os
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords


base_dir = os.path.dirname(os.path.dirname(__file__))  
results_dir = os.path.join(base_dir, "results")
os.makedirs(results_dir, exist_ok = True)

POSTS_PATH = os.path.join(results_dir, "distracted_boyfriend_posts.csv")
TEXT_PATH = os.path.join(results_dir, "distracted_boyfriend_text.csv")
TIME_SERIES_PATH = os.path.join(results_dir, "distracted_boyfriend_timeseries.csv")
SOCIAL_NW_PATH = os.path.join(results_dir, "distracted_boyfriend_network.gexf")



def analyze_text(input_csv = POSTS_PATH):
    df = pd.read_csv(input_csv)
    sia = SentimentIntensityAnalyzer()
    stop_words = set(stopwords.words("english"))

    df["clean_title"] = df["title"].apply(
        lambda x: " ".join(
            [w.lower() for w in re.findall(r"\b\w+\b", str(x)) if w.lower() not in stop_words]
        )
    )
    df["sentiment"] = df["clean_title"].apply(lambda x: sia.polarity_scores(x)["compound"])

    all_tokens = " ".join(df["clean_title"]).split()
    word_freq = Counter(all_tokens).most_common(20)

    return df, word_freq
 

