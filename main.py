from src.framework import TextAnalysisFramework
from src.pdf_utils import extract_text_from_pdf
import os
import matplotlib
matplotlib.use("TkAgg")

def main():
    # initialize framework
    framework = TextAnalysisFramework()
    
    # load stop words
    framework.load_stop_words("data/stopwords.txt")
    extra_stopwords = ["nupath", "attributes", "offers", "cs", "ge", "math", "phil", 
                       "psyc", "chem", "engw", "engl", "hist", "musc", "pols", "jrnl", 
                       "may", "fina", "nsrg", "musi"]
    framework.update_stopwords(extra_stopwords, action="add")
    
    # loop through all PDFs in data/raw_pdfs
    pdf_dir = "data/raw_pdfs"
    raw_txt_dir = "data/raw"
    os.makedirs(raw_txt_dir, exist_ok=True)

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)

            # use file name w/o extension as label
            label = os.path.splitext(filename)[0]

            # extract and save text
            print(f"Processing: {label}")
            raw_text = extract_text_from_pdf(pdf_path)
            text_file = os.path.join(raw_txt_dir, f"{label}.txt")

            with open(text_file, "w", encoding="utf-8") as f:
                f.write(raw_text)

            # load into framework
            framework.load_text(text_file, label=label)
    
    # run visualizations after all files are loaded
    word_list = ["ethics", "world", "culture", "technology", "innovation",
                "politics", "data", "new", "impact", "rights", "research", 
                "experiential", "industry"]

    cluster_map = {
    "Philosophy and Religion": "Humanities",
    "English": "Humanities",
    "History": "Humanities",
    "Political Science": "Social Sciences",
    "Psychology": "Social Sciences",
    "School of Journalism": "Social Sciences",
    "Music": "Arts",
    "School of Nursing": "STEM",
    "Chemistry and Chemical Biology": "STEM",
    "Mathematics": "STEM",
    "Computer Science": "STEM",
    "Business": "Professional"
    }   

    cluster_colors = {
    "Humanities": "salmon",
    "Social Sciences": "lightblue",
    "Arts": "orchid",
    "STEM": "lightseagreen",
    "Professional": "gold",
    "Other": "gray"
    }

    framework.wordcount_sankey(word_list=word_list,
                                cluster_map=cluster_map,
                                cluster_colors=cluster_colors)
    framework.top_word_subplots()
    framework.readability_bar()
    framework.sentiment_bar()
    framework.radar()

if __name__ == "__main__":
    main()
