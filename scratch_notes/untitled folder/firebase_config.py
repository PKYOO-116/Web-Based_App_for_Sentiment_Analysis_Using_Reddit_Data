import firebase_admin
from firebase_admin import credentials, db


def firebase_apps():
    cred_paths = {
        0: 'service_accounts/paul_service_account.json',
        1: 'service_accounts/armand_service_account.json',
        2: 'service_accounts/joshua_service_account.json',
        3: 'service_accounts/replication_service_account.json'
    }

    firebase_urls = {
        0: 'https://dsci551-db-team67-default-rtdb.firebaseio.com/',
        1: 'https://dsci551-team67-armand-default-rtdb.firebaseio.com/',
        2: 'https://dsci551-team67-default-rtdb.firebaseio.com/',
        3: 'https://dsci551-team67-replica-default-rtdb.firebaseio.com/'
    }

    firebase_apps = {}
    for index, cred_path in cred_paths.items():
        cred = credentials.Certificate(cred_path)
        firebase_apps[index] = firebase_admin.initialize_app(cred, {
            'databaseURL': firebase_urls[index]
        }, name=f'db{index + 1}')

    return firebase_apps


def databases():
    databases = {
        "database1": db.reference('/', app=firebase_admin.get_app('db1')),
        "database2": db.reference('/', app=firebase_admin.get_app('db2')),
        "database3": db.reference('/', app=firebase_admin.get_app('db3')),
        "database4": db.reference('/', app=firebase_admin.get_app('db4'))
    }

    return databases
