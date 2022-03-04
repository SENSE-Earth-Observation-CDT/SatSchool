import os
import geopandas as gpd
import streamlit as st
import numpy as np
import pandas as pd
import streamlit_book as stb
import random
import time

land_questions = [
{'question':"What does NDVI stand for?",
                  'options': {
                   "Natural difference vegetation index":False,
                   "Nature dynamic vigour index":False,
                   "Nature dimensionless vigour index":False,
                   "Normalised difference vegetation index":True,
                   },
                  'success':"custom success message",
                  'error':"custom error message",
                  'button':"Check answer"},
                  
{'question':"Deforestation is the ____ largest cause of human-caused climate change?",
                  'options': {
                   "1st":False,
                   "2nd":True,
                   "3rd":False,
                   "4th":False,
                   },
                  'success':"Correct! Only the burning of fossil fuels is more damaging.",
                  'error':"custom error message",
                  'button':"Check answer"},
                  
{'question':"Which of the following does deforestation affect?",
                  'options': {
                   "Harm to the local economies":True,
                   "Uprooting indigenous people":True,
                   "Threaten biodiversity":True,
                   },
                  'success':"Correct! All of them. The largest biodiversity on Earth is found in tropical forests.",
                  'error':"custom error message",
                  'button':"Check answer"},
                  
{'question':"The rainforest houses incredible biodiversity. Which of these is **not** a real rainforest resident?",
                  'options': {
                   "Thunder Dragon Mantis":True,
                   "Black Howler Monkey":False,
                   "Strawberry Dart Frog.":False,
                   "Rhinoceros Hornbill":False,
                   },
                  'success':"Correct!",
                  'error':"custom error message",
                  'button':"Check answer"},
                  
{'question':"How many of the Earth’s plants and animals are found in the tropical rainforests?",
                  'options': {
                   "25%":False,
                   "33%":False,
                   "50%":True,
                   "75%":False,
                   },
                  'success':"Correct! There are also many rare plants which have medicinal properties only found in the rainforest.",
                  'error':"custom error message",
                  'button':"Check answer"},
]

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

quiz_active = False
if not quiz_active:
    quiz_start = st.button('Start quiz!')

if quiz_start:
	st.session_state['quiz_active'] = True
	quiz_active=True
	
if 'quiz_active' in st.session_state.keys():
    quiz_active = True
    
if quiz_active:
    key_quiz = 'land' + '1'
    
    qn = random.choice(land_questions)
    time_start = time.time()
    
    ans = stb.multiple_choice(qn['question'],
                  qn['options'],
                  success=qn['success'],
                  error=qn['error'],
                  button=qn['button'])
    print(ans, time.time()-time_start)
                  
                  
st.header('Test your knowledge')

st.subheader('Land')


                  
st.subheader('Oceans')

stb.multiple_choice("How much of the Earth’s surface is covered by oceans? ",
                  {
                   "51%":False,
                   "71%":True,
                   "81%":False,
                   "91%":False,
                   },
                  success="Correct!",
                  error="custom error message",
                  button="Check answer")
                  
stb.true_or_false("True or False. Humans have mapped more of Mars than they have of the Earth’s oceans.", True,
                  success="True!  Remote sensing allows us to explore more of the Earth’s surface than ever before, particularly in places difficult to access such as the poles.",
                  error="custom error message",
                  button="Check answer")
                  
stb.multiple_choice("How deep is the Marianas trench?",
                  {
                   "1 mile":False,
                   "2 miles":False,
                   "7 miles":True,
                   "11 miles":False,
                   },
                  success="Correct! It is so deep it could fit Mt. Everest, with a mile to spare!",
                  error="custom error message",
                  button="Check answer")
                  
stb.single_choice("Which is not a cause of major ocean currents?",
                  [
                   "Wind blowing",
                   "Volcanoes erupting",
                   "Earth rotating",
                   "Water density varying",
                   ],
                  answer_index=1,
                  success="Correct! The oceans currents are complex depending on the rotation of the Earth, surface winds and the water density, which is affected by the temperature and salinity (saltiness).",
                  error="custom error message",
                  button="Check answer")
                  
                  
stb.single_choice("Which process does not lead to a decrease in water salinity?",
                  [
                   "Run off from the land",
                   "Precipitation",
                   "Sea ice melting",
                   "Evaporation",
                   ],
                  answer_index=3,
                  success="Correct! When water freezes it releases salt into the surrounding, so as it melts the fresh water reduces the salinity",
                  error="custom error message",
                  button="Check answer")
                  
st.subheader('Ice')

stb.single_choice("Where is the majority of the permafrost in the world?",
                  [
                   "Arctic",
                   "Antartica",
                   ],
                  answer_index=0,
                  success="Correct! In the Arctic circle, the permafrost is the polar region with the permanently frozen land. As this melts this can release carbon dioxide held in peat bogs and also warm the poles further due to the ice no longer reflecting the sunlight (albedo effect).",
                  error="custom error message",
                  button="Check answer")
                  
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
