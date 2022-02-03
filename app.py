import streamlit as st

from streamlit_option_menu import option_menu
from apps import home, intro, scores, ice, oceans, land  # import your app modules here

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

titles = [title.lower() for title in list(apps.keys())]
params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0
    
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=list(apps.keys()),
        icons=list(apps.values()),
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        🌐 https://eo-cdt.org
        
        ©️ 2022 SatSchool
    """
    )

# Place each app module under the apps folder
if selected == "Home":
    home.app()
elif selected == "Land":
    land.app()
elif selected == "Oceans":
    oceans.app()
elif selected == "Ice":
    ice.app()
elif selected == "Introduction":
    intro.app()
elif selected == "Scores":
    scores.app()
