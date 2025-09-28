# text_analysis.py
import pandas as pd
from collections import Counter
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

def analyze_text(input_csv="distracted_boyfriend_posts.csv"):
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

if __name__ == "__main__":
    df, freq = analyze_text()
    print("Top Words:", freq)
    df.to_csv("distracted_boyfriend_text.csv", index=False)

