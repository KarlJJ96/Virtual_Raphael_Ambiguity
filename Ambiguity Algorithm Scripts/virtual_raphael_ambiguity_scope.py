# -*- coding: utf-8 -*-
"""Virtual Raphael Ambiguity Scope.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wy7HHyLHQFuYqOkID8zGbgTITu3_Cy6D
"""

import spacy

def detect_scope_ambiguity(doc):
    for token in doc:
        if token.pos_ == "VERB":
            has_direct_object = any(child.dep_ == "dobj" for child in token.children)
            if not has_direct_object:
                return True
    return False

def analyze_sentences(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    ambiguous_sentences = []

    for sent in doc.sents:
        has_scope_ambiguity = detect_scope_ambiguity(sent)

        if has_scope_ambiguity:
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