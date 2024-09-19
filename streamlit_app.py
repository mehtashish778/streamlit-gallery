import streamlit as st
import pandas as pd
import os

from streamlit_gallery import apps, components
from streamlit_gallery.utils.page import page_group
from API.ig_comment import ig_comments
from pipeline.method.s1 import Instagram_Comment_Analytics
from pipeline.analysis.comment_analysis import comment_analysis

def main():
    page = page_group("p")

    with st.sidebar:
        st.title("Menu")

        # with st.expander("✨ APPS", True):
        #     page.item("Streamlit gallery", apps.gallery, default=True)

        with st.expander("🧩 COMPONENTS", True):
            # page.item("Ace editor", components.ace_editor)
            # page.item("Disqus", components.disqus)
            page.item("Elements⭐", components.elements)
            page.item("Elements1⭐", components.elements)

            # page.item("Pandas profiling", components.pandas_profiling)
            # page.item("Quill editor", components.quill_editor)
            # page.item("React player", components.react_player)

    page.show()
    
    
    # Fetch Instagram Comments button in the sidebar
    if st.sidebar.button("Fetch Instagram Comments"):
        with st.spinner("Fetching comments..."):
            status = ig_comments()  # Assuming ig_comments() is a defined function
            if status == 200:
                st.sidebar.success("Comments fetched successfully!")
            else:
                st.sidebar.error("Failed to fetch comments.")

    # Analyze Comments button in the sidebar
    if st.sidebar.button("Analyze Comments"):
        with st.spinner("Analyzing comments..."):
            # Load comments from CSV
            comments_df = pd.read_csv(os.path.join('data', 'instagram_comments.csv'))
            

            comments_dict = dict(zip(comments_df['Comment ID'], comments_df['Comment Text']))
            
            # Perform analysis
            analysis_results = comment_analysis(comments_dict)  # Assuming comment_analysis is a defined function
            
            # Display results
            st.subheader("Analysis Results")
            for comment_id, analysis in analysis_results.items():
                st.write(f"Comment ID: {comment_id}")
                st.write(f"Comment: {comments_dict[comment_id]}")
                st.write(f"Analysis: {analysis}")
                st.write("---")
            

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="🎈", layout="wide")
    main()
