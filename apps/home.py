import streamlit as st
import geemap.foliumap as geemap
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests, time

def app():
    st.title("Home")

    st.markdown(
        """
    A [streamlit](https://streamlit.io) app template for sat school.

    """
    )

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.image("https://github.com/giswqs/data/raw/main/timelapse/spain.gif")
        st.image("https://github.com/giswqs/data/raw/main/timelapse/las_vegas.gif")

    with row1_col2:
        st.image("https://github.com/giswqs/data/raw/main/timelapse/goes.gif")
        st.image("https://github.com/giswqs/data/raw/main/timelapse/fire.gif")


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()


    lottie_url_hello = "https://assets6.lottiefiles.com/private_files/lf30_cmdcmgh0.json"
    lottie_url_download = "https://assets8.lottiefiles.com/packages/lf20_nay3rc6w.json"
    lottie_hello = load_lottieurl(lottie_url_hello)
    lottie_download = load_lottieurl(lottie_url_download)


    st_lottie(lottie_hello, key="hello", width=200)
    if st.button("Download"):
        with st_lottie_spinner(lottie_download, key="download", width=200):
            time.sleep(15)