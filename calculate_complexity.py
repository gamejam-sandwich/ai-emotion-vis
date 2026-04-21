import streamlit as st
import pandas as pd


@st.cache_data
def _load_concreteness():
    """Using streamlit-cache to load data once across all reruns"""
    dataframe = pd.read_csv("concreteness.csv")
    concreteness_dict = dict(zip(dataframe.iloc[:, 0].str.lower(), dataframe.iloc[:, 2]))
    # Structure as {word: concreteness_score}
    return concreteness_dict


def normalize_values(val, min, max):
    """Normalizes the values with min-max scaling"""
    return ((val - min) / (max - min)) * 100





def calculate_complexity(words):
    concreteness_data = _load_concreteness()

    length_list = []
    concreteness_list = []
    norm_len = []
    norm_con = []
    for word in words:
        length_list.append(len(word))
        concreteness_list.append(concreteness_data[word])
    for i in range(len(length_list)):  # pylint: disable=consider-using-enumerate
        current_con = concreteness_list[i]
        current_len = length_list[i]
        norm_con.append(normalize_values(current_con, 1, 5))
        norm_len.append(normalize_values(current_len, 1, 12))

    complexity_list = []
    for i in range(len(norm_len)):  # pylint: disable=consider-using-enumerate
        complexity = (norm_con[i] * 0.6) + (norm_len[i] * 0.4)
        complexity_list.append(complexity)
    return complexity_list

print(calculate_complexity(["apple", "isolated", "unpopular"]))
