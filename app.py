import streamlit as st

import streamlit_book as stb
import geemap
from pathlib import Path
#geemap.ee_initialize()


st.session_state["warned_about_save_answers"] = True


st.set_page_config(layout="wide", page_title="SatSchool", page_icon="🛰️")



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Set multipage
current_path = Path(__file__).parent.absolute()

# Streamit book properties
stb.set_book_config(menu_title="Main Menu",
                    menu_icon="",
                    options=[
                            "Introduction",
                            "Land",
                            "Oceans",
                            "Ice",
                            "Quiz"
                            ],
                    paths=[
                        current_path / "apps/intro",
                        current_path / "apps/land",
                        current_path / "apps/oceans",
                        current_path / "apps/ice.py",
                        current_path / "apps/quiz.py",
                          ],
                    icons=[
                          "house",
                          "",
                          "",
                          "",
                          "",
                          "trophy"
                          ],
                    save_answers=True,
                    )
    
with st.sidebar:

    st.sidebar.title("About")
    st.sidebar.info(
        """
        🌐 https://eo-cdt.org
        
        ©️ 2022 SatSchool
    """
    )
