import os
import json
import re
from tqdm import tqdm
import nltk
from nltk.corpus import wordnet

# Download WordNet data
nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Example terms to align
terms_to_align = ["dataset", "benchmark", "model", "algorithm"]

# Create the alignment dictionary
alignment_dict = {}
for term in terms_to_align:
    synonyms = get_synonyms(term)
    for synonym in synonyms:
        alignment_dict[synonym] = term

def align_terms(input_folder, output_file):
    aligned_names = {}
    aligned_values = {}
    aligned_metrics = {}

    for json_file in tqdm(os.listdir(input_folder), desc="Aligning terms"):
        input_file_path = os.path.join(input_folder, json_file)
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract paper_id and table_id from the file name
        file_name_parts = json_file.replace("_claims.json", "").split("_")
        paper_id = file_name_parts[0]
        table_id = file_name_parts[1]

        for claim_id, claim in data.items():
            for spec_id, spec in claim.get("specifications", {}).items():
                name = spec.get("name")
                value = spec.get("value")

                # Align names using the dictionary
                aligned_name = alignment_dict.get(name.lower(), name)
                if aligned_name not in aligned_names:
                    aligned_names[aligned_name] = []
                aligned_names[aligned_name].append(f"{paper_id}_{table_id}_{claim_id}_{spec_id}")

                # Align values using the dictionary
                aligned_value = alignment_dict.get(value.lower(), value)
                if aligned_value not in aligned_values:
                    aligned_values[aligned_value] = []
                aligned_values[aligned_value].append(f"{paper_id}_{table_id}_{claim_id}_{spec_id}")

            # Align metrics
            measure = claim.get("Measure")
            if measure:
                aligned_measure = alignment_dict.get(measure.lower(), measure)
                if aligned_measure not in aligned_metrics:
                    aligned_metrics[aligned_measure] = []
                aligned_metrics[aligned_measure].append(f"{paper_id}_{table_id}_{claim_id}")

    # Check if the output file already exists
    output_folder = os.path.dirname(output_file)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save aligned terms to a new JSON file
    aligned_terms = {
        "aligned_names": aligned_names,
        "aligned_values": aligned_values,
        "aligned_metrics": aligned_metrics
    }

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(aligned_terms, file, indent=4)

# Define the input folder containing the JSON files and the output file name
input_folder = "data/claims/json"
output_file = "data/alignment_with_dictionary/VULTURII_ALIGNMENT.JSON"

# Run the alignment
align_terms(input_folder, output_file)
