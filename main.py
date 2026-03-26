import streamlit as st
import figure as f

def launch_dashboard():
    """Streamlit dashboard"""
    st.write("# AI Emotional Analysis Visualization")
    st.plotly_chart(f.fig, config={'scrollZoom': False})


if __name__ == "__main__":
    launch_dashboard()
