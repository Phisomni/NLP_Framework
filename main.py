# main.py

from src.framework import TextAnalysisFramework
from src.pdf_utils import extract_text_from_pdf
import os

def main():
    # Initialize framework
    framework = TextAnalysisFramework()

    # Load stop words
    framework.load_stop_words("data/stopwords.txt")

    # Loop through all PDFs in data/raw_pdfs
    pdf_dir = "data/raw_pdfs"
    raw_txt_dir = "data/raw"
    os.makedirs(raw_txt_dir, exist_ok=True)

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)

            # Use file name (minus extension) as label
            label = os.path.splitext(filename)[0]

            # Extract and save text
            print(f"Processing: {label}")
            raw_text = extract_text_from_pdf(pdf_path)
            text_file = os.path.join(raw_txt_dir, f"{label}.txt")

            with open(text_file, "w", encoding="utf-8") as f:
                f.write(raw_text)

            # Load into framework
            framework.load_text(text_file, label=label)

    # Run visualizations after all files are loaded
    framework.wordcount_sankey(k=10)
    framework.your_second_visualization()
    framework.your_third_visualization()

if __name__ == "__main__":
    main()
