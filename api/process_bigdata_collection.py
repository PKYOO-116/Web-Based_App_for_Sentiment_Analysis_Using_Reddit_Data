import subprocess

subreddits = ['Politics'] #['US Politics', 'American Politics']
keywords = ['Trump', 'Biden', 'Republican', 'Democrat']
max_comments = 1000

for subreddit in subreddits:
    for keyword in keywords:
        command = ['python3', 'extract_data.py']

        process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)

        process.communicate(f'{subreddit}\n{keyword}\n{max_comments}\n')
        process.wait()
