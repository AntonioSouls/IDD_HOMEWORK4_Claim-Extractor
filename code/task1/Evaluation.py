import os
import json

def load_claims(directory):
    claims = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                claims_dict = json.load(file)
                claims.extend(claims_dict.values())
    return claims

def dict_to_tuple(d):
    if isinstance(d, dict):
        return tuple((k, dict_to_tuple(v)) for k, v in d.items())
    if isinstance(d, list):
        return tuple(dict_to_tuple(v) for v in d)
    return d

def compare_claims(gt_claims, pred_claims):
    gt_claims_set = {dict_to_tuple(claim) for claim in gt_claims}
    pred_claims_set = {dict_to_tuple(claim) for claim in pred_claims}

    true_positives = len(gt_claims_set & pred_claims_set)
    false_positives = len(pred_claims_set - gt_claims_set)
    false_negatives = len(gt_claims_set - pred_claims_set)

    return true_positives, false_positives, false_negatives

def calculate_precision_recall_f1(true_positives, false_positives, false_negatives):
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

# Carica i claims dalle directory specificate
gt_claims = load_claims('data/ground_truth_claims')
pred_claims = load_claims('data/claims/json')

# Confronta i claims e calcola le metriche
true_positives, false_positives, false_negatives = compare_claims(gt_claims, pred_claims)
precision, recall, f1_score = calculate_precision_recall_f1(true_positives, false_positives, false_negatives)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1_score}")
