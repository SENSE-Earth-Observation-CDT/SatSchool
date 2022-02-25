import os
import geopandas as gpd
import streamlit as st
import numpy as np
import pandas as pd

def save_uploaded_file(file_content, file_name):
    """
    Save the uploaded file to a temporary directory
    """
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(file_name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(file_content.getbuffer())

    return file_path


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.markdown(
"<h1 style='text-align: center; color: #565656; background: #F1E5AC'> Scores 🏆</h1>",
unsafe_allow_html=True)

st.write("")
st.write("This page will have a quiz/game that you can complete after you have completed all the modules.")
st.write("The quiz will test your knowledge of the modules, and will give you a score to be shown on the board.")

np.random.seed(0)
dataset = pd.read_csv("https://raw.githubusercontent.com/advaitapatel/leaderboards/master/leaderboard_final.csv", index_col=None)
dataset.sample(frac=1)

st.table(dataset.head().style.set_table_styles(
    [{
        'selector': 'th',
        'props': [
            ('background-color', '#D3D3D3'),
            ('font-color', 'gray')]
    }]))
