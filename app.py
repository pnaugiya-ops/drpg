import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os

# --- 0. DATA PERSISTENCE HELPERS ---
# This function ensures data is saved to a file so all users see it
def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

def save_data(df, filename):
    df.to_csv(filename, index=False)

# File names for global storage
APTS_FILE = "appointments_db.csv"
LABS_FILE = "labs_db.csv"
VITALS_FILE = "vitals_db.csv"

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; border: 1px solid white; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border:1px solid #e0e0e0; border-left:6px solid #ff4b6b; margin-bottom:15px; line-height: 1.6; color: #333; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; height: 3em; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States for UI flow
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}
if 'blocked' not in st.session_state: st.session_state.blocked = []

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
            age = st.number_input("Age", 18, 100, 25)
            s = st.radio("Clinical Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter My Dashboard"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":age,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Admin Password", type="password")
            if st.form_submit_button("Login to Clinic Master"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D"})
                    st.rerun()

# --- 3. PATIENT PORTAL ---
elif st.session_state.role == "P":
    head_l, head_r = st.columns([3, 1])
    with head_l:
        st.markdown(f"### 📋 Patient: {st.session_state.name} ({st.session_state.age} yrs)")
        st.caption(f"Status: {st.session_state.stat}")
    with head_r:
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

    m = st.segmented_control(
        "SELECT VIEW", 
        options=["Health Tracker", "Diet Plans", "Exercise", "Lab Reports", "Vitals", "Social", "Book Slot"],
        default="Health Tracker"
    )
    st.divider()

    # (Previous sections Diet Plans, Exercise etc. remain the same)
    # ... [Keep your diet and exercise logic here] ...

    if m == "Lab Reports":
        st.header("📊 Lab Tracking")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 90)
            if st.form_submit_button("Save Report"):
                df_labs = load_data(LABS_FILE, ["User", "Date", "Hb", "Sugar"])
                new_row = pd.DataFrame([{"User": st.session_state.name, "Date": date.today(), "Hb": hb, "Sugar": sugar}])
                save_data(pd.concat([df_labs, new_row]), LABS_FILE)
                st.success("Report Saved Globally!")

    elif m == "Book Slot":
        st.header("📅 Select Time Slot")
        slots = [f"{h}:{m:02d} AM" for h in [11] for m in [15, 30, 45]] + [f"{h}:{m:02d} PM" for h in [12, 1, 6, 7] for m in [0, 15, 30, 45]]
        d = st.date_input("Date", min_value=date.today())
        t = st.selectbox("Slot", slots)
        if st.button("Request Booking"):
            # Load global appointments
            df_apts = load_data(APTS_FILE, ["Patient", "Date", "Time"])
            new_apt = pd.DataFrame([{"Patient": st.session_state.name, "Date": str(d), "Time": t}])
            save_data(pd.concat([df_apts, new_apt]), APTS_FILE)
            st.success("Booking Request Sent Successfully! The Doctor can now see this.")

# --- 4. ADMIN PORTAL ---
elif st.session_state.role == "D":
    adm_l, adm_r = st.columns([3, 1])
    with adm_l:
        st.title("👩‍⚕️ Admin Master")
    with adm_r:
        if st.button("Log Out", key="admin_logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

    t1, t2, t3, t4 = st.tabs(["Appointments", "Patient Records", "Clinic Availability", "Social Media"])
    
    with t1:
        st.subheader("Live Bookings")
        df_view = load_data(APTS_FILE, ["Patient", "Date", "Time"])
        if not df_view.empty:
            st.dataframe(df_view, use_container_width=True)
            if st.button("Clear All Appointments"):
                save_data(pd.DataFrame(columns=["Patient", "Date", "Time"]), APTS_FILE)
                st.rerun()
        else:
            st.info("No Bookings available yet.")

    with t2:
        st.subheader("Global Lab Records")
        st.dataframe(load_data(LABS_FILE, ["User", "Date", "Hb", "Sugar"]))
