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
   
b.markdown("""Welcome to the 'Hands on with Data' module as part of SatSchool. 🚀🚀🚀

For the main SatSchool website, please visit **[https://satschool-outreach.github.io](https://satschool-outreach.github.io)**.



In this module you will learn how to manipulate and understand data from satellites in a range of environmental contexts. It's your chance to get hands on with satellite data!

You will learn:

* How scientists work with satellite data to better understand different parts of the Earth system
* How to work with different kinds of satellite data yourself and the types of information it contains
* How to interpret maps and graphs displaying different types of environmental data

<img src="https://www.gim-international.com/cache/a/f/b/3/2/afb32cbe5b80419c8de0d63398cfb5c661498273.jpeg" alt="Sentinel 2" width="700">""", unsafe_allow_html=True)
