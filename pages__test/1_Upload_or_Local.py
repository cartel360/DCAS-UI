import streamlit as st
import os
from utils.loader import process_uploaded_files

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


st.title("📂 Load Farmer + AG User Data")

load_mode = st.radio("Select Input Mode", ["Upload Files", "Load from Local Folder"])

if load_mode == "Upload Files":
    st.subheader("Upload Required CSV Files")
    profile_file = st.file_uploader("Farmer Profile CSV", type="csv")
    aguser_file = st.file_uploader("AG User CSV", type="csv")
    msg_code_file = st.file_uploader("Message Code CSV (Optional)", type="csv")

    if profile_file and aguser_file:
        if st.button("🔄 Process Uploaded Files"):
            with st.spinner("Processing..."):
                final_df, dropped_info = process_uploaded_files(profile_file, aguser_file, msg_code_file)
            st.session_state["final_df"] = final_df
            st.session_state["dropped_info"] = dropped_info
            st.success("Upload processed. Proceed to reports.")
else:
    st.subheader("Select Local CSV Files")
    data_folder = "data"
    csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

    if len(csv_files) < 2:
        st.warning("Please ensure at least 2 files are in the `data/` folder.")
    else:
        profile_file = st.selectbox("Farmer Profile CSV", csv_files)
        aguser_file = st.selectbox("AG User CSV", csv_files)
        msg_code_file = st.selectbox("Message Code CSV (optional)", ["None"] + csv_files)

        if st.button("🔄 Load from Local Folder"):
            with open(os.path.join(data_folder, profile_file), 'rb') as f1, \
                 open(os.path.join(data_folder, aguser_file), 'rb') as f2:

                f3 = None
                if msg_code_file != "None":
                    f3 = open(os.path.join(data_folder, msg_code_file), 'rb')

                with st.spinner("Processing local files..."):
                    final_df, dropped_info = process_uploaded_files(f1, f2, f3)
                st.session_state["final_df"] = final_df
                st.session_state["dropped_info"] = dropped_info
                st.success("Local files processed. Proceed to reports.")
