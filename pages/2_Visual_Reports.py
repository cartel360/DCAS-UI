import streamlit as st
from utils.reports import render_reports

st.markdown("""
<style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #006300;
    }

    /* Main content background */
    .main {
        background-color: #F5FDF9;
    }

    /* Header and subheaders */
    h1, h2, h3, h4 {
        color: #1F3A2E;
    }

    /* Buttons */
    .stButton > button {
        background-color: #996601;
        color: white;
        border: none;
    }

    .stButton > button:hover {
        background-color: #b37800;
        color: white;
    }

    /* Sidebar menu hover (radio, selectbox, etc.) */
    [data-testid="stSidebar"] .css-1d391kg:hover {
        background-color: #996601 !important;
        color: white !important;
    }

    /* Dataframe table styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #d0d0d0;
    }
</style>
""", unsafe_allow_html=True)


st.title("📊 Visual Reports & Summaries")

if "final_df" not in st.session_state:
    st.warning("⚠️ Please load or upload data first in the previous step.")
    st.stop()

render_reports(st.session_state["final_df"])
