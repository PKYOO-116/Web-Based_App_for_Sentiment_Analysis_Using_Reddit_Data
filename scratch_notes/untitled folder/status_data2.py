from firebase_config import databases

all_databases = databases()

for db_name, db_ref in all_databases.items():
    ref = db_ref.child('submissions')  # Assuming 'submissions' child exists
    snapshot = ref.get()
    num_rows = len(snapshot) if snapshot else 0

    print(f"Data rows in {db_name}:", num_rows)
