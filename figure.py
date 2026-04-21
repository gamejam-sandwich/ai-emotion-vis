import json
import streamlit as st
import main as m


def read_jsons(json_files):
    """
    Returns a list of dictionaries containing the JSON
    files of emotional analysis data from each LLM
    """
    dicts = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            d = json.loads(f.read())
            dicts.append(d)
    return dicts
@st.cache_data
def load_data():
    """Caches the data to avoid reloading on every change"""
    scores = m.get_data("chart")
    return scores[0], scores[1], scores[2]
