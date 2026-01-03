import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="GynaeCare Hub", page_icon="🏥", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Security: Set a secret password for the Doctor
DR_PASSWORD = "clinicadmin786" # You can change this to any secret word

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = "Patient"

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 GynaeCare Digital Clinic")
    
    tab1, tab2 = st.tabs(["Patient Portal", "Doctor Login"])
    
    with tab1:
        with st.form("patient_login"):
            name = st.text_input("Full Name")
            status = st.radio("Status", ["Pregnant", "Non-Pregnant / PCOS"])
            if st.form_submit_button("Enter Portal"):
                if name:
                    st.session_state.logged_in = True
                    st.session_state.patient_name = name
                    st.session_state.status = status
                    st.session_state.role = "Patient"
                    st.rerun()

    with tab2:
        with st.form("dr_login"):
            pw = st.text_input("Enter Clinic Password", type="password")
            if st.form_submit_button("Login as Doctor"):
                if pw == DR_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.role = "Doctor"
                    st.session_state.patient_name = "Dr. Admin"
                    st.rerun()
                else:
                    st.error("Incorrect Password")

# --- 3. THE MAIN INTERFACE ---
else:
    st.sidebar.title(f"Logged in: {st.session_state.patient_name}")
    
    # --- DOCTOR ADMIN VIEW ---
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Clinic Management", ["Appointments", "Patient Database", "Post Video/Updates"])
        
        if menu == "Appointments":
            st.header("📅 Today's Appointments")
            df = conn.read(ttl=0)
            if not df.empty and 'Type' in df.columns:
                appts = df[df['Type'] == 'APPOINTMENT'].sort_values(by='Timestamp', ascending=False)
                st.table(appts[['Name', 'Date', 'Time', 'Details']])
            else:
                st.info("No appointments booked yet.")

        elif menu == "Patient Database":
            st.header("📋 Patient Medical Logs")
            df = conn.read(ttl=0)
            st.dataframe(df, use_container_width=True)

    # --- PATIENT VIEW ---
    else:
        menu = st.sidebar.radio("Navigation", ["My Dashboard", "Book Appointment", "Medical Feed", "Diet & Records"])
        
        if menu == "My Dashboard":
            st.title("🤰 My Pregnancy Tracker")
            # [Add the LMP / EDD calculator code here]
            
        elif menu == "Book Appointment":
            st.header("📅 Schedule a Visit")
            # [Add the Mon-Sat / Sun timing logic here]
            if st.button("Confirm Booking"):
                # Logic to save to Google Sheet with Type='APPOINTMENT'
                st.success("Booked! Dr. Admin can see your request now.")

        elif menu == "Medical Feed":
            st.header("🎥 Dr's Educational Feed")
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Example
            st.info("🔔 **Doctor's Note:** New video added on HPV Vaccination benefits!")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
