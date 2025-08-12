import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import json
from datetime import datetime, timedelta
import time
import os
import pickle  # For saving and loading the persistent count


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
    today = datetime.now().strftime('%m%d%Y')
    if os.path.exists(count_file_path):
        with open(count_file_path, 'rb') as file:
            last_date, count = pickle.load(file)
            if last_date == today:
                return count
    return 1  # Reset or initialize


def update_count(count):
    today = datetime.now().strftime('%m%d%Y')
    with open(count_file_path, 'wb') as file:
        pickle.dump((today, count), file)


def hash_index(text):
    return sum(ord(c) for c in text) % (NUM_DATABASES - 1)


def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    return score['compound']


def fetch_comments(subreddit_names, keywords, max_comments):
    start_time = datetime.now()
    time_limit = timedelta(minutes=3)
    count = load_or_initialize_count()
    submissions = {'submission': {}}
    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)
        for submission in subreddit.hot(limit=100):  # Adjust the limit as necessary
            if any(keyword.lower() in submission.title.lower() for keyword in keywords):
                submission.comments.replace_more(limit=0)  # Load all comments
                for comment in submission.comments.list():
                    if len(submissions['submission']) >= max_comments or datetime.now() - start_time > time_limit:
                        print(f"Extraction ended. {len(submissions['submission'])} comments extracted.")
                        print("Now executing the data save process.")
                        update_count(count)
                        return submissions
                    if comment.id not in submissions['submission']:
                        submissions['submission'][comment.id] = {
                            'secondary_data_id': datetime.now().strftime('%m%d%Y')
                                                 + f'_{len(submissions["submission"]) + 1:03}',
                            'body': comment.body,
                            'title': submission.title,
                            'subreddit': subreddit_name,
                            'upvotes': comment.ups,
                            'downvotes': comment.downs,
                            'timestamp': comment.created_utc,
                            'permalink': f'https://reddit.com{comment.permalink}',
                            'sentiment_score': analyze_sentiment(comment.body),
                            'hash_index': hash_index(comment.body)
                        }
                        count += 1
    print(f"Extraction ended. {len(submissions['submission'])} comments extracted.")
    print("Now executing the data save process.")
    update_count(count)
    return submissions


def save_to_files(comments):
    for id, data_dict in comments['submission'].items():
        index = data_dict['hash_index']
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

    print(f"Data saving completed. Total {len(comments['submission'])} comments saved across databases.")


if __name__ == "__main__":
    subreddits = input("Would you want to specify the subreddit?: ").split(',')
    keywords = input("Any keywords for searching?: ").split(',')
    max_comments = int(input("How many searches do I execute? Please enter number only.:"))
    print(f"Search for {max_comments} reddit comments.")
    comments = fetch_comments(subreddits, keywords, max_comments)
    save_to_files(comments)
    print(f"Operation completed. {len(comments['submission'])} comments were found and processed.")
