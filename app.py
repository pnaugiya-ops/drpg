import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & PERMANENT SIDEBAR ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

# This CSS ensures the Sidebar is visible and hides the 'Edit' buttons
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; min-width: 250px !important; }
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []
if 'blocked_dates' not in st.session_state: st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state: st.session_state.broadcasts = []

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
    dm = st.sidebar.radio("Menu", ["Appointments", "Patient Reports", "Block Dates", "Broadcast"])
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if dm == "Appointments":
        st.header("📅 Appointments")
        st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No bookings")
    elif dm == "Block Dates":
        b_date = st.date_input("Block Clinic Date")
        if st.button("Confirm Block"):
            st.session_state.blocked_dates.append(b_date)
            st.success("Date Blocked")

# --- 4. PATIENT DASHBOARD ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    m = st.sidebar.radio("Go To:", [
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
            
            weeks_data = {
                4: "🌱 Size of a poppy seed.",
                12: "🍋 Size of a lime. Baby starts moving.",
                20: "🍌 Halfway! You may feel kicks.",
                28: "🍆 Eyes can open.",
                40: "🍉 Ready for birth!"
            }
            st.write(weeks_data.get(wks, "🍉 Your baby is growing every day!"))
        else:
            st.header("🩸 Menstrual Cycle Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Diet Plans":
        st.header("🥗 Detailed Diet Chart")
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        if "Pregnant" in st.session_state.stat:
            d1, d2, d3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with d1: st.write("**Early Morning:** Nuts + Warm Milk\n\n**Breakfast:** Veggie Poha/Eggs\n\n**Lunch:** Roti, Dal, Sabzi, Curd")
            with d2: st.write("**Focus:** Iron & Calcium. Add Paneer/Fish and Sprout Salads.")
            with d3: st.write("**Focus:** Energy & Digestion. Small frequent meals.")
        elif "PCOS" in st.session_state.stat:
            st.write("**PCOS Strategy:** High fiber, Low Sugar. Seeds (Flax/Pumpkin) are essential.")

    elif m == "Exercise & Yoga":
        st.header("🧘 Exercise Guidance")
        if "Pregnant" in st.session_state.stat:
            # FIXED LINE 131 BELOW
            st.write("- **Weeks 1-12:** Light Walking (20 mins)")
            st.write("- **Weeks 13-28:** Butterfly Pose, Pelvic Tilts")
            st.write("- **Weeks 29+:** Squats & Birthing Ball")
        else:
            st.write("- Surya Namaskar, Brisk Walking, and Yoga for hormonal balance.")

    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Saved!")

    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure (BP)")
        st.number_input("Pulse Rate", 40, 180, 72)
        if st.button("Log Vitals"): st.success("Vitals Recorded")

    elif m == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        st.selectbox("Select Vaccine", ["TT-1", "TT-2", "Tdap", "Flu Vaccine"])
        st.date_input("Dose Date")
        if st.button("Mark as Done"): st.success("Vaccination logged.")

    elif m == "Book Appointment":
        st.header("📅 Book Clinic Visit")
        dt = st.date_input("Choose Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Clinic is closed on Sunday")
        else:
            st.selectbox("Time Slot", ["11:00 AM", "11:30 AM", "06:00 PM", "06:30 PM"])
            if st.button("Confirm Booking"): st.success("Appointment Confirmed!")
