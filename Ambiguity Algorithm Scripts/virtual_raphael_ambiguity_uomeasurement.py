# -*- coding: utf-8 -*-
"""Virtual Raphael Ambiguity UoMeasurement.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jNEEeIh4iWRpCpNjmloIOXyLvrUEXBjC
"""

import re
import spacy

# Define measurement units
units = {
    "length": {
        "metric": ["nm", "µm", "mm", "cm", "m", "km"],
        "imperial": ["inch", "inches", "ft", "feet", "yard", "yards", "mile", "miles"]
    },
    "weight": {
        "metric": ["ng", "µg", "mg", "g", "kg", "tonne"],
        "imperial": ["oz", "lb", "stone", "ton"]
    },
    "volume": {
        "metric": ["nl", "µl", "ml", "l", "m3"],
        "imperial": ["fl oz", "cup", "pint", "quart", "gallon", "gallons"]
    },
    "temperature": {
        "metric": ["C", "Celsius", "K", "Kelvin"],
        "imperial": ["F", "Fahrenheit"]
    },
    "pressure": {
        "metric": ["Pa", "kPa", "MPa", "bar"],
        "imperial": ["psi", "atm"]
    },
    "concentration": {
        "ppm": ["ppm"],
        "ppb": ["ppb"],
        "molar": ["M", "mol/L"],
        "others": ["mg/L", "ug/L"]
    },
    "time": {
        "metric": ["ns", "µs", "ms", "s", "min", "h", "hr", "day", "week", "month", "year"],
        "imperial": ["second", "minute", "hour", "day", "week", "month", "year"]
    },
    "flow rate": {
        "metric": ["nl/s", "µl/s", "ml/s", "l/s", "m3/s"],
        "imperial": ["cfm", "gpm"]
    },
    "viscosity": {
        "metric": ["cP", "mPa.s"],
        "imperial": ["P", "lb/ft.s"]
    },
    "voltage": {
        "metric": ["mV", "V", "kV"],
        "imperial": ["volt"]
    },
    "current": {
        "metric": ["µA", "mA", "A"],
        "imperial": ["amp"]
    },
    "resistance": {
        "metric": ["mΩ", "Ω", "kΩ", "MΩ"],
        "imperial": ["ohm"]
    },
    "torque": {
        "metric": ["Nm"],
        "imperial": ["lb.ft"]
    },
    "speed": {
        "metric": ["rpm", "m/s", "km/h"],
        "imperial": ["mph", "ft/s"]
    },
    "humidity": {
        "metric": ["%RH"]
    },
    "light": {
        "metric": ["lux", "lm"],
        "imperial": ["foot-candle"]
    },
    "noise": {
        "metric": ["dB"]
    },
    "force": {
        "metric": ["N", "kN"],
        "imperial": ["lbf"]
    },
    "vibration": {
        "metric": ["mm/s", "in/s"]
    }
}

all_units = [unit for measure in units.values() for system in measure.values() for unit in system]

# Define regex patterns
number_pattern = re.compile(r'\b\d+(\.\d+)?\b')
unit_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(unit) for unit in all_units) + r')\b')

def detect_units_inconsistency(doc):
    used_units = {measure: {system: set() for system in measure} for measure in units}

    for token in doc:
        token_text = token.text.lower()
        for measure, systems in units.items():
            for system, unit_list in systems.items():
                if token_text in unit_list:
                    used_units[measure][system].add(token_text)

    inconsistencies = []
    for measure, systems in used_units.items():
        if len([system for system in systems.values() if system]) > 1:
            for system_units in systems.values():
                inconsistencies.extend(system_units)

    return inconsistencies

def detect_numbers_without_units(doc):
    sentences_with_issues = []

    for sent in doc.sents:
        numbers_in_sent = number_pattern.findall(sent.text)
        units_in_sent = unit_pattern.findall(sent.text)

        if numbers_in_sent and not units_in_sent:
            sentences_with_issues.append(sent.text)

    return sentences_with_issues

def analyze_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    inconsistencies = detect_units_inconsistency(doc)
    sentences_with_issues = detect_numbers_without_units(doc)

    return inconsistencies, sentences_with_issues

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_output_file(data, output_path):
    with open(output_path, 'w') as file:
        for item in data:
            file.write(item + "\n")

def main(input_file, output_file_inconsistencies, output_file_ambiguous):
    text = read_input_file(input_file)
    inconsistencies, sentences_with_issues = analyze_text(text)

    if inconsistencies:
        write_output_file(inconsistencies, output_file_inconsistencies)
        print(f"Inconsistent units have been written to {output_file_inconsistencies}")
    else:
        print("No inconsistencies found in unit usage.")

    if sentences_with_issues:
        write_output_file(sentences_with_issues, output_file_ambiguous)
        print(f"Potentially ambiguous sentences have been written to {output_file_ambiguous}")
    else:
        print("No potentially ambiguous sentences found.")

if __name__ == "__main__":
    input_file = "your_file.txt"
    output_file_inconsistencies = "Inconsistent Use of Units.txt"
    output_file_ambiguous = "Potentially Ambiguous Sentences.txt"
    main(input_file, output_file_inconsistencies, output_file_ambiguous)