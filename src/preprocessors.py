import re
import string
from collections import Counter
import textstat
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure VADER sentiment lexicon is available
nltk.download("vader_lexicon")


def clean_text(text):
    """
    Clean up raw extracted text by removing common unwanted patterns.

    This function is especially useful for preprocessing text extracted from PDFs,
    where timestamps, URLs, and pagination artifacts may appear.

    Args:
        text (str): The raw extracted text.

    Returns:
        str: Cleaned text with normalized whitespace.
    """
    # Remove timestamp patterns like "4/6/25, 6:08 PM"
    text = re.sub(r"\d+/\d+/\d{2,4},\s+\d+:\d+\s+(AM|PM)", "", text)

    # Remove URLs (http/https links)
    text = re.sub(r"http[s]?://\S+", "", text)

    # Remove page markers like "3/33"
    text = re.sub(r"\b\d+/\d+\b", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def default_parser(text, stop_words=set()):
    """
    Default parser for course description texts. Extracts token-level and sentence-level metrics.

    This parser is designed to process cleaned educational text and extract useful statistics
    for analysis and visualization.

    Args:
        text (str): The raw text to be parsed and analyzed.
        stop_words (set): Optional set of stop words to exclude from analysis.

    Returns:
        dict: A dictionary with extracted metrics including:
            - word_count (dict): Frequency of non-stopword tokens.
            - word_length (float): Average length of tokens.
            - sentence_length (float): Average sentence length (in words).
            - type_token_ratio (float): Lexical diversity.
            - readability (float): Flesch Reading Ease score.
            - sentiment (float): Average compound sentiment score (VADER).
    """
    # Step 1: Clean the text
    text = clean_text(text)
    text_lower = text.lower()

    # Step 2: Extract sentences while preserving sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text_lower)
    valid_sentences = [s.strip() for s in sentences if s.strip()]

    # Step 3: Remove punctuation for tokenization
    text_for_tokens = re.sub(rf"[{re.escape(string.punctuation)}]", "", text_lower)
    tokens = text_for_tokens.split()

    # Filter out standalone numbers or course codes like "engl1234"
    tokens = [
        w for w in tokens
        if not w.isdigit() and not re.match(r"^[a-z]*\d+[a-z]*$", w)
    ]

    # Remove stopwords
    filtered_tokens = [w for w in tokens if w not in stop_words]

    # Step 4: Compute lexical statistics
    word_freq = Counter(filtered_tokens)
    word_len_avg = sum(len(w) for w in filtered_tokens) / len(filtered_tokens) if filtered_tokens else 0
    avg_sentence_len = sum(len(s.split()) for s in valid_sentences) / len(valid_sentences) if valid_sentences else 0
    type_token = len(set(filtered_tokens)) / len(filtered_tokens) if filtered_tokens else 0

    # Step 5: Compute readability score
    try:
        readability = textstat.flesch_reading_ease(text)
        readability = max(min(readability, 100), 0)  # Clamp to [0, 100]
    except:
        readability = 50  # Fallback if textstat fails

    if len(valid_sentences) < 3:
        print("Not enough valid sentences. Using fallback readability = 50.")
        readability = 50

    # Step 6: Compute sentiment using VADER
    try:
        sia = SentimentIntensityAnalyzer()
        sentence_scores = [sia.polarity_scores(s)["compound"] for s in valid_sentences]
        sentiment_score = sum(sentence_scores) / len(sentence_scores) if sentence_scores else 0

        # Smooth extreme values to avoid visual skew
        if sentiment_score > 0.9:
            sentiment_score = 0.9 + (sentiment_score - 0.9) * 0.1
        elif sentiment_score < -0.9:
            sentiment_score = -0.9 + (sentiment_score + 0.9) * 0.1
    except:
        sentiment_score = 0

    # Preview the results for debugging
    print(f"Readability: {readability:.2f} | Sentiment: {sentiment_score:.2f} | "
          f"Word Len: {word_len_avg:.2f} | Sent Len: {avg_sentence_len:.2f} | "
          f"TTR: {type_token:.2f}")

    return {
        "word_count": dict(word_freq),
        "word_length": word_len_avg,
        "sentence_length": avg_sentence_len,
        "type_token_ratio": type_token,
        "readability": readability,
        "sentiment": sentiment_score
    }
