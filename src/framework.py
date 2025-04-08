from collections import defaultdict
from .preprocessors import default_parser
import os

class TextAnalysisFramework:
    """
    A framework for text analysis that supports loading, parsing, and visualizing text data.
    
    This framework handles multiple texts, maintains stopwords, and provides various
    visualization methods for comparative text analysis.
    """

    def __init__(self):
        """
        Initialize the TextAnalysisFramework with empty data structures.
        
        Attributes:
            stop_words (set): Set of stopwords to be excluded from analysis
            data (defaultdict): Nested dictionary to store analysis results by type and text label
            raw_texts (dict): Dictionary to store original text content by label
        """
        self.stop_words = set()
        self.data = defaultdict(dict)
        self.raw_texts = {}

    # data processing functions

    def load_stop_words(self, stopfile):
        """
        Load stopwords from a file.
        
        Args:
            stopfile (str): Path to the file containing stopwords (one per line)
        """
        with open(stopfile, 'r') as f:
            self.stop_words = set(word.strip().lower() for word in f.readlines())

    def load_text(self, filename, label=None, parser=None):
        """
        Load and parse a text file.
        
        Args:
            filename (str): Path to the text file to be loaded
            label (str, optional): Label for the text. Defaults to filename basename if None.
            parser (callable, optional): Function to parse the text. Defaults to default_parser.
                                       Parser should accept (text, stop_words) and return a dict.
        """
        if label is None:
            label = os.path.basename(filename)

        if parser is None:
            parser = default_parser

        with open(filename, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        self.raw_texts[label] = raw_text
        parsed_output = parser(raw_text, self.stop_words)
        
        for key, value in parsed_output.items():
            self.data[key][label] = value

    # visualization functions

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generate a Sankey diagram for word counts across texts.
        
        Args:
            word_list (list, optional): List of specific words to include in the visualization.
                                       If None, top words will be used.
            k (int, optional): Number of top words to include if word_list is None. Defaults to 5.
        """
        from .visualizations import plot_sankey
        plot_sankey(self.data["word_count"], word_list, k)

    def top_word_subplots(self, k=10, p=4):
        """
        Generate word count subplots for comparative analysis.
        
        This visualization displays word frequency distributions across different texts.
        """
        from .visualizations import plot_wordcount_subplots
        plot_wordcount_subplots(self.data["word_count"], k, p)

    def readability_bar(self):
        """
        Generate comparative readability visualization.
        
        This visualization compares readability metrics across different texts.
        """
        from .visualizations import plot_comparative_readability
        plot_comparative_readability(self.data.get("readability", {}))

    def sentiment_bar(self):
        """
        Generate comparative sentiment visualization.
        
        This visualization compares sentiment analysis results across different texts.
        """
        from .visualizations import plot_comparative_sentiment
        print("Sentiment scores:", self.data.get("sentiment", {}))
        plot_comparative_sentiment(self.data.get("sentiment", {}))

    def radar(self):
        """
        Generate radar chart for department-specific metrics.
        
        This visualization displays multiple metrics in a radar chart format.
        """
        from .visualizations import plot_department_radar
        plot_department_radar(self.data)

    # stopword mod functions

    def add_stopword(self, word):
        """
        Add a single word to the stopword set.
        
        Args:
            word (str): Word to be added to stopwords
        """
        word = word.strip().lower()
        self.stop_words.add(word)

    def remove_stopword(self, word):
        """
        Remove a single word from the stopword set if it exists.
        
        Args:
            word (str): Word to be removed from stopwords
        """
        word = word.strip().lower()
        self.stop_words.discard(word)

    def update_stopwords(self, word_list, action="add"):
        """
        Add or remove a list of stopwords.
        
        Args:
            word_list (list): List of words to add/remove
            action (str): "add" to add words, "remove" to remove words
            
        Raises:
            ValueError: If action is not 'add' or 'remove'
        """
        for word in word_list:
            if action == "add":
                self.add_stopword(word)
            elif action == "remove":
                self.remove_stopword(word)
            else:
                raise ValueError("action must be 'add' or 'remove'")
            
    def save_stopwords(self, outfile="data/stopwords.txt"):
        """
        Save the current set of stopwords to a file.
        
        Args:
            outfile (str, optional): Path to save the stopwords file. 
                                    Defaults to "data/stopwords.txt".
        """
        with open(outfile, "w", encoding="utf-8") as f:
            for word in sorted(self.stop_words):
                f.write(word + "\n")



