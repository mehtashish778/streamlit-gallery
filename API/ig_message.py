import requests

# Your access token and page ID
ACCESS_TOKEN = 'EAAUkdfPvZBZAoBO6UB4ZAFkLZCnB9ChSUXixVmzpi1dM41CLLxpL59q0SkhghWzirFfdiYaGXzSDH30yDvlnr9PbM3XNKZAcHhi6YFZC3QUydGEkbut9xAhkZAFwyKQZCsR7ZBrn95LAjn2wbYzY6Uqjo5VwQUeST0Y3KZCZCsdg4gFdF4vZAW8hfB4TJrZBRdBXoP8goXZAgVFeQFNbxX1ClXTi8L4fgM2l9kjO7v'
PAGE_ID = '404459866089042'

def get_instagram_conversations():
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/conversations"
    params = {
        'platform': 'instagram',
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        conversations = response.json().get('data', [])
        for conversation in conversations:
            print(f"Conversation ID: {conversation['id']}")
            # Optionally, get messages from the conversation
            get_messages_from_conversation(conversation['id'])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def get_messages_from_conversation(conversation_id):
    url = f"https://graph.facebook.com/v20.0/{conversation_id}/messages"
    params = {
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        messages = response.json().get('data', [])
        for message in messages:
            print(f"Message ID: {message['id']}")
            print(f"From: {message['from']['name']}")
            print(f"Message: {message['message']}")
            print(f"Timestamp: {message['created_time']}")
            print("-" * 40)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    get_instagram_conversations()



    
