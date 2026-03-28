import streamlit as st
import pandas as pd
import figure as f


def get_data(list_name):
    '''Gets 2D list of datapoints'''
    json_files = ["gpt.json", "claude.json", "gemini.json"]
    table_list = []
    scores_list = []
    i = 0
    dictionaries = f.read_jsons(json_files)
    for d in dictionaries:
        mini_list = []
        emotion_scores = []
        semantic_scores = []
        for word_set in d:
            info = f"""{word_set["word"]} with emotional intensity
                  {word_set["emotional_intensity"]}
                  and semantic complexity {word_set["semantic_complexity"]}
                  """
            emotion_scores.append(word_set["emotional_intensity"])
            semantic_scores.append(word_set["semantic_complexity"])
            mini_list.append(info)
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
    st.plotly_chart(f.fig, config={'scrollZoom': False})

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
