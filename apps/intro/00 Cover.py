import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import time
import json

logo = True

with open ('apps/intro/satschoollottie.json', 'r') as f:
    lottie_satschool = json.load(f)
    
st.title('SatSchool - Hands on with Data')

a,b = st.columns([0.3,0.5])

with a:
    st_lottie(lottie_satschool, key="lottie_satschool", speed=0.5, loop=False, quality='high', width=400)
   
b.markdown('''Welcome to Sat School. We like space and satellites. This super duper cool website is fun and easy to use. You'll use satellite data in your browser to look at interesting stuff. Wow! 🚀🚀🚀

This web app illustrates the use of the satschool template for teaching and learning. In this particular web app, we focus on the environmental applications of Earth Observation data.

<img src="https://www.gim-international.com/cache/a/f/b/3/2/afb32cbe5b80419c8de0d63398cfb5c661498273.jpeg" alt="Sentinel 2" width="700">

<br>Adding new pages is simple, modular, and mostly requires no or little code!''', unsafe_allow_html=True)
