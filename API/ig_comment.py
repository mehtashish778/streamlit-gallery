import requests
import pandas as pd
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import requests
import pandas as pd
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import json
import os
import csv


# Constants (move these to a separate config file in a real-world scenario)
ACCESS_TOKEN = 'key'
MY_USERNAME = 'VETiNSTANT'
INSTAGRAM_ACCOUNT_ID = '17841459159542761'
BASE_URL = 'https://graph.facebook.com/v20.0'

DATA_DIR = 'data'


def save_last_fetch_time():
    current_time = datetime.datetime.now().isoformat()
    # Save the last fetch time in the data folder
    with open(os.path.join(DATA_DIR, 'last_fetch_time.json'), 'w') as f:
        json.dump({'last_fetch': current_time}, f)

def get_last_fetch_time():
    if os.path.exists(os.path.join(DATA_DIR, 'last_fetch_time.json')):
        with open(os.path.join(DATA_DIR, 'last_fetch_time.json'), 'r') as f:
            data = json.load(f)
            return data.get('last_fetch')
    return None


def make_api_request(url: str, params: Dict) -> Dict:
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
    response.raise_for_status()
    return response.json().get('data', [])

def create_csv_if_not_exists():
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # if file does not exist create new files 
    if not os.path.exists(os.path.join(DATA_DIR, 'instagram_posts.csv')):
        with open(os.path.join(DATA_DIR, 'instagram_posts.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Post ID','Post Timestamp','Number of Comments','Caption','Hashtags Used','Is Collaborative','Type of Post','Collaborator User IDs'])
            
        
            
    if not os.path.exists(os.path.join(DATA_DIR, 'instagram_comments.csv')):
        with open(os.path.join(DATA_DIR, 'instagram_comments.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile) 
            writer.writerow(['Post ID','Comment ID','Comment Timestamp','Comment Text', 'Comment Username', 'Is Replied by Us'])
            
                    
    
    if not os.path.exists(os.path.join(DATA_DIR, 'instagram_replies_comments.csv')):
        with open(os.path.join(DATA_DIR, 'instagram_replies_comments.csv'), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Comment ID', 'Reply Comment ID', 'Reply Comment Timestamp', 'Reply Comment Text', 'Reply Comment Username' ])

            
def get_instagram_posts() -> List[Dict]:
    url = f'{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media'
    params = {
        'fields': 'id,caption,timestamp,comments_count,media_type',
        'access_token': ACCESS_TOKEN
    }
    return make_api_request(url, params)


def get_comments_for_post(post_id: str) -> List[Dict]:
    url = f'{BASE_URL}/{post_id}/comments'
    params = {
        'fields': 'id,text,timestamp,username',
        'access_token': ACCESS_TOKEN
    }
    return make_api_request(url, params)

def get_replies_for_comment(comment_id: str) -> List[Dict]:
    url = f'{BASE_URL}/{comment_id}/replies'
    params = {
        'fields': 'id,text,timestamp,username',
        'access_token': ACCESS_TOKEN
    }
    return make_api_request(url, params)

def process_post(post: Dict) -> Tuple[Dict, List[Dict], List[Dict]]:
    post_data = {
        'Post ID': post['id'],
        'Post Timestamp': post['timestamp'],
        'Number of Comments': post['comments_count'],
        'Caption': post.get('caption', ''),
        'Hashtags Used': [tag for tag in post.get('caption', '').split() if tag.startswith('#')],
        'Is Collaborative': post.get('is_collaborative_post', False),
        'Type of Post': post.get('media_type', 'unknown'),
        'Collaborator User IDs': post.get('collaborators', [])
    }
    
    comments = get_comments_for_post(post['id'])
    comment_data = []
    reply_data = []
    
    for comment in comments:
        replies = get_replies_for_comment(comment['id'])
        is_reply_by_me = 'Yes' if replies and replies[-1]['username'] == MY_USERNAME else 'No'
        
        comment_data.append({
            'Post ID': post['id'],
            'Comment ID': comment['id'],
            'Comment Timestamp': comment['timestamp'],
            'Comment Text': comment['text'],
            'Comment Username': comment['username'],
            'Is Replied by Us': is_reply_by_me
        })
        
        reply_data.extend([{
            'Comment ID': comment['id'],
            'Reply Comment ID': reply['id'],
            'Reply Comment Timestamp': reply['timestamp'],
            'Reply Comment Text': reply['text'],
            'Reply Comment Username': reply['username']
        } for reply in replies])
    
    return post_data, comment_data, reply_data

def ig_comments():
    create_csv_if_not_exists()  # Ensure CSV files are created in the data folder
    posts = get_instagram_posts()
    
    post_data = []
    comment_data = []
    reply_data = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_post = {executor.submit(process_post, post): post for post in posts}
        for future in as_completed(future_to_post):
            post_info, comments, replies = future.result()
            post_data.append(post_info)
            comment_data.extend(comments)
            reply_data.extend(replies)
    
    # Create DataFrames from the collected data
    post_df = pd.DataFrame(post_data)
    comment_df = pd.DataFrame(comment_data)
    reply_df = pd.DataFrame(reply_data)

    # Export to CSV files in the data folder
    post_df.to_csv(os.path.join(DATA_DIR, 'instagram_posts.csv'), index=False)
    comment_df.to_csv(os.path.join(DATA_DIR, 'instagram_comments.csv'), index=False)
    reply_df.to_csv(os.path.join(DATA_DIR, 'instagram_replies_comments.csv'), index=False)
    
    # Save the current fetch time
    save_last_fetch_time()
    
    return 200

# if __name__ == "__main__":
#     ig_comments()