import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import data_processing
import gpt_embedding

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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data(list_name):
    """Gets 2D list of datapoints"""
    json_files = [
        os.path.join(BASE_DIR, "llm_files", "chatgpt.json"),
        os.path.join(BASE_DIR, "llm_files", "claude_sonnet.json"),
        os.path.join(BASE_DIR, "llm_files", "gem.json")
    ]
    table_list = []
    scores_list = []
    i = 0
    dictionaries = read_jsons(json_files)
    for d in dictionaries:
        mini_list = []
        emotion_scores = []
        semantic_scores = []
        word_list = []
        for word_set in d:
            info = f"""{word_set["word"]}: {word_set["explanation"]}
                  """
            #emotion_scores.append(word_set["emotional_intensity"])
            score = gpt_embedding.get_emotional_intensity(word_set["word"])
            emotion_scores.append(score)
            word_list.append(word_set["word"])
            mini_list.append(info)
        semantic_scores = data_processing.calculate_complexity(word_list)
        table_list.append(mini_list)
        temp = [emotion_scores, semantic_scores]
        scores_list.append(temp)
        i += 1
    if list_name == "table":
        return table_list
    elif list_name == "chart":
        return scores_list

def launch_dashboard():
    """Streamlit dashboard"""
    st.write("# AI Emotional Analysis Visualization")

    scores = get_data("chart")
    gpt_data = scores[0]
    claude_data = scores[1]
    gemini_data = scores[2]


    # Arrange checkboxes horizontally
    col1, col2, col3 = st.columns(3)
    with col1:
        # Default select to display Claude's data
        claude = st.checkbox("Claude", value=True)
    with col2:
        gemini = st.checkbox("Gemini")
    with col3:
        gpt = st.checkbox("Chat-GPT")

    fig = go.Figure()
    selected_models = []

    if claude:
        fig.add_trace(
            go.Scatter(
                x=claude_data[0],
                y=claude_data[1],
                mode="markers",
                marker=dict(color="red"),
                name="Claude"
            )
        )
        selected_models.append("Claude")
    if gemini:
        fig.add_trace(
            go.Scatter(
                x=gemini_data[0],
                y=gemini_data[1],
                mode="markers",
                marker=dict(color="green"),
                name="Gemini"
            )
        )
        selected_models.append("Gemini")
    if gpt:
        fig.add_trace(
            go.Scatter(
                x=gpt_data[0],
                y=gpt_data[1],
                mode="markers",
                marker=dict(color="blue"),
                name="GPT"
            )
        )
        selected_models.append("GPT")
    if selected_models:
        fig.update_layout(
            title="Semantic Complexity vs Emotional Intensity",
            xaxis_title="Emotional intensity",
            yaxis_title="Semantic complexity"
        )
        st.plotly_chart(fig, config={'scrollZoom': False})
    else:
        st.error("Select at least one model")
    #TODO: When clicking each cell in the table, it should highlight
    # the specific point on the graph. Also should automatically
    # switch the dropdown to the agent that the word is for.
    # MAYBE: example, if you hover over one of GPT's cells and the chart
    # is currently on GPT's data, that point will be highlighted. But if
    # you hovered over Gemini, it wouldn't highlight. You would have to
    # switch to Gemini's data then hover/click on its cells for the effects.
    table_list = get_data("table")
    matrix = pd.DataFrame(
        {
            "Chat-GPT": table_list[0],
            "Claude": table_list[1],
            "Gemini": table_list[2]
        },
        index = [i for i in range(1, 26)]
    )
    st.table(matrix)



if __name__ == "__main__":
    launch_dashboard()
