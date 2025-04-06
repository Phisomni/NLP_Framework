# src/visualizations.py

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter

def plot_sankey(word_counts, word_list=None, k=5):
    # Extract top-k words if not provided
    if word_list is None:
        all_words = []
        for counts in word_counts.values():
            all_words.extend(counts.keys())
        common_words = [w for w, _ in Counter(all_words).most_common(k)]
    else:
        common_words = word_list

    labels = list(word_counts.keys()) + common_words
    sources, targets, values = [], [], []

    for i, doc in enumerate(word_counts):
        for word in common_words:
            count = word_counts[doc].get(word, 0)
            if count > 0:
                sources.append(i)
                targets.append(len(word_counts) + common_words.index(word))
                values.append(count)

    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig.show()

def plot_wordcount_subplots(word_counts):
    fig, axs = plt.subplots(len(word_counts), 1, figsize=(10, len(word_counts) * 3))
    if len(word_counts) == 1:
        axs = [axs]

    for ax, (doc, wc) in zip(axs, word_counts.items()):
        top_words = Counter(wc).most_common(10)
        words, counts = zip(*top_words)
        ax.bar(words, counts)
        ax.set_title(doc)
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def plot_comparative_readability(readability_scores):
    docs = list(readability_scores.keys())
    scores = list(readability_scores.values())

    plt.figure(figsize=(10, 5))
    plt.bar(docs, scores)
    plt.ylabel("Flesch Reading Ease")
    plt.title("Readability Score by Document")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
