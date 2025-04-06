# src/preprocessors.py

import re
import string
from collections import Counter
import textstat
from nltk.sentiment import SentimentIntensityAnalyzer

def default_parser(text, stop_words=set()):
    # Clean and tokenize
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", "", text)
    tokens = text.split()

    # Filter stop words
    filtered_tokens = [w for w in tokens if w not in stop_words]

    # Word count
    word_freq = Counter(filtered_tokens)

    # Stats
    word_len_avg = sum(len(w) for w in filtered_tokens) / len(filtered_tokens) if filtered_tokens else 0
    readability = textstat.flesch_reading_ease(text)

    # Sentiment
    try:
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(text)["compound"]
    except Exception:
        sentiment_score = 0

    return {
        "word_count": dict(word_freq),
        "word_length": word_len_avg,
        "readability": readability,
        "sentiment": sentiment_score
    }
