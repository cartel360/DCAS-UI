import streamlit as st
from streamlit_lottie import st_lottie
import json
import os

st.set_page_config(page_title="DCAS Reporting Tool", layout="wide")


st.markdown("""
<style>
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #006300;
    }
    
    /* Sidebar text color */
    [data-testid="stSidebar"] .css-1d391kg, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
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

    /* Sidebar menu hover */
    [data-testid="stSidebar"] .css-1d391kg:hover {
        background-color: #996601 !important;
        color: white !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #d0d0d0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------
# Sidebar (Logo + Menu)
# ---------------------
# with st.sidebar:
#     st.markdown("""
#         <a href="/" target="_self">
#             <img src="assets/logo.png" width="220">
#         </a>
#     """, unsafe_allow_html=True)

#     st.markdown("## 🌾 DCAS Reporting Tool")
#     st.markdown("MVP for visualizing farmer and AG user data.")
#     st.markdown("---")

#     st.markdown("👤 Built for Internal Use")
#     st.markdown("🔖 Version: `v0.1 MVP`")


# ---------------------
# Landing Page Content
# ---------------------

# Optional: Lottie animation
# def load_lottie(path: str):
#     with open(path, "r") as f:
#         return json.load(f)

# if os.path.exists("assets/planting.json"):
#     lottie_json = load_lottie("assets/planting.json")
#     st_lottie(lottie_json, height=200, speed=1)

# st.markdown("""
#     <div style='text-align: center; padding: 30px 0;'>
#         <h1 style='color:#006300;'>🌱 Welcome to the DCAS Reporting Tool</h1>
#         <p style='font-size:20px;'>
#             This internal MVP allows you to upload or load farmer & AG user CSVs,
#             merge them, analyze growth stages, gender, value chains, messages, and more.
#         </p>
#     </div>
# """, unsafe_allow_html=True)

# st.markdown("---")

# st.markdown("### 🚀 Get Started")
# st.info("Use the sidebar to **upload CSVs** or **load from your local data folder**.")
# st.markdown("👉 After loading, navigate to the **Reports** tab to explore interactive insights.")

import streamlit as st
from modules.dcas import data_loader as dcas_loader, reports as dcas_reports, visualizations as dcas_viz
from modules.gaps import data_loader as gaps_loader, reports as gaps_reports, visualizations as gaps_viz
from modules.survey import data_loader as dis_loader, reports as dis_reports, visualizations as dis_viz

st.set_page_config(page_title="DCAS Reporting Tool", layout="wide")

# Logo and header
st.sidebar.image("assets/logo.png", use_container_width=True)
st.sidebar.markdown("## 📊 Data Insights Platform")

# Main navigation
module = st.sidebar.selectbox("Select Module", ["DCAS", "GAPS", "Survey"])
sub_menu = st.sidebar.radio("Go to", ["Upload / Load Data", "Reports"])

# Conditional rendering based on module/submenu
if module == "DCAS":
    if sub_menu == "Upload / Load Data":
        dcas_loader.load_data()
    elif sub_menu == "Reports":
        dcas_reports.render_reports()

elif module == "GAPS":
    if sub_menu == "Upload / Load Data":
        gaps_loader.load_data()
    elif sub_menu == "Reports":
        gaps_reports.render_reports()

elif module == "Survey":
    if sub_menu == "Upload / Load Data":
        dis_loader.load_data()
    elif sub_menu == "Reports":
        dis_reports.render_reports()
