from firebase_admin import db
from api.firebase_config import firebase_apps

firebase_apps = firebase_apps()

for index, app in firebase_apps.items():
    ref = db.reference('submissions', app=app)
    snapshot = ref.get()
    num_rows = len(snapshot) if snapshot else 0

    index += 1
    print(f"Data rows in the Database{index}:", num_rows)
