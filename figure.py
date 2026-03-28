import json
import streamlit as st
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

option = st.selectbox(
    "Choices",
    ("GPT", "Claude", "Gemini")
)
st.write("You selected:", option)

# DEFAULT IS GPT
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=gpt_data[0],
        y=gpt_data[1],
        mode="markers"
    )
)
# TODO: Figure out how to update the axis values
if option == "GPT":
    fig.update_layout(
        xaxis=gpt_data[0],
        yaxis=gpt_data[1]
    )
elif option == "Claude":
    fig.add_trace(
        go.Scatter(
            x=claude_data[0],
            y=claude_data[1],
            mode="markers"
        )
    )
else:
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
