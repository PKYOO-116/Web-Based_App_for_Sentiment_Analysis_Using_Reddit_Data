from firebase_config import get_databases

def wipe_databases():
    dbs = get_databases()  # This should return a dictionary
    for db_key, ref in dbs.items():
        print(f"Deleting all data in {db_key}...")
        ref.child('comments').delete()  # Assumes 'comments' is the node to wipe
        print(f"All data in {db_key} has been wiped.")

if __name__ == "__main__":
    confirm = input("Are you sure you want to DELETE ALL DATA from all databases? This operation cannot be undone. Type 'yes' to confirm: ")
    if confirm.lower() == 'yes':
        wipe_databases()
        print("Data deletion completed.")
    else:
        print("Data deletion aborted.")