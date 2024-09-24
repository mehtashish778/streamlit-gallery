import json
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace

from .dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player, LineGraph

import warnings  # {{ edit_1 }}

# Suppress specific deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*experimental_get_query_params.*")  # {{ edit_2 }}

# ... existing code ...

def main():
    st.write(
        """
        VI Dashboard ✨ &nbsp; [![GitHub][github_badge]][github_link]
        =====================

        A tool for analyzing Instagram comments, offering insights on sentiment and engagement trends.

        [github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label
        [github_link]: https://github.com/mehtashish778/streamlit-gallery
        """
    )

    st.expander("Comment Analysis")


    if "w" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(board, 12, 12, 12, 5, minW=3, minH=4),
            sentiment_pie=Pie(board, 0, 0, 4, 4, minW=3, minH=4),  # Sentiment pie at first position
            intent_pie=Pie(board, 4, 0, 4, 4, minW=3, minH=4),     # Intent pie next to sentiment pie
            intensity_pie=Pie(board, 8, 0, 4, 4, minW=3, minH=4),  # Intensity pie next to intent pie
            line=LineGraph(board, 0, 0, 12, 8, minW=3, minH=3)


            # pie1=Pie1(board, 0, 12, 6, 10, minH=5),
            # player=Player(board, 0, 12, 6, 10, minH=5),
            # line=LineGraph(board, 12, 7, 3, 7, minW=2, minH=4),
            # card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
            # data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
            
        )
        state.w = w

        # w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
        # w.editor.add_tab("Data grid", json.dumps(DataGrid.DEFAULT_ROWS, indent=2), "json")
        # w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
        w.editor.add_tab("Sentiment Pie chart", "data/comment_analysis.csv", "csv")  # Pass CSV file path
        w.editor.add_tab("Intent Pie chart", "data/comment_analysis.csv", "csv")  # Pass CSV file path
        w.editor.add_tab("Intensity Pie chart", "data/comment_analysis.csv", "csv")  # Pass CSV file path
        
        csv1 = pd.read_csv('data\instagram_comments.csv')
        csv2  = pd.read_csv('data\instagram_replies_comments.csv')
        merged_df = pd.merge(csv1, csv2, on='Comment ID', how='left')
        merged_csv = merged_df.to_csv(index=False)
        
        w.editor.add_tab("Line Graph", merged_csv, "csv")  # Pass CSV file path



        # w.editor.add_tab("Pie chart", "data/comment_analysis.csv", "csv")  # Pass CSV file path



    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.editor()
            # w.player()
            label = "engagement_intensity"  # Replace with the actual label you want to use
            w.sentiment_pie(w.editor.get_content("Sentiment Pie chart"), "engagement_intensity")  # Pass both CSV file path and label
            w.intent_pie(w.editor.get_content("Intent Pie chart"), "sentiment" )
            w.intensity_pie(w.editor.get_content("Intensity Pie chart"), "engagement_intent")
            w.line(w.editor.get_content("Line Graph"), {"Comment Text": "Comment Timestamp", "Reply Comment Text": "Reply Comment Timestamp"},"Comment Trends Over Time")

            # w.radar(w.editor.get_content("Radar chart"))
            # w.card(w.editor.get_content("Card content"))
            # w.data_grid(w.editor.get_content("Data grid"))



if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
