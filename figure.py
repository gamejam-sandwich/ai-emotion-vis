import plotly.graph_objects as go
import json


def _read_jsons():
    json_files = ["gpt.json", "claude.json", "gemini.json"]
    dicts = []
    for file in json_files:
        with open(file, "r")as f:
            print(f.readline())
    return dicts

dictionaries = _read_jsons()
print(dictionaries)
"""
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[1, 3, 2, 5, 4]
    )
)
"""