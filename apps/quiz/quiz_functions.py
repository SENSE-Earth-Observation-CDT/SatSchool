import streamlit as st
from datetime import datetime
import pandas as pd
import time
import math
import randomname
import os, glob

TIME_LIMIT = 30 #seconds

def get_name():
    loop = True
    while loop:
        name = randomname.get_name()
        if not os.path.exists(f'{name}.csv'):
            loop = False
    return name

def get_time_remaining(timing):
    time_left = TIME_LIMIT - (timing - st.session_state['time_now'])
    if time_left < 20:
        return 'Only a few seconds left!'
    else:
        return ''
    
def get_all_leaderboard():
    csvs = glob.glob('leaderboard_data/*.csv')
    dfs = [pd.read_csv(i, index_col=False) for i in csvs]
    return pd.concat(dfs)

def show_leaderboard(empty_node, show_results=False):
    with empty_node:
        with st.container():
            if show_results:
                g,h,i = st.columns([6,3,6])
                #st.subheader("Time's up!")
                g.info(f"Time's up! You scored a total of **{st.session_state['total_score']:.2f}** \
                    and answered **{st.session_state['count']}** questions.")
                h.text('\n'); h.text('\n'); h.text('\n'); h.text('\n'); h.text('\n'); h.text('\n')
                if h.button('Give me a different name'):
                    st.session_state['name'] = get_name()
                if 'name' not in st.session_state.keys():
                    st.session_state['name'] = get_name()
                g.markdown(f'Do you want to submit your score to the leaderboard? \n \
                Your name on the leader board will be **{st.session_state["name"]}**.')
            else:
                _,_, i = st.columns([6,6,6])

            df_leaderboard = get_all_leaderboard()
            i.subheader('Leaderboard')
            i.table(df_leaderboard.sort_values(by='Final score:', ascending=False).style.set_table_styles(
            [{
                'selector': 'th',
                'props': [
                    ('background-color', '#D3D3D3'),
                    ('font-color', 'gray')]
            }]))
            
            if show_results:
                df = pd.DataFrame({'Name': st.session_state["name"], 'Final score:': st.session_state['total_score'], 'Questions answered:': st.session_state['count']}, index=[0])
                g.table(df)
                if st.button('Submit my score'):
                    with st.spinner(''):
                        df.to_csv(f'leaderboard_data/{st.session_state["name"]}.csv', mode='a', index=False)
                        st.success('Your score has been submitted!')
                        st.session_state['quiz_active'] = False
                        time.sleep(2)
                        st.experimental_rerun()
            #st.markdown('---')

def answer(ans):
    st.session_state['correct'] = ans
    if ans == 'True':
        score = (1 * math.exp(-0.05*(time.time()-st.session_state['time_now'])))*10
        st.session_state['score'] = max(1, score)
    else:
        st.session_state['score'] = -10
    if st.session_state['total_score'] + st.session_state['score'] > 0:
        st.session_state['total_score'] += st.session_state['score']
    else: 
        st.session_state['total_score'] = 0
        st.session_state['score'] = 0
    st.session_state['total_score'] = max(0, st.session_state['total_score'])
    st.session_state['time_now'] = time.time()
    st.session_state['count'] += 1