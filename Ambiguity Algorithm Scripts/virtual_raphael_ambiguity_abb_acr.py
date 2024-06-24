# -*- coding: utf-8 -*-
"""Virtual Raphael Ambiguity Abb/Acr.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10zFLTHfulRtnnM8g8gggyV3qRQ_PtuHd
"""

import re
import spacy
import PyPDF2
import camelot

# Regex patterns for identifying abbreviations/acronyms and their definitions
abbreviation_pattern = re.compile(r'\b[A-Z]{2,5}\b')
definition_patterns = [
    re.compile(r'\b([A-Z]{2,5})\s*\(([^)]+)\)'),
    re.compile(r'\b([^)]+)\s*\(([A-Z]{2,5})\)'),
    re.compile(r'\b([A-Z]{2,5})\s*-\s*([^.\n]+)'),
    re.compile(r'\b([^.\n]+)\s*-\s*([A-Z]{2,5})')
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
    return text

def extract_tables_from_pdf(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='all')
    table_texts = []
    for table in tables:
        df = table.df
        table_text = df.to_string(header=False, index=False)
        table_texts.append(table_text)
    return table_texts

def find_abbreviations(text):
    return set(abbreviation_pattern.findall(text))

def verify_definitions(text, abbreviations):
    defined_abbreviations = set()
    for pattern in definition_patterns:
        for match in pattern.findall(text):
            defined_abbreviations.update(match)
    return abbreviations - defined_abbreviations

def analyze_text(text, table_texts):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    abbreviations = find_abbreviations(text)

    for table_text in table_texts:
        abbreviations.update(find_abbreviations(table_text))

    undefined_abbreviations = verify_definitions(text, abbreviations)

    for table_text in table_texts:
        undefined_abbreviations = verify_definitions(table_text, undefined_abbreviations)

    return undefined_abbreviations

def read_input_pdf(file_path):
    text = extract_text_from_pdf(file_path)
    tables = extract_tables_from_pdf(file_path)
    return text, tables

def write_output_file(data, output_path):
    with open(output_path, 'w') as file:
        for item in data:
            file.write(item + "\n")

def main(input_file, output_file):
    text, table_texts = read_input_pdf(input_file)
    undefined_abbreviations = analyze_text(text, table_texts)
    write_output_file(undefined_abbreviations, output_file)
    print(f"Undefined abbreviations and acronyms have been written to {output_file}")

if __name__ == "__main__":
    input_file = "your_file.pdf"
    output_file = "Undefined Abbreviations and Acronyms.txt"
    main(input_file, output_file)