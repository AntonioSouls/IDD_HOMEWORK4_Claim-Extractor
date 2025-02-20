import os
import json
import pandas as pd
from collections import defaultdict

def count_entries(data):
    name_counts = defaultdict(int)
    value_counts = defaultdict(int)
    measure_counts = defaultdict(int)
    
    def process_entry(entry):
        if 'specifications' in entry:
            for spec_key, spec in entry['specifications'].items():
                name = spec['name']
                value = spec['value']
                name_counts[name] += 1
                value_counts[value] += 1
        
        if 'Measure' in entry:
            measure = entry['Measure']
            if measure:
                measure_counts[measure] += 1

    def process_data(data):
        for key, row in data.items():
            if isinstance(row, dict) and 'specifications' in row:
                process_entry(row)
            else:
                for subkey, subrow in row.items():
                    if isinstance(subrow, dict):
                        process_entry(subrow)

    process_data(data)
    return name_counts, value_counts, measure_counts

def load_and_count_all_claims(directory_path):
    total_name_counts = defaultdict(int)
    total_value_counts = defaultdict(int)
    total_measure_counts = defaultdict(int)

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                name_counts, value_counts, measure_counts = count_entries(data)
                for key, count in name_counts.items():
                    total_name_counts[key] += count
                for key, count in value_counts.items():
                    total_value_counts[key] += count
                for key, count in measure_counts.items():
                    total_measure_counts[key] += count

    return total_name_counts, total_value_counts, total_measure_counts

def save_profiling_to_csv(profiling_counts, filename):
    profiling_df = pd.DataFrame(list(profiling_counts.items()), columns=['Key', 'Count'])
    profiling_df.to_csv(filename, index=False)
    print(f"Profiling CSV file saved as {filename}")

def main():
    directory_path = 'data/claims/json'
    total_name_counts, total_value_counts, total_measure_counts = load_and_count_all_claims(directory_path)

    if not os.path.exists('data/profiling'):
        os.makedirs('data/profiling')
    
    save_profiling_to_csv(total_name_counts, 'data/profiling/NAME_PROFILING.csv')
    save_profiling_to_csv(total_value_counts, 'data/profiling/VALUE_PROFILING.csv')
    save_profiling_to_csv(total_measure_counts, 'data/profiling/METRIC_PROFILING.csv')

if __name__ == '__main__':
    main()
