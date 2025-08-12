import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
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
count_file_path = os.path.join("count.pkl")
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
    return sum(ord(c) for c in firebase_id) % NUM_DATABASES

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    return scores['compound']

def fetch_comments(subreddit_names, keywords, max_comments, processed_ids):
    comments = []
    start_time = datetime.now()
    time_limit = timedelta(minutes=10)
    count = load_or_initialize_count()

    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=100):
            if any(keyword.lower() in submission.title.lower() for keyword in keywords):
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if len(comments) >= max_comments or datetime.now() - start_time > time_limit:
                        return comments
                    if comment.id not in processed_ids:
                        processed_ids.add(comment.id)
                        sentiment_score = analyze_sentiment(comment.body)
                        comments.append({
                            'id': comment.id,
                            'body': comment.body,
                            'title': submission.title,
                            'subreddit': subreddit_name,
                            'upvotes': comment.ups,
                            'downvotes': comment.downs,
                            'timestamp': datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                            'permalink': f'https://reddit.com{comment.permalink}',
                            'sentiment_score': sentiment_score
                        })
                        count += 1
    update_count(count)
    return comments

def save_to_firebase(comments):
    dbs = get_databases()
    for comment in comments:
        db_ref = dbs['database1'].child('comments').push(comment)  # Temporarily save in database1
        firebase_id = db_ref.key  # Retrieve Firebase ID after insert
        db_index = hash_index(firebase_id)  # Hash based on Firebase ID
        correct_db_ref = dbs[f'database{db_index + 1}']  # Get the correct database reference
        comment['firebase_id'] = firebase_id
        correct_db_ref.child('comments').child(firebase_id).set(comment)  # Save comment in the correct database
        print(f"Comment inserted with Firebase ID: {firebase_id} in database{db_index + 1}")

if __name__ == "__main__":
    processed_ids = set()
    subreddits = input("Enter comma-separated subreddit names: ").split(',')
    keywords = input("Enter comma-separated keywords: ").split(',')
    max_comments = int(input("Enter the maximum number of comments to process: "))
    comments = fetch_comments([sub.strip() for sub in subreddits], [kw.strip() for kw in keywords], max_comments, processed_ids)
    save_to_firebase(comments)
    print(f"Operation completed. {len(comments)} comments were found and processed.")
