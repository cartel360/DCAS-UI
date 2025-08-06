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
            <h1 style='color:#006300;'>🌱 Welcome to the Survey Reporting Tool</h1>
            <p style='font-size:20px;'>
                This internal MVP allows you to upload or load farmer & AG user CSVs,
                merge them, analyze growth stages, gender, value chains, messages, and more.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.header("📂 Survey Data Upload / Load")
    
    mode = st.radio("Select Input Mode", ["Upload Files", "Load from Local Folder"])

    if mode == "Upload Files":
        profile = st.file_uploader("Farmer Profile CSV", type="csv")
        aguser = st.file_uploader("AG User CSV", type="csv")
        msgcodes = st.file_uploader("Message Codes CSV", type="csv")

        if profile and aguser:
            st.success("Files uploaded successfully. Ready to process.")
            if st.button("🔄 Process Uploaded Files"):
                with st.spinner("Processing..."):
                    final_df, dropped_info = process_uploaded_files(profile, aguser, msgcodes)
                st.session_state["final_df"] = final_df
                st.session_state["dropped_info"] = dropped_info
                st.success("Upload processed. Proceed to reports.")
    else:
        st.info("Local folder mode not yet implemented in this snippet.")





