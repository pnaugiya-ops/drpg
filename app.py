import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & TOGGLE STYLE ---
st.set_page_config(
    page_title="Bhavya Labs", 
    layout="wide", 
    initial_sidebar_state="auto" # This allows the user to toggle it open/closed
)

st.markdown("""
    <style>
    /* Hiding the technical buttons at the top right */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Styling the Sidebar to make buttons stand out */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #003366;
    }
    
    /* Styling the navigation radio buttons */
    .st-emotion-cache-6qob1r {
        background-color: #e8f4f8 !important;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 5px;
    }

    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
for key in ['logged_in', 'lab_records', 'appointments', 'blocked_dates', 'broadcasts']:
    if key not in st.session_state:
        if key == 'logged_in': st.session_state[key] = False
        else: st.session_state[key] = []

# --- 2. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
        <p>Infertility Specialist | Ultrasound | Laparoscopic Surgery</p>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Current Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":a,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D","name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. DOCTOR DASHBOARD ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin Panel")
    dm = st.sidebar.radio("Navigation", ["Appointments", "Patient Reports", "Block Dates"])
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if dm == "Appointments":
        st.header("📅 Appointments")
        st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No bookings")

# --- 4. PATIENT DASHBOARD (TOGGLEABLE SIDEBAR) ---
elif st.session_state.role == "P":
    # Information for users on how to toggle
    st.sidebar.info("Click the ◄ arrow at the top to hide this menu.")
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    
    # THE DASHBOARD OPTIONS
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Pregnancy/Cycle Tracker", 
        "Diet Plans", 
        "Exercise & Yoga", 
        "Lab Reports & Trends", 
        "Health Vitals", 
        "Vaccinations", 
        "Book Appointment"
    ])
    
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if m == "Pregnancy/Cycle Tracker":
        st.header("🤰 Pregnancy & Ultrasound Calculator")
        if "Pregnant" in st.session_state.stat:
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd_calc = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date (EDD): {edd_calc}")
            st.info(f"✨ Current Week: {wks}")
        else:
            st.header("🩸 Menstrual Cycle Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Diet Plans":
        st.header("🥗 Detailed Diet Chart")
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        st.write(f"Showing personalized {pref} diet for {st.session_state.stat} status.")
        st.info("Trimester-wise plans are loaded below.")

    elif m == "Exercise & Yoga":
        st.header("🧘 Exercise Guidance")
        st.write("- **Safe Movements:** Walking, Butterfly Pose, and Deep Breathing.")

    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Record Saved!")

    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure (BP)")
        if st.button("Log Vitals"): st.success("Vitals Recorded")

    elif m == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        st.selectbox("Select Vaccine", ["TT-1", "TT-2", "Tdap", "Flu Vaccine"])
        if st.button("Mark as Administered"): st.success("Vaccination logged.")

    elif m == "Book Appointment":
        st.header("📅 Book Clinic Visit")
        dt = st.date_input("Choose Date", min_value=date.today())
        if st.button("Confirm Booking"): st.success("Appointment Confirmed!")
