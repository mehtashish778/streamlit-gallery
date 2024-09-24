import streamlit as st
from API.ig_comment import ig_comments
from pipeline.method.s1 import Instagram_Comment_Analytics
from pipeline.analysis.comment_analysis import comment_analysis
import pandas as pd
import os
import json
from pathlib import Path
from datetime import datetime


import warnings  # {{ edit_1 }}

# Suppress specific deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*experimental_get_query_params.*")  # {{ edit_2 }}


# Add custom CSS for creativity
def load_custom_css():
    st.markdown("""
        <style>
            .title-style {
                font-size: 42px;
                color: #1A73E8;
                font-weight: bold;
                text-align: center;
            }
            .sidebar-style {
                font-size: 18px;
                color: #1A73E8;
            }
            .header {
                color: #FF6347;
                font-size: 24px;
                margin-bottom: 10px;
            }
            .result-box {
                border: 2px solid #1A73E8;
                padding: 15px;
                border-radius: 10px;
                background-color: #f7f9fb;
            }
        </style>
    """, unsafe_allow_html=True)

def main():
    load_custom_css()
    
    st.markdown('<h1 class="title-style">📊 Welcome to the Central Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("<p>This is a unified internal data application of VetInstant.</p>", unsafe_allow_html=True)
    
    # Sidebar with fetching and analyzing options
    st.sidebar.markdown('<h2 class="sidebar-style">Fetch Latest Data</h2>', unsafe_allow_html=True)
    
    # Load last fetch time from JSON
    with open('data/last_fetch_time.json') as f:
        last_fetch_data = json.load(f)
    last_fetch_time = last_fetch_data.get("last_fetch", "No fetch time available")
    
    # Display last fetch time
    st.markdown(f"**🕒 Last Fetch Time:** {last_fetch_time}")

    # Fetch Instagram Comments button in the sidebar
    if st.sidebar.button("🚀 Fetch Instagram Comments", key="fetch_comments"):
        with st.spinner("Fetching comments..."):
            status = ig_comments()  # Assuming ig_comments() is a defined function
            if status == 200:
                # Update last fetch time
                new_fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                last_fetch_data["last_fetch"] = new_fetch_time
                with open('data/last_fetch_time.json', 'w') as f:
                    json.dump(last_fetch_data, f)
                
                st.sidebar.success("✅ Comments fetched successfully!")
                st.balloons()  # Fun animation on success!
            else:
                st.sidebar.error("❌ Failed to fetch comments.")

    # Analyze Comments button in the sidebar
    if st.sidebar.button("🔍 Analyze Comments", key="analyze_comments"):
        with st.spinner("Analyzing comments..."):
            # Load comments from CSV
            comments_df = pd.read_csv(os.path.join('data', 'instagram_comments.csv'))
            
            comments_dict = dict(zip(comments_df['Comment ID'], comments_df['Comment Text']))
            
            # Perform analysis
            analysis_results = comment_analysis(comments_dict)  # Assuming comment_analysis is a defined function
            
            # Display results with columns for better structure
            st.subheader("📈 Analysis Results")
            col1, col2 = st.columns(2)
            
            for i, (comment_id, analysis) in enumerate(analysis_results.items()):
                if i % 2 == 0:
                    with col1:
                        display_result(comment_id, comments_dict, analysis)
                else:
                    with col2:
                        display_result(comment_id, comments_dict, analysis)

# Helper function to display each result
def display_result(comment_id, comments_dict, analysis):
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown(f"<p class='header'>💬 Comment ID: {comment_id}</p>", unsafe_allow_html=True)
    st.write(f"**Comment:** {comments_dict[comment_id]}")
    st.write(f"**Analysis:** {analysis}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")  # Horizontal line to separate comments

if __name__ == "__main__":
    main()
