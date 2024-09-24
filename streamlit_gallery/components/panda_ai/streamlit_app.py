import os
import json
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
import streamlit as st
import pandas as pd
import time


# Move this line to the top of the script
# st.set_page_config(page_title="🐼 Panda AI Chatbot", layout="centered")

# Function to save token usage with chat history
def save_token_usage(question, response, tokens_used):
    log_entry = {
        "question": question,
        "response": response,
        "tokens_used": tokens_used
    }
    # Append to a JSON file
    with open('data/token_usage_log.json', 'a') as log_file:
        log_file.write(json.dumps(log_entry) + '\n')

# Create a function to initialize PandasAI with OpenAI LLM
def create_pandasai():
    # Initialize OpenAI LLM with API key
    llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
    return llm

def choose_data(data_name):
    
    # Read all necessary CSV files
    instagram_comments = pd.read_csv('data/instagram_comments.csv')
    instagram_replies_comments = pd.read_csv('data/instagram_replies_comments.csv')
    comment_analysis = pd.read_csv('data/comment_analysis.csv')
    instagram_post = pd.read_csv('data/instagram_posts.csv')
    
    if data_name == 'comments_and_replies':
        # Merge DataFrames in the specified order
        merged_data = (
            instagram_post  # Start with post data
            .merge(instagram_comments, on='Post ID', how='left')  # Merge with comments
            .merge(comment_analysis, left_on='Comment ID', right_on='comment_id', how='left')  # Merge with comment analysis
            .merge(instagram_replies_comments, on='Comment ID', how='left')  # Merge with replies
        )
        
        return merged_data
    elif data_name == 'comments_analysis':
        return comment_analysis
    elif data_name == 'comments':
        return instagram_comments
    elif data_name == 'replies':
        return instagram_replies_comments
    


def main():
    st.title("🐼 Panda AI Chatbot")
    st.markdown(
        """
        Welcome to the Panda AI Chatbot! Ask any question about your Instagram data, and the AI will provide insightful answers.
        """
    )
    

    

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for selecting dataset
    st.sidebar.title("Data Selection")
    data_option = ['comments_and_replies','comments_analysis','comments','replies']
    selected_data = st.sidebar.selectbox("Select Data", data_option)
    
    # Load selected data
    upload_data = choose_data(selected_data)

    if upload_data is not None:  # Check if data is loaded
        llm = create_pandasai()
        df = SmartDataframe(upload_data, config={'llm': llm})
        
        # Chat interface styling
        st.markdown(
            """
            <style>
            .user-message { color: white; background-color: #007bff; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: auto; text-align: right;  float: right; }  # Correct alignment for user message
            .ai-message { color: black; background-color: #007bff; padding: 10px; border-radius: 10px; margin-bottom: 10px; width: auto; text-align: left; float: left; }  # Correct alignment for AI message
            </style>
            """, unsafe_allow_html=True)
        
        # Expandable section for the original DataFrame
        with st.expander("View Selected Data", expanded=False):
            st.dataframe(upload_data)

        # Input for user questions
        question = st.text_input("Ask a question about the data:", placeholder="Type your question here...")
        if question:
            with st.spinner('Processing...'):
                response = df.chat(question)
                time.sleep(1)  # Simulate processing time
                
                # Ensure response is a string before counting tokens
                if isinstance(response, str):
                    tokens_used = len(response.split())  # Count tokens based on word count
                else:
                    tokens_used = 0  # Set to 0 if response is not a string

                # Update chat history
                st.session_state.chat_history.append({"message": question,"role": "user"})
                st.session_state.chat_history.append({"role": "ai", "message": response})
                save_token_usage(question, response, tokens_used)
        
        # Chat history display
        with st.container():
            for chat in reversed(st.session_state.chat_history):
                if chat["role"] == "user":
                    st.markdown(f'<div class="user-message"><strong>User:</strong> {chat["message"]}</div>', unsafe_allow_html=True)
                else:
                    message = str(chat["message"])  # Convert to string
                    # Check if the response is an image URL
                    if message.startswith("C:/") and (message.endswith(".png") or message.endswith(".jpg") or message.endswith(".jpeg")):
                        # Convert Windows path to URL format
                        st.markdown(f'<div class="ai-message"><strong>🐼:</strong> <img src="{response}" alt="{response}" style="max-width: 100%; height: auto;"></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="ai-message"><strong>🐼:</strong> {message}</div>', unsafe_allow_html=True)
     
      

    else:
        st.warning("Please select a dataset from the sidebar to proceed.")  # Notify user to select data


if __name__ == "__main__":
    main()

