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
            info = f"""{word_set["word"]}: {word_set["explanation"]}
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
