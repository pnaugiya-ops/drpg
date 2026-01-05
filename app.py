import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { 
        background:#003366; color:white; padding:20px; 
        border-radius:15px; text-align:center; margin-bottom:10px; 
    }
    .stButton>button { 
        border-radius:10px; background:#ff4b6b; color:white; 
        font-weight:bold; width:100%; 
    }
    .diet-box { 
        background: #fff5f7; padding: 15px; border-radius: 10px; 
        border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; 
    }
    .clinic-badge { 
        background: #e8f4f8; color: #003366; padding: 5px 10px; 
        border-radius: 5px; font-weight: bold; display: inline-block; 
        margin: 2px; font-size: 11px; border: 1px solid #003366; 
    }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database Connection Error. Check secrets.toml.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "age":a, "stat":s, "role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APP ---
else:
    # Sidebar
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}")
    st.sidebar.markdown(f"**Age:** {st.session_state.get('age', 'N/A')}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.write("Access records via Google Sheets.")
    
    else: # Patient View
        menu_options = ["Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccination Record", "Book Appointment"]
        m = st.sidebar.radio("Menu", menu_options)
