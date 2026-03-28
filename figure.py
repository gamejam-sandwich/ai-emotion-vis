import json
import plotly.graph_objects as go
import main as m


def read_jsons(json_files):
    """
    Returns a list of dictionaries containing the JSON
    files of emotional analysis data from each AI agent
    """
    dicts = []
    for file in json_files:
        with open(file, "r", encoding="utf-8") as f:
            d = json.loads(f.read())
            dicts.append(d)
    return dicts

scores = m.get_data("chart")
gpt_data = scores[0]
claude_data = scores[1]
gemini_data = scores[2]

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=gpt_data[0],
        y=gpt_data[1],
        mode="markers"
    )
)
