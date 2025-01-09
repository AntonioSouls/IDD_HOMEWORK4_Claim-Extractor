import pandas as pd
import json
import os

def create_profiling(data):
    all_entries_name = []
    all_entries_value = []
    all_entries_metric = []
    profiling_df_dict = {}

    # Claims extractions
    for key, row in data.items():
        for spec_key, spec in row['specifications'].items():
            all_entries_name.append({'Key': spec['name'], 'Count': 1})
            all_entries_value.append({'Key': spec['name'] + "::" + spec['value'], 'Count': 1})
        all_entries_metric.append({'Key': row['Measure'], 'Count': 1})

    profiling_df_name = pd.DataFrame(all_entries_name)
    profiling_df_value = pd.DataFrame(all_entries_value)
    profiling_df_metric = pd.DataFrame(all_entries_metric)
    
    # Group-by to manage duplicate
    profiling_df_dict['name'] = (profiling_df_name.groupby('Key').sum().reset_index())
    profiling_df_dict['value'] = (profiling_df_value.groupby('Key').sum().reset_index())
    profiling_df_dict['metric'] = (profiling_df_metric.groupby('Key').sum().reset_index())

    return profiling_df_dict

def load_all_claims(directory_path):
    all_claims = [] 

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_claims.append(data) 
    return all_claims

def create_profiling_spreadsheet():
    try:
        folder_exists = os.path.exists('data/profiling')
        if not folder_exists:
            os.makedirs('data/profiling')
            print(f"\033[32mCreated directory: {'data/profiling'}\033[0m\n")

        # Load all claims
        all_claims = load_all_claims('data/claims/json')

        # Flatten the list of dictionaries
        flattened_data = {k: v for d in all_claims for k, v in d.items()}

        # Create profiling with pre-aligned values
        profiling_df_dict = create_profiling(flattened_data)

        for key in profiling_df_dict:
            filename = 'data/profiling/' + key.upper() + '_PROFILING.csv'
            profiling_df_dict[key].to_csv(filename, index=False)
            print(f"- \033[32mProfiling CSV file saved as {filename}\033[0m\n")

    except Exception as e:
        print(f"\033[31mError during the process: {e}\033[0m\n")