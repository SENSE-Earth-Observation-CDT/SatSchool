import streamlit as st
import apps.streamlit_book as stb

def app():
    st.markdown(
    "<h1 style='text-align: center; color: #565656; background: #ADD8E6'> Oceans 🌊</h1>",
    unsafe_allow_html=True)

    # Streamit book properties
    stb.set_book_config(path="apps/oceans",toc=False, button='top', book_id='oceans')