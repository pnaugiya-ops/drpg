import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. SETUP & DESIGN ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")

# Force Light Mode & Styles to prevent "Black Screen" issues
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #ffffff; color: #000000; }
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .stButton>button { background:#ff4b6b; color:white; font-weight:bold; width:100%; border-radius:10px; }
    .diet-box { background: #fff5f7; padding: 15px; border-radius: 10px; border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; }
    .info-card { background: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Database Setup (Safe Mode)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("⚠️ Database connection missing. Check secrets.toml.")

# Initialize Session State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'name' not in st.session_state: st.session_state.name = "Guest"
if 'stat' not in st.session_state: st.session_state.stat = "PCOS/Gynae"

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>Infertility Specialist | Ultrasound | Laparoscopy | Pharmacy</p>
    </div>""", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👤 Patient Login", "🩺 Doctor Login"])
    
    with tab1:
        with st.form("patient_login"):
            name = st.text_input("Enter Full Name")
            age = st.number_input("Age", 18, 100, 25)
            status = st.radio("Patient Type", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Login to Portal"):
                if name:
                    st.session_state.logged_in = True
                    st.session_state.name = name
                    st.session_state.age = age
                    st.session_state.stat = status
                    st.session_state.role = "P"
                    st.rerun()
                else:
                    st.warning("Please enter your name.")

    with tab2:
        with st.form("doctor_login"):
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Doctor Access"):
                if pwd == "clinicadmin786":
                    st.session_state.logged_in = True
                    st.session_state.role = "D"
                    st.rerun()
                else:
                    st.error("Wrong Password")

# --- 3. DASHBOARD (LOGGED IN) ---
else:
    # Sidebar
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.session_state.role == "P":
        st.sidebar.write(f"**Status:** {st.session_state.stat}")
        st.sidebar.write(f"**Age:** {st.session_state.get('age', 'N/A')}")
    
    if st.sidebar.button("🔓 Logout", key="logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- DOCTOR VIEW ---
    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.info("System is active. View Google Sheets for live data.")

    # --- PATIENT VIEW ---
    else:
        # Menu
        menu = st.sidebar.radio("Select Section:", 
            ["Tracker", "Diet Charts", "Exercise Plan", "My Vitals", "Vaccinations", "Book Appointment"])

        # === SECTION 1: TRACKER ===
        if menu == "Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Tracker")
                lmp = st.date_input("Select LMP Date", value=date.today() - timedelta(days=60))
                weeks = (date.today() - lmp).days // 7
                st.success(f"You are **{weeks} Weeks** Pregnant | EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')}")
                
                # Content from 'Here is a week.docx'
                if weeks <= 4: st.info("🌱 **Week 4:** Poppy Seed size. Implantation occurring.")
                elif weeks <= 8: st.info("🍇 **Week 8:** Raspberry size. Fingers forming.")
                elif weeks <= 12: st.info("🍋 **Week 12:** Lime size. Reflexes developing.")
                elif weeks <= 20: st.info("🍌 **Week 20:** Banana size. You might feel movement!")
                elif weeks >= 38: st.info("🍉 **Week 40:** Watermelon size. Ready for birth.")
                else: st.info("👶 Baby is growing steadily.")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=25))
                st.info(f"🩸 Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        # === SECTION 2: DIET ===
        elif menu == "Diet Charts":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Nutrition Plan")
                d_type = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
                
                st.markdown("<div class='diet-box'><b>🌅 Early Morning:</b> Soaked Almonds (5) + Warm Water</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>🥣 Breakfast:</b> Veggie Poha / Upma / Stuffed Paratha + Curd</div>", unsafe_allow_html=True)
                
                if d_type == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>🍗 Lunch:</b> 2 Rotis + Chicken/Fish Curry + Salad</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet
