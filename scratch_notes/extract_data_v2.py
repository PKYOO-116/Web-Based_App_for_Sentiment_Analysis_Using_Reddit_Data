import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json
from datetime import datetime, timedelta, timezone
import os
import pickle  # For saving and loading the persistent count
from firebase_config import get_databases

# Initialize sentiment analyzer
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# Initialize Reddit API with given credentials
reddit = praw.Reddit(
    client_id='gxUTrYGyJ8Y2NntR5kOZQA',
    client_secret='dlsKv6hx2KUOvRvZzvxroSOmzOE84g',
    user_agent='sentiment analysis for upcoming election'
)

# Specify the directory to save JSON and CSV files
save_directory = "../DBdata/"
count_file_path = os.path.join(save_directory, "count.pkl")
NUM_DATABASES = 4

def load_or_initialize_count():
    today = datetime.now().strftime('%Y%m%d')
    if os.path.exists(count_file_path):
        with open(count_file_path, 'rb') as file:
            last_date, count = pickle.load(file)
            if last_date == today:
                return count
    return 1

def update_count(count):
    today = datetime.now().strftime('%Y%m%d')
    with open(count_file_path, 'wb') as file:
        pickle.dump((today, count), file)


def hash_index(firebase_id):
    return sum(ord(c) for c in firebase_id) % (NUM_DATABASES - 1)


def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores['compound']


def fetch_comments(subreddit_names, keywords, max_comments):
    start_time = datetime.now()
    time_limit = timedelta(minutes=3)
    count = load_or_initialize_count()
    key = ', '.join(keywords)
    submissions = {'comments': {}}

    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=100):
            if any(keyword.lower() in submission.title.lower() for keyword in keywords):
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if len(submissions['comments']) >= max_comments or datetime.now() - start_time > time_limit:
                        print(f"Extraction ended. {len(submissions['comments'])} comments extracted.")
                        print("Now executing the data save process.")
                        update_count(count)
                        return submissions
                    if comment.id not in submissions['comments']:
                        firebase_id = f"{submission.id}-{comment.id}"  # Generate Firebase ID
                        submissions['comments'][comment.id] = {
                            'id': comment.id,
                            'firebase_id': firebase_id,  # Save Firebase ID
                            'body': comment.body,
                            'title': submission.title,
                            'subreddit': subreddit_name,
                            'keywords': key,
                            'upvotes': comment.ups,
                            'downvotes': comment.downs,
                            'timestamp': datetime.fromtimestamp(
                                comment.created_utc, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                            'permalink': f'https://reddit.com{comment.permalink}',
                            'sentiment_score': analyze_sentiment(comment.body)
                        }
                        count += 1
    print(f"Extraction ended. {len(submissions['comments'])} comments extracted.")
    print("Now executing the data save process.")
    update_count(count)
    return submissions


def save_to_firebase(comments):
    # Assuming a function get_databases() returns a dictionary of database references
    dbs = get_databases()
    for id, data_dict in comments['comments'].items():
        db_index = hash_index(data_dict['firebase_id'])  # Use Firebase ID for hashing
        db_ref = dbs[f'database{db_index + 1}']  # Adjust the index to match your database naming

        db_ref.child('comments').child(data_dict['firebase_id']).update(data_dict)

        db_replica_ref = dbs[f'database4'] # replication save
        db_replica_ref.child('comments').child(data_dict['firebase_id']).update(data_dict)

    print(f"Data pushing completed. Total {len(comments['comments'])} comments saved in firebase databases.")


def save_to_files(comments):
    for id, data_dict in comments['comments'].items():
        index = hash_index(data_dict['firebase_id'])
        json_path = os.path.join(save_directory, f'database{index+1}.json')
        json_path_re = os.path.join(save_directory, 'database4.json')

        if os.path.exists(json_path_re):
            with open(json_path_re, 'r+') as file:
                existing_data = json.load(file)
                existing_data.update(comments)
                file.seek(0)
                file.truncate()
                json.dump(existing_data, file, indent=4)
        else:
            with open(json_path_re, 'w') as file:
                json.dump(comments, file, indent=4)

        if os.path.exists(json_path):
            with open(json_path, 'r+') as file:
                existing_data = json.load(file)
                existing_data.update(comments)
                file.seek(0)
                file.truncate()
                json.dump(existing_data, file, indent=4)
        else:
            with open(json_path, 'w') as file:
                json.dump(comments, file, indent=4)

    print(f"Data saving completed. Total {len(comments['comments'])} comments saved locally.")


if __name__ == "__main__":
    subreddits = input("Would you want to specify the subreddit?: ").split(',')
    keywords = input("Any keywords for searching?: ").split(',')
    max_comments = int(input("How many searches do I execute? Please enter number only.:"))
    print(f"Search for {max_comments} reddit comments.")
    comments = fetch_comments(subreddits, keywords, max_comments)
    save_to_files(comments)
    save_to_firebase(comments)
    print(f"Operation completed. {len(comments['comments'])} comments were found and processed.")