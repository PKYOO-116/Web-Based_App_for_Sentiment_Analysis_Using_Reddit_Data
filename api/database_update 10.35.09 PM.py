import json
from firebase_config import initialize_apps  # Import the initialization function
from firebase_admin import db


def upload_data_to_firebase(data, app):
    """ Uploads data to the specified Firebase database under a unique node. """
    ref = db.reference('/comments', app=app)
    ref.push(data)  # Use push to add data without overwriting existing data


def read_data_from_json(file_path):
    """ Reads data from a JSON file. """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


# Initialize Firebase apps using the imported function
firebase_apps = initialize_apps()

# Load data from JSON file
data_path = 'path/to/your/database0.json'  # Update this path as necessary
comments_data = read_data_from_json(data_path)

# Define which Firebase app to use based on hash_index, replicate to the last database
for comment in comments_data:
    # Use hash_index to determine the Firebase app, assuming 0 to N-1 are hash-based apps and N is the replication app
    hash_index = comment["hash_index"]
    main_app_name = f'db{hash_index}'  # This assumes hash_index is directly mapped to the db names like db0, db1, etc.
    replication_app_name = 'dbN'  # Change 'dbN' to your actual replication database name, e.g., 'db4'

    # Upload data to the main database based on hash index
    if main_app_name in firebase_apps:
        upload_data_to_firebase(comment, firebase_apps[main_app_name])

    # Also replicate the data to the last database
    if replication_app_name in firebase_apps:
        upload_data_to_firebase(comment, firebase_apps[replication_app_name])
