import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'lab_records' not in st.session_state:
    st.session_state.lab_records = []
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'blocked_dates' not in st.session_state:
    st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state:
    st.session_state.broadcasts = []

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
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
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
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
    st.sidebar.markdown(f"### 👩‍⚕️ {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    
    dm = st.sidebar.radio("Doctor Panel", ["Manage Appointments", "Patient Lab Reports", "Block Dates", "Broadcast Media"])

    if dm == "Manage Appointments":
        st.header("📅 Patient Bookings")
        if st.session_state.appointments:
            st.table(pd.DataFrame(st.session_state.appointments))
        else:
            st.write("No appointments booked yet.")

    elif dm == "Patient Lab Reports":
        st.header("📋 Review Lab Reports")
        if st.session_state.lab_records:
            st.dataframe(pd.DataFrame(st.session_state.lab_records))
        else:
            st.write("No lab records found.")

    elif dm == "Block Dates":
        st.header("🚫 Block Dates for Clinic")
        b_date = st.date_input("Select Date to Block")
        reason = st.text_input("Reason (Optional)")
        if st.button("Block Date"):
            st.session_state.blocked_dates.append(b_date)
            st.success(f"Date {b_date} blocked.")

    elif dm == "Broadcast Media":
        st.header("📢 Social Media Broadcast")
        v_url = st.text_input("YouTube/Video URL")
        v_desc = st.text_area("Video Description")
        if st.button("Broadcast to Patients"):
            st.session_state.broadcasts.append({"url": v_url, "desc": v_desc})
            st.success("Video broadcasted to all patient dashboards!")

# --- 4. PATIENT DASHBOARD ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment", "Doctor's Broadcasts"])
    
    # 4.1 TRACKER
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
        else:
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    # 4.2 LAB REPORTS
    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Results")
        with st.form("lab_entry"):
            hb = st.number_input("Hemoglobin", 5.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 50, 500, 90)
            if st.form_submit_button("Save"):
                st.session_state.lab_records.append({"Date": date.today(), "Name": st.session_state.name, "Hb": hb, "Sugar": sugar})
                st.success("Added!")

    # 4.3 FULL DETAILED DIET PLANS (Pregnancy & PCOS)
    elif m == "Diet Plans":
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Detailed Pregnancy Trimester Diet")
            tri = st.selectbox("Select Current Trimester", ["1st Trimester (0-12wks)", "2nd Trimester (13-26wks)", "3rd Trimester (27-40wks)"])
            
            if pref == "Vegetarian":
                st.write("**Early Morning:** 5 Soaked Almonds + 1 glass Warm Milk.")
                st.write("**Breakfast:** Veggie Poha OR Moong Dal Chilla OR Paneer Paratha + Curd.")
                st.write("**Mid-Morning:** 1 Fruit (Pomegranate/Apple)
