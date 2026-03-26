import streamlit as st
import pandas as pd
import figure as f

def launch_dashboard():
    """Streamlit dashboard"""
    st.write("# AI Emotional Analysis Visualization")
    #st.plotly_chart(f.fig, config={'scrollZoom': False})

    json_files = ["gpt.json", "claude.json", "gemini.json"]
    data_list = []
    i = 0
    dictionaries = f.read_jsons(json_files)
    for d in dictionaries:
        mini_list = []
        for word_set in d:
            info = f"""{word_set["word"]} with emotional intensity
                  {word_set["emotional_intensity"]}
                  and semantic complexity {word_set["semantic_complexity"]}
                  """
            mini_list.append(info)
        data_list.append(mini_list)
        i += 1

    #TODO: turn this into a separate function
    matrix = pd.DataFrame(
        {
            "Chat-GPT": data_list[0],
            "Claude": data_list[1],
            "Gemini": data_list[2]
        },
        index = [i for i in range(1, 26)]
    )
    st.table(matrix)



if __name__ == "__main__":
    launch_dashboard()
