import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(
    page_title="Bhavya Labs", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Branding and Navigation Styling */
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; border: 1px solid white; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border:1px solid #e0e0e0; border-left:6px solid #ff4b6b; margin-bottom:15px; line-height: 1.6; color: #333; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; height: 3em; }
    
    /* Ensure Sidebar is prominent */
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; min-width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h2 style='margin:0;'>Dr. Priyanka Gupta</h2>
        <p style='font-size:1.2em;'>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise Lab</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Access", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Patient Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Clinical Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter My Dashboard"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Admin Password", type="password")
            if st.form_submit_button("Login to Clinic Master"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D"})
                    st.rerun()

# --- 3. PATIENT PORTAL (DETAILED) ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}")
    st.sidebar.info(f"Status: {st.session_state.stat}")
    
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Health & Pregnancy Tracker", 
        "Detailed Diet Plans", 
        "Exercise & Yoga Routine", 
        "Lab Reports & Trends", 
        "Vital Signs Monitoring", 
        "Vaccination Schedule", 
        "Book Appointment"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- TRACKER ---
    if m == "Health & Pregnancy Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("Last Menstrual Period (LMP)", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            
            weeks_info = {
                4: "🌱 **Week 4:** Implantation stage. Embryo is size of a poppy seed.",
                12: "🍋 **Week 12:** Organs are fully formed. Risk of miscarriage drops significantly.",
                20: "🍌 **Week 20:** Halfway point! You may start feeling 'quickening' (kicks).",
                28: "🍆 **Week 28:** Third Trimester begins. Baby can open eyes.",
                36: "🍈 **Week 36:** Baby is gaining weight rapidly for birth.",
                40: "🍉 **Week 40:** Full term. Monitor for labor signs."
            }
            st.info(weeks_info.get(wks, "🍉 Your baby is reaching new milestones every day!"))
            

[Image of fetal development stages during pregnancy]

        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracking")
            lp = st.date_input("Start Date of Last Period")
            st.info(f"Next Predicted Cycle: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Date of Delivery")
            days_post = (date.today() - birth_date).days
            st.success(f"Day {days_post} of recovery. Great job, Mom!")

    # --- DETAILED DIET PLANS ---
    elif m == "Detailed Diet Plans":
