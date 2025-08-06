import streamlit as st
import pandas as pd
import os
from utils.loader import process_uploaded_files



def load_data():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=300, use_container_width=False)
        else:
            st.warning("Logo not found")

    st.markdown("""
        <div style='text-align: center; padding: 10px 0;'>
            <h1 style='color:#006300;'>🌱 Welcome to the DCAS Reporting Tool</h1>
            <p style='font-size:20px;'>
                This internal MVP allows you to upload or load farmer & AG user CSVs,
                merge them, analyze growth stages, gender, value chains, messages, and more.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("📂 DCAS Data Upload / Load")
    
    mode = st.radio("Select Input Mode", ["Upload Files", "Load from Local Folder"])

    if mode == "Upload Files":
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





