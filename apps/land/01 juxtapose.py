from streamlit_juxtapose import juxtapose
import streamlit as st
from PIL import Image
import requests

import pathlib
    
st.title('Rondônia in western Brazil')

with st.container():


    STREAMLIT_STATIC_PATH = (
    pathlib.Path(st.__path__[0]) / "static"
    )  # at venv/lib/python3.9/site-packages/streamlit/static

    IMG1 = "2000.jpg"
    IMG2 = "2012.jpg"

    DEFAULT_IMG1_URL = (
    "https://juxtapose.knightlab.com/static/img/Sochi_11April2005.jpg"
    )
    DEFAULT_IMG2_URL = (
    "https://juxtapose.knightlab.com/static/img/Sochi_22Nov2013.jpg"
    )

    def fetch_img_from_url(url: str) -> Image:
        from PIL import Image
        import requests
        
        img = Image.open(requests.get(url, stream=True).raw)
        return img

    #form = st.form(key="Image comparison")
    #img1_url = form.text_input("Image one url", value=DEFAULT_IMG1_URL)
    #img1 = fetch_img_from_url(DEFAULT_IMG1_URL)
    img1 = Image.open('apps/land/amazon_deforestation_20000730_lrg.jpg')
    img1.save(STREAMLIT_STATIC_PATH / IMG1)

    #img2_url = form.text_input("Image two url", value=DEFAULT_IMG2_URL)
    #img2 = fetch_img_from_url(DEFAULT_IMG2_URL)
    img2 = Image.open('apps/land/amazon_deforestation_20120718_lrg.jpg')
    img2.save(STREAMLIT_STATIC_PATH / IMG2)

    #submit = form.form_submit_button("Submit")
    #if submit:
    
    juxtapose(IMG1, IMG2, label1='30th July 2000', label2='18th July 2012')
