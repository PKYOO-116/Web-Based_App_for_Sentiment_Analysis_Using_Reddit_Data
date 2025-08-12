import firebase_admin
from firebase_admin import credentials, db

# Store the initialized apps in a global dictionary to avoid re-initialization
initialized_apps = {}

def initialize_apps():
    global initialized_apps
    apps_config = {
        'db1': {
            'cred_path': 'Firebase_Credentials/reddit-01-66725-firebase-adminsdk-lz9a1-2f248e3764.json',
            'firebase_url': 'https://reddit-01-66725-default-rtdb.firebaseio.com/'
        },
        'db2': {
            'cred_path': 'Firebase_Credentials/reddit-02-aaa4b-firebase-adminsdk-j5jd0-fe92801ba2.json',
            'firebase_url': 'https://reddit-02-aaa4b-default-rtdb.firebaseio.com/'
        },
        'db3': {
            'cred_path': 'Firebase_Credentials/reddit-03-firebase-adminsdk-5b5v6-21dfa82d27.json',
            'firebase_url': 'https://reddit-03-default-rtdb.firebaseio.com/'
        },
        'db4': {
            'cred_path': 'Firebase_Credentials/reddit-04-firebase-adminsdk-8ejxe-96f77d6b57.json',
            'firebase_url': 'https://reddit-04-default-rtdb.firebaseio.com/'
        }
    }

    for app_name, config in apps_config.items():
        if app_name not in firebase_admin._apps:
            cred = credentials.Certificate(config['cred_path'])
            firebase_admin.initialize_app(cred, {
                'databaseURL': config['firebase_url']
            }, name=app_name)
            print(f'Firebase app {app_name} initialized successfully')  # Logging the initialization

def get_databases():
    # Assuming apps have been initialized
    return {
        "database1": db.reference('/', app=firebase_admin.get_app('db1')),
        "database2": db.reference('/', app=firebase_admin.get_app('db2')),
        "database3": db.reference('/', app=firebase_admin.get_app('db3')),
        "database4": db.reference('/', app=firebase_admin.get_app('db4'))
    }

initialize_apps()
db_dict = get_databases()