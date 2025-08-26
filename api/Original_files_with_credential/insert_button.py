import firebase_admin
from firebase_admin import credentials, db

def hash_db_index(text):
    return sum(ord(c) for c in text) % 4
    
def initialize_apps():
    cred_paths = {
        0: 'Firebase_Credentials/reddit-01-66725-firebase-adminsdk-lz9a1-2f248e3764.json',
        1: 'Firebase_Credentials/reddit-02-aaa4b-firebase-adminsdk-j5jd0-fe92801ba2.json',
        2: 'Firebase_Credentials/reddit-03-firebase-adminsdk-5b5v6-21dfa82d27.json',
        3: 'Firebase_Credentials/reddit-04-firebase-adminsdk-8ejxe-96f77d6b57.json'
    }

    firebase_urls = {
        0: 'https://reddit-01-66725-default-rtdb.firebaseio.com/',
        1: 'https://reddit-02-aaa4b-default-rtdb.firebaseio.com/',
        2: 'https://reddit-03-default-rtdb.firebaseio.com/',
        3: 'https://reddit-04-default-rtdb.firebaseio.com/'
    }

    for index, cred_path in cred_paths.items():
        cred = credentials.Certificate(cred_path)
        app_name = f'db{index + 1}'
        # Check if the app has already been initialized
        if not firebase_admin._apps or app_name not in firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': firebase_urls[index]
            }, name=app_name)
            print(f'Firebase app {app_name} initialized successfully')  # Logging the initialization


def get_databases():
    databases = {
        "database1": db.reference('/', app=firebase_admin.get_app('db1')),
        "database2": db.reference('/', app=firebase_admin.get_app('db2')),
        "database3": db.reference('/', app=firebase_admin.get_app('db3')),
        "database4": db.reference('/', app=firebase_admin.get_app('db4'))
    }
    return databases

def insert_post(title, date, search_keyword, subreddit_name, content):
    # Determine the database index based on the title
    database_index = hash_db_index(title)
    
    # Get the reference to the appropriate database node
    db = get_databases()[f"database{database_index + 1}"]
    db_ref = db.child(f"submissions")
    
    # Generate a unique key for the submission
    submission_key = db_ref.push().key

    # Insert the post data into the Firebase Realtime Database
    db_ref.child(submission_key).set({
        'title': title,
        'date': date,
        'search_keyword': search_keyword,
        'subreddit_name': subreddit_name,
        'content': content
    })

    print(f"Post inserted with ID: {submission_key}")
