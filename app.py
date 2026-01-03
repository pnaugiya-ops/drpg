import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import re

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        border-radius: 12px; background-color: #ff4b6b; color: white; 
        font-weight: bold; border: none; height: 3em; width: 100%;
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background-color: #e6f0ff; 
        border-left: 6px solid #003366; color: #003366; margin-bottom: 20px;
    }
    .stExpander { background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; }
    .print-card { padding:20px; border:2px solid #000; font-family:sans-serif; background: white; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: DATA PARSING FOR GRAPHS ---
def extract_val(details, key):
    try:
        match = re.search(f"{key}: ([\d.]+)", str(details))
        return float(match.group(1)) if match else None
    except: return None

# --- 2. LOGIN & WELCOME ---
if not st.session_state.logged_in:
    st.title("🏥 Welcome to Bhavya Labs & Clinics")
    st.markdown("<div class='status-box'><b>Our Comprehensive Services:</b> Obs & Gynae Consultation | Ultrasound | Pharmacy | Thyrocare Franchise (All Blood Tests) | Laparoscopy & Infertility</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.info("📞 Appointment: +91 9676712517")
    col2.info("📧 Email: pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Current Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae/Fertility)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title("Bhavya Clinics")
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin Menu", ["Appointments", "Medical Database", "Broadcast News"])
        if menu == "Appointments":
            st.header("📅 Patient Schedule (15-Min Slots)")
            if not df.empty:
                st.dataframe(df[df['Type']=='APPOINTMENT'].sort_values(by=['Date', 'Time'], ascending=False))
        elif menu == "Medical Database":
            st.header("📋 Master Record")
            st.dataframe(df)

    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Book Appointment", "Lab Trend Tracker", "Vitals & BMI", "Diet & Nutrition", "Baby's Growth & Scans", "Medical Library"])

        # --- DASHBOARD ---
        if menu == "Dashboard":
            st.title(f"Hello, {st.session_state.patient_name}")
            st.markdown(f"<div class='status-box'>Current Profile: <b>{st.session_state.status}</b></div>", unsafe_allow_html=True)
            if st.session_state.status == "Pregnant":
                lmp = st.date_input("Enter LMP (Last Period Date) to track progress")
                edd = lmp + timedelta(days=280)
                weeks = (datetime.now().date() - lmp).days // 7
                c1, c2 = st.columns(2)
                c1.metric("Current Week", f"{weeks} Weeks")
                c2.metric("EDD", edd.strftime("%d %b %Y"))

        # --- 15-MINUTE APPOINTMENT BOOKING ---
        elif menu == "Book Appointment":
            st.header("📅 Book Appointment")
            date = st.date_input("Date", min_value=datetime.now().date())
            
            def get_slots():
                slots = []
                # Morning 11:00 - 14:00 | Evening 18:00 - 20:00
                for h, m in [(h, m) for h in [11, 12, 13, 18, 19] for m in [0, 15, 30, 45]]:
                    slots.append(datetime.strptime(f"{h}:{m}", "%H:%M").strftime("%I:%M %p"))
                return slots

            time = st.selectbox("Select
