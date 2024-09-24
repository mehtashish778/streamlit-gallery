import streamlit as st
import pandas as pd
import os

from streamlit_gallery import apps, components
from streamlit_gallery.utils.page import page_group
from API.ig_comment import ig_comments
from pipeline.method.s1 import Instagram_Comment_Analytics
from pipeline.analysis.comment_analysis import comment_analysis


import warnings  # {{ edit_1 }}

# Suppress specific deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*experimental_get_query_params.*")  # {{ edit_2 }}



def main():
    page = page_group("p")

    with st.sidebar:
        st.title("Menu")

        with st.expander("✨ APPS", True):
            page.item("Streamlit gallery", apps.gallery, default=True)

        with st.expander("🧩 COMPONENTS", True):

            page.item("Elements⭐", components.elements)
            page.item("Call Analysis", components.call_analysis)
            page.item("Panda AI", components.pandas_ai)


    page.show()
    

if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="🎈", layout="wide")
    main()
