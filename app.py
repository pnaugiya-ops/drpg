import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .stButton>button { background:#ff4b6b; color:white; font-weight:bold; width:100%; border-radius:10px; }
    .diet-box { background: #fff5f7; padding: 15px; border-radius: 10px; border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 2px; font-size: 11px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Connection Error.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & CLINIC BRANDING ---
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
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":a,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D","name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APP ---
else:
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}\n\n**Age:** {st.session_state.get('age','N/A')}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.write("Access records via Google Sheets.")
    
    else:
        m = st.sidebar.radio("Menu", ["Tracker", "Diet Plans", "Exercise", "Vitals & Vaccines", "Book Appointment"])
        
        # 3.1 TRACKER
        if m == "Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Guide")
                lmp = st.date_input("LMP Date", value=date.today() - timedelta(days=60))
                edd = lmp + timedelta(days=280)
                weeks = (date.today() - lmp).days // 7
                st.success(f"EDD: {edd.strftime('%d %b %Y')} | Week: {weeks}")
                
                
                
                if weeks <= 4: st.info("🌱 Week 4: Implantation stage.")
                elif weeks <= 12: st.info("🍋 Week 12: Baby can open/close fists.")
                elif weeks <= 20: st.info("🍌 Week 20: Halfway! You feel flutters.")
                else: st.info("👶 Baby is growing vital senses.")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")

        # 3.2 DIET (Triple Quoted for Stability)
        elif m == "Diet Plans":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Diet")
                pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
                st.markdown("""<div class='diet-box'>
                    <b>Early Morning:</b> Soaked almonds + Warm water.<br>
                    <b>Breakfast:</b> Veggie Poha / Stuffed Paratha + Curd.</div>""", unsafe_allow_html=True)
                
                if pref == "Non-Vegetarian":
                    st.markdown("""<div class
