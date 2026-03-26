import plotly.graph_objects as go
import json


def read_jsons(json_files):
    """
    Returns a list of dictionaries containing the JSON
    files of emotional analysis data from each AI agent
    """
    dicts = []
    for file in json_files:
        with open(file, "r") as f:
            d = json.loads(f.read())
            dicts.append(d)
    return dicts


fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[1, 3, 2, 5, 4]
    )
)
