import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_processing import calculate_complexity
import figure as f


def get_data(list_name):
    """Gets 2D list of datapoints"""
    json_files = ["llm_files/chatgpt.json", "llm_files/claude_sonnet.json", "llm_files/gem.json"]
    table_list = []
    scores_list = []
    i = 0
    dictionaries = f.read_jsons(json_files)
    for d in dictionaries:
        mini_list = []
        emotion_scores = []
        semantic_scores = []
        word_list = []
        for word_set in d:
            info = f"""{word_set["word"]}: {word_set["explanation"]}
                  """
            emotion_scores.append(word_set["emotional_intensity"])
            word_list.append(word_set["word"])
            mini_list.append(info)
        semantic_scores = calculate_complexity(word_list)
        print(semantic_scores)
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

    option = st.selectbox(
        "Choices",
        ("GPT", "Claude", "Gemini"),
    )
    #TODO: CHANGE OPTION TO CHECKBOX INSTEAD OF DROPDOWN
    #TODO: ADD OPTION FOR SHOWING ALL THREE, ALSO DIFFERENT COLORS FOR EACH
    fig = go.Figure()
    # DEFAULT IS GPT
    if option == "GPT":
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=gpt_data[0],
                y=gpt_data[1],
                mode="markers"
            )
        )
    elif option == "Claude":
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=claude_data[0],
                y=claude_data[1],
                mode="markers"
            )
        )
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=gemini_data[0],
                y=gemini_data[1],
                mode="markers"
            )
        )
    fig.update_layout(
        title=option,
        xaxis_title="Emotional intensity",
        yaxis_title="Semantic complexity"
    )
    st.plotly_chart(fig, config={'scrollZoom': False})

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
