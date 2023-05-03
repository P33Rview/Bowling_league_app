###################
### BOWLING APP ###
###################
import requests
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu


# Set up the configuration of the webpage
st.set_page_config(page_title = "Bowling Analytics", page_icon = ":bowling:", layout = "wide")

# --- STORING ASSETS ---
def load_animation(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

animation_bowling_1 = load_animation("https://assets10.lottiefiles.com/datafiles/qbAoVVjPqpGHkwP/data.json")
animation_bowling_2 = load_animation("https://assets10.lottiefiles.com/private_files/lf30_rivr2ir4.json")

# --- MANIPULATING STREAMLIT ELEMENTS ---

#manipulate_st_elemenents = """
#                        <style>
#                        #MainMenu {visibility: hidden;}
#                        footer {visibility: hidden;}
#                        header {visibility: hidden;}
#                        </style>
#                        """
#
#
#st.markdown(manipulate_st_elemenents, unsafe_allow_html=True)

# --- HEADER ---
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title("Bowling Analytics App :trophy:")
        st.subheader("Hi there, here you can find your performance over the last two bowling seasons.")
    with right_column:
        st_lottie(animation_bowling_2, height = 200, key = "coding")

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title = None,
    options =[ "Introdution", "Ranking", "Statistics"],
    icons = ["info-square-fill", "123", "bar-chart-fill"], #icons.getbootstrap.com
    orientation = "horizontal"
)

# --- BODY ---
with st.container():
    st.write("---")
    #setting the page into 2 columns
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Rankings")
