from flask import Flask, jsonify, request
from firebase_config import initialize_apps, get_databases

app = Flask(__name__)

initialize_apps()

@app.before_request
def before_request():
    print("Received a request to:", request.url)

def hash_db_index(firebase_id):
    # Simple hash function based on the firebase_id
    return sum(ord(c) for c in firebase_id) % 4  # assuming you have four databases

def get_post_data(post_key):
    database_index = hash_db_index(post_key)
    db = get_databases()[f"database{database_index + 1}"]
    post_ref = db.child('comments').child(post_key)
    post = post_ref.get()
    if post:
        post['id'] = post_key  # Ensure to return the Firebase ID in the post data
        return post
    return None

@app.route('/api/posts/<post_key>', methods=['GET'])
def get_post(post_key):
    post_data = get_post_data(post_key)
    if post_data:
        return jsonify(post_data), 200
    else:
        return jsonify({"error": "Post not found"}), 404

@app.route('/api/posts', methods=['GET'])
def get_posts():
    all_posts = []
    found_posts = False  # Flag to check if posts are found

    # Assuming database names are 'database1', 'database2', 'database3', 'database4'
    # We will skip 'database4'
    databases = get_databases()

    # Iterate over each database and fetch posts, skipping the fourth database
    for db_name, ref in databases.items():
        if db_name == 'database4':  # Skip the fourth database
            continue

        try:
            posts = ref.child('comments').get()
            if posts:
                for post_id, post_data in posts.items():
                    post_data['id'] = post_id  # Include the Firebase ID in the post data
                    all_posts.append(post_data)
                found_posts = True
            print(f"Posts found in {db_name}: {bool(posts)}")  # Debugging output
        except Exception as e:
            print(f"Error fetching posts from {db_name}: {str(e)}")  # Handle potential errors gracefully

    if not found_posts:
        print("No posts found across all databases")  # More informative debugging output

    return jsonify(all_posts)

@app.errorhandler(403)
def custom_403_handler(error):
    return jsonify({"error": "Access forbidden", "message": str(error)}), 403

def insert_post(title, timestamp, subreddit, body):
    db = get_databases()['database1']  # default to database1 for initial insert
    new_post_ref = db.child('comments').push({
        'title': title,
        'timestamp': timestamp,  
        'subreddit': subreddit,
        'body': body
    })
    firebase_id = new_post_ref.key
    database_index = hash_db_index(firebase_id)
    db = get_databases()[f"database{database_index + 1}"]
    db.child('comments').child(firebase_id).set({
        'title': title,
        'timestamp': timestamp,  
        'subreddit': subreddit,
        'body': body,
        'firebase_id': firebase_id
    })
    print(f"Post inserted with ID: {firebase_id} in database{database_index + 1}")
    return firebase_id

@app.route('/api/posts', methods=['POST'])
def add_post():
    try:
        data = request.json
        title = data['title']
        timestamp = data['timestamp']
        subreddit = data['subreddit']
        body = data['body']

        post_id = insert_post(title, timestamp, subreddit, body)
        return jsonify({'success': True, 'post_id': post_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<post_key>', methods=['DELETE'])
def delete_post(post_key):
    try:
        database_index = hash_db_index(post_key)
        db = get_databases()[f"database{database_index + 1}"]
        db_ref = db.child('comments').child(post_key)
        if not db_ref.get():
            return jsonify({'success': False, 'message': 'No post found in the targeted database'}), 404
        
        db_ref.delete()
        return jsonify({'success': True, 'message': 'Post deleted successfully'}), 200
    except Exception as e:
        print(f"Failed to delete post with Firebase ID: {post_key}, Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<post_key>', methods=['PUT'])
def update_post(post_key):
    try:
        data = request.json
        database_index = hash_db_index(post_key)
        db = get_databases()[f"database{database_index + 1}"]
        db_ref = db.child('comments').child(post_key)
        db_ref.update(data)
        print("updated successfully")
        return jsonify({"message": "Post updated successfully", "success": True}), 200
    except Exception as e:
        print(f"Failed to update post with Firebase ID: {post_key}, Error: {str(e)}")
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8001)