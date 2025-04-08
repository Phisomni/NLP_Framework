from pdfminer.high_level import extract_text
import os
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_text_from_pdf(filepath):
    """
    Extracts raw text from a PDF using pdfminer.
    
    Args:
        filepath (str): Path to the PDF file.

    Returns:
        str: Extracted plain text.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"No such file: {filepath}")
    return extract_text(filepath)
