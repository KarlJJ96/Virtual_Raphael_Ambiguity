# -*- coding: utf-8 -*-
"""Virtual Raphael Ambiguity Syntactic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gueAPbmF6Liv5MCbHTMk-RZy6IdaX3Tv
"""

import spacy

def detect_subordinate_clauses(doc):
    subordinate_clauses = 0
    for token in doc:
        if token.dep_ in ["mark", "advcl", "acl"]:
            subordinate_clauses += 1
    return subordinate_clauses

def detect_prepositional_phrase_attachment_ambiguities(doc):
    potential_ambiguities = []
    for token in doc:
        if token.pos_ == "ADP":
            prev_token_1 = token.head
            prev_token_2 = prev_token_1.head if prev_token_1.dep_ != "ROOT" else None
            if prev_token_2 and prev_token_1.dep_ != "ROOT":
                potential_ambiguities.append(token)
    return potential_ambiguities

def analyze_sentences(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        subordinate_clauses = detect_subordinate_clauses(sent)
        prepositional_phrase_ambiguities = detect_prepositional_phrase_attachment_ambiguities(sent)

        if subordinate_clauses > 2 or prepositional_phrase_ambiguities:
            ambiguous_sentences.append(sent.text)

    return ambiguous_sentences

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_output_file(sentences, output_path):
    with open(output_path, 'w') as file:
        for sentence in sentences:
            file.write(sentence + "\n")

def main(input_file, output_file):
    text = read_input_file(input_file)
    ambiguous_sentences = analyze_sentences(text)
    write_output_file(ambiguous_sentences, output_file)
    print(f"Potentially ambiguous sentences have been written to {output_file}")

if __name__ == "__main__":
    input_file = "your_file.txt"
    output_file = "Potentially Ambiguous Sentences.txt"
    main(input_file, output_file)