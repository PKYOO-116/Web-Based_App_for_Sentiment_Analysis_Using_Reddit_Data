import json
import os
import pandas as pd
from api.firebase_config import firebase_apps, databases

firebase_apps = firebase_apps()
databases = databases()

data_directory = "DBdata"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)


def is_data_updated(existing_data, new_data):
    return existing_data != new_data


def save_data_in_formats(db_name, reference):
    new_data = reference.get()
    json_file_path = os.path.join(data_directory, f"{db_name}.json")
    csv_file_path = os.path.join(data_directory, f"{db_name}.csv")

    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    if is_data_updated(existing_data, new_data):
        with open(json_file_path, 'w') as json_file:
            json.dump(new_data, json_file, indent=4)
        print(f"Updated {db_name} data in JSON format.")

        if new_data and 'submissions' in new_data:
            flattened_data = [value for key, value in new_data['submissions'].items()]
            df = pd.DataFrame(flattened_data)
        else:
            df = pd.DataFrame()
        df.to_csv(csv_file_path, index=False)
        print(f"Updated {db_name} data in CSV format.")
    else:
        print(f"No update needed for {db_name}. Data is already up-to-date.")


for db_name, ref in databases.items():
    save_data_in_formats(db_name, ref)
