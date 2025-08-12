import firebase_admin
from firebase_admin import credentials, db
from firebase_config import initialize_apps  # Import the initialization function

def count_data_entries(app):
    """ Counts the number of entries in the specified Firebase database. """
    ref = db.reference('/comments', app=app)  # Adjust this to the correct node if different
    data = ref.get()
    return len(data) if data else 0

# Initialize Firebase apps using the imported initialization function
firebase_apps = initialize_apps()

# Example usage: Print the count of entries in each database
for db_key, app in firebase_apps.items():
    num_entries = count_data_entries(app)
    print(f"Total number of comments collected so far in {db_key}: {num_entries}")
