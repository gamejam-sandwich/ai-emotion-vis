from streamlit_plotly_events import plotly_events
import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import data_processing
import gpt_embedding

# dummy

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
    print(gemini_data)

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
    col4, col5, col6 = st.columns([1, 5, 1])
    if selected_models:
        with col5:
            fig.update_layout(
                title=dict(text="Semantic Complexity vs Emotional Intensity", x=0.5, xanchor="center"),
                xaxis_title="Emotional intensity",
                yaxis_title="Semantic complexity",
                dragmode=False,
                width=500,
                height=500
            )
            fig.update_xaxes(range=[30,100], dtick=10)
            fig.update_yaxes(range=[30,100], dtick=10)
            # Click event
            selected_point = plotly_events(fig, click_event=True, select_event=False, hover_event=False)
            #st.plotly_chart(fig, config={'scrollZoom': False}, use_container_width=False)
        
        with col6:
            if selected_point:
                point = selected_point[0]
                x=point['x']
                y=point['y']
                st.write(f"Point:{x}, {y}")
    else:
        st.error("Select at least one model")
    
    

    table_list = get_data("table")
    scores_list = get_data("chart")

    model_names = ["Chat-GPT", "Claude", "Gemini"]
    columns = {}
    for i, name in enumerate(model_names):
        column = []
        for j in range(len(table_list[i])):
            cell = table_list[i][j]
            emotional = scores_list[i][0][j]
            semantic = scores_list[i][1][j]
            column.append(f"{cell}\nEmotional: {emotional:.1f} | Semantic: {semantic:.1f}")
        columns[name] = column

    matrix = pd.DataFrame(columns, index=[i for i in range(1, 26)])
    st.table(matrix)

    """
    matrix = pd.DataFrame(
        {
            "Chat-GPT": table_list[0],
            "Claude": table_list[1],
            "Gemini": table_list[2]
        },
        index = [i for i in range(1, 26)]
    )
    st.table(matrix)
    """



if __name__ == "__main__":
    launch_dashboard()
