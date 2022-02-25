import streamlit as st

import streamlit_book as stb
import ee
ee.Initialize()


st.session_state["warned_about_save_answers"] = True


st.set_page_config(layout="wide", page_title="SatSchool", page_icon="🛰️")



hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com
apps = {"Home": "house", "Introduction": "intro", "Land": "land", "Oceans": "oceans", "Ice": "ice", "Scores": "trophy"}

# Streamit book properties
stb.set_book_config(menu_title="Main Menu",
                    menu_icon="",
                    options=[
                            "Introduction",
                            "Land",
                            "Oceans",
                            "Ice",
                            "Scores"
                            ],
                    paths=[
                        "apps/intro",
                        "apps/land",
                        "apps/oceans",
                        "apps/ice.py",
                        "apps/scores.py",
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