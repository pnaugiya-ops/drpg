import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 15px; border-radius: 10px; border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; font-size: 12px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database Connection Error.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & CLINIC BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
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

# --- 3. MAIN APPLICATION ---
else:
    # Sidebar
    st.sidebar.markdown(f"**User:** {st.session_state.name} | **Age:** {st.session_state.get('age', 'N/A')}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.write("Access patient records and appointments via Google Sheets.")
    
    else: # Patient View
        m = st.sidebar.radio("Navigation", ["Pregnancy Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccination Record", "Book Appointment"])
        
        # 3.1 PREGNANCY TRACKER (Source: Here is a week.docx)
        if m == "Pregnancy Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Week-by-Week Development")
                lmp = st.date_input("LMP Date", value=date.today() - timedelta(days=60))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Week: {weeks}")
                
                if weeks <= 4: st.info("🌱 **Week 4:** Baby is a poppy seed size, snuggling into the womb.")
                elif weeks <= 8: st.info("🍇 **Week 8:** Raspberry size. Fingers and toes are sprouting.")
                elif weeks <= 12: st.info("🍋 **Week 12:** Lime size. Baby can open/close fists and make sucking motions.")
                elif weeks <= 20: st.info("🍌 **Week 20:** Banana size. Halfway mark! You may feel 'flutters'.")
                elif weeks >= 38: st.info("🍉 **Week 40:** Watermelon size. Full term and ready for birth!")
                else: st.info("👶 Baby is developing senses and vital organs daily.")
                
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=
