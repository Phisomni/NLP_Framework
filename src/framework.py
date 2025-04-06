# src/framework.py

from collections import defaultdict
from .preprocessors import default_parser
import os

class TextAnalysisFramework:
    def __init__(self):
        self.stop_words = set()
        self.data = defaultdict(dict)
        self.raw_texts = {}

    def load_stop_words(self, stopfile):
        with open(stopfile, 'r') as f:
            self.stop_words = set(word.strip().lower() for word in f.readlines())

    def load_text(self, filename, label=None, parser=None):
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

    def wordcount_sankey(self, word_list=None, k=5):
        from .visualizations import plot_sankey
        plot_sankey(self.data["word_count"], word_list, k)

    def your_second_visualization(self):
        from .visualizations import plot_wordcount_subplots
        plot_wordcount_subplots(self.data["word_count"])

    def your_third_visualization(self):
        from .visualizations import plot_comparative_readability
        plot_comparative_readability(self.data.get("readability", {}))
