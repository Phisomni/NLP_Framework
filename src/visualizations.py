import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter
import numpy as np


def plot_sankey(word_counts, word_list=None, k=5, cluster_map=None, cluster_colors=None):
    """
    Generate a Sankey diagram showing the frequency of selected words across multiple texts.
    Connections (links) are color-coded by department cluster.

    Args:
        word_counts (dict): Mapping from department to word frequency dict.
        word_list (list, optional): List of words to visualize. Uses top-k if None.
        k (int, optional): Top-k most frequent words to visualize if no word_list is provided.
        cluster_map (dict, optional): Mapping from department label to cluster label.
        cluster_colors (dict, optional): Mapping from cluster label to color.

    Produces:
        Interactive Sankey diagram.
    """
    import plotly.graph_objects as go
    from collections import Counter

    # fallback to empty maps if not provided
    cluster_map = cluster_map or {}
    cluster_colors = cluster_colors or {}

    if word_list is None:
        all_words = []
        for counts in word_counts.values():
            all_words.extend(counts.keys())
        common_words = [w for w, _ in Counter(all_words).most_common(k)]
    else:
        common_words = word_list

    departments = list(word_counts.keys())
    labels = departments + common_words
    sources, targets, values, link_colors = [], [], [], []

    for i, dept in enumerate(departments):
        cluster = cluster_map.get(dept, "Other")
        color = cluster_colors.get(cluster, "gray")
        for word in common_words:
            count = word_counts[dept].get(word, 0)
            if count > 0:
                sources.append(i)
                targets.append(len(departments) + common_words.index(word))
                values.append(count)
                link_colors.append(color)

    # simple neutral color for all nodes
    node_colors = ["#eeeeee"] * len(labels)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            label=labels,
            color=node_colors,
            pad=15,
            thickness=20
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors
        )
    )])

    fig.update_layout(
        title_text="Word Frequency Sankey Diagram (Colored by Department Cluster)",
        font_size=12
    )
    fig.show()



def plot_wordcount_subplots(word_counts, k=10, p=4):
    """
    Display grouped bar charts of the top-k words for each document in batches of p documents.

    Args:
        word_counts (dict): Dictionary mapping document labels to word frequency dictionaries.
        k (int, optional): Number of top words to display per document.
        p (int, optional): Number of documents per figure (must be 4 for 2x2 layout).

    Produces:
        Multiple 2x2 subplot pages of bar charts showing word frequencies per document.
    """
    docs = list(word_counts.keys())
    chunk_size = p

    for i in range(0, len(docs), chunk_size):
        fig, axs = plt.subplots(2, 2, figsize=(14, 8))
        axs = axs.flatten()
        fig.subplots_adjust(hspace=0.6)

        for j in range(chunk_size):
            if i + j >= len(docs):
                axs[j].axis('off')
                continue
            doc = docs[i + j]
            wc = word_counts[doc]
            top_words = Counter(wc).most_common(k)
            words, counts = zip(*top_words)
            axs[j].bar(words, counts)
            axs[j].set_title(doc)
            axs[j].tick_params(axis='x', rotation=45)

        plt.suptitle(f"Top {k} Words (Group {i // chunk_size + 1})")
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()


def plot_comparative_readability(readability_scores):
    """
    Bar chart comparing the Flesch Reading Ease scores across documents.

    Args:
        readability_scores (dict): Mapping of document labels to readability scores.

    Produces:
        A single bar chart visualization.
    """
    docs = list(readability_scores.keys())
    scores = list(readability_scores.values())

    plt.figure(figsize=(10, 5))
    plt.bar(docs, scores)
    plt.ylabel("Flesch Reading Ease")
    plt.title("Readability Score by Department")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def plot_comparative_sentiment(sentiment_scores):
    """
    Bar chart comparing the compound sentiment scores across documents.

    Args:
        sentiment_scores (dict): Mapping of document labels to sentiment scores.

    Produces:
        A single bar chart visualization with a baseline at neutral (0).
    """
    docs = list(sentiment_scores.keys())
    scores = list(sentiment_scores.values())

    plt.figure(figsize=(10, 5))
    plt.bar(docs, scores, color='skyblue')
    plt.ylabel("Compound Sentiment Score")
    plt.title("Sentiment Score by Department")
    plt.xticks(rotation=45, ha="right")
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.show()


def plot_department_radar(data, departments=None):
    """
    Radar chart comparing normalized text metrics across departments.

    Args:
        data (dict): Nested dictionary containing metrics like readability, sentiment, etc.
        departments (list, optional): Specific department labels to plot. If None, all are used.

    Produces:
        A radar chart overlaying multiple departments' metric profiles.
    """
    labels = ["readability", "sentiment", "word_length", "sentence_length", "type_token_ratio"]

    if departments is None:
        departments = list(data.get("readability", {}).keys())

    print("\nRadar Chart: Normalizing metrics across departments")
    for metric in labels:
        print(f"{metric}: {list(data.get(metric, {}).keys())}")

    # Collect raw values per metric
    raw_metric_data = {metric: [] for metric in labels}
    for dept in departments:
        for metric in labels:
            raw_metric_data[metric].append(data.get(metric, {}).get(dept, 0))

    # Normalize values to [0,1]
    normalized_data = {metric: [] for metric in labels}
    for metric in labels:
        values = raw_metric_data[metric]
        min_val, max_val = min(values), max(values)
        range_val = max_val - min_val if max_val != min_val else 1
        normalized_data[metric] = [(v - min_val) / range_val for v in values]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for i, dept in enumerate(departments):
        values = [normalized_data[metric][i] for metric in labels]
        values += values[:1]
        ax.plot(angles, values, label=dept)
        ax.fill(angles, values, alpha=0.1)

    ax.set_title("Normalized Department Profiles", size=16)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    plt.tight_layout()
    plt.show()