import streamlit as st
import leafmap.foliumap as leafmap
import apps.streamlit_book as stb

def app():
    st.markdown(
    "<h1 style='text-align: center; color: #565656; background: #FADBD8'> Introduction </h1>",
    unsafe_allow_html=True)

    # Streamit book properties
    stb.set_book_config(path="apps/intro",toc=False, button='top', book_id='intro')
    #txi = st.text_input("Text input", disabled=True)

    #st.write(submit)

        
