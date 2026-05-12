import streamlit as st
from site import main


@st.cache_data
def load_data():
    """Caches the data to avoid reloading on every change"""
    scores = main.get_data("chart")
    return scores[0], scores[1], scores[2]
