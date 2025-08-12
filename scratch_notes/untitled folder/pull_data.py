import praw
from firebase_admin import db
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_config import initialize_apps

NUM_DATABASES = 4
data_bundle_num = 1

# Initialize Reddit API with praw
reddit = praw.Reddit(
    client_id='gxUTrYGyJ8Y2NntR5kOZQA',
    client_secret='dlsKv6hx2KUOvRvZzvxroSOmzOE84g',
    user_agent='sentiment analysis for upcoming election'
)

subreddit = reddit.subreddit('politics')
keywords = ['election', 'vote', 'trump', 'biden']

# Initialize Firebase apps
firebase_apps = initialize_apps()

def hash_db_index(text):
    # Hash function to decide which database to use
    return sum(ord(c) for c in text) % (NUM_DATABASES - 1)

def add_submission_to_firebase(submission, apps):
    # Convert the submission's creation time from Unix timestamp to a readable datetime
    submission_date = datetime.utcfromtimestamp(submission.created_utc)
    index = hash_db_index(submission.title)
    print(f'Title: {submission.title}, DB Index: {index}')

    added_to_replica = False
    app = apps[f'db{index + 1}']
    ref = db.reference('submissions', app=app)

    submission_key = submission.id
    submission_date_str = submission_date.strftime('%Y-%m-%d %H:%M:%S')
    data_bundle_id = datetime.now().strftime('%Y%m%d_') + str(data_bundle_num)

    if not ref.child(submission_key).get():
        ref.child(submission_key).set({
            'title': submission.body,
            'url': submission.url,
            'score': submission.score,
            'date': submission_date_str,
            'collection id': data_bundle_id,
            'database number': index + 1
        })
        added_to_replica = True

    # Handle replica database separately
    replica_app = apps['db4']
    replica_ref = db.reference('submissions', app=replica_app)
    if not replica_ref.child(submission_key).get():
        replica_ref.child(submission_key).set({
            'title': submission.title,
            'url': submission.url,
            'score': submission.score,
            'date': submission_date_str,
            'collection id': data_bundle_id,
            'database number': index + 1
        })
        added_to_replica = True

    return added_to_replica

# Main execution block
if __name__ == "__main__":
    count = 0
    while True:
        num_limit = input("How many searches do I execute? Please enter number only: ")
        try:
            num_limit = int(num_limit)
            print(f"Search for {num_limit} reddit posts.")
            break
        except ValueError:
            print("Please enter a valid number.")

    for keyword in keywords:
        for submission in subreddit.search(keyword, limit=num_limit):
            if add_submission_to_firebase(submission, firebase_apps):
                count += 1
                data_bundle_num += 1

    print(f"Total of {count} submissions added.")
