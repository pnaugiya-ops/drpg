import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import re

# --- 1. SETUP & HIGH-CONTRAST UI ---
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
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: DATA PARSING ---
def extract_val(details, key):
    try:
        match = re.search(f"{key}: ([\d.]+)", str(details))
        return float(match.group(1)) if match else None
    except: return None

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 Bhavya Labs & Clinics")
    st.markdown("<div class='status-box'><b>Services:</b> Obs & Gynae | Ultrasound | Pharmacy | Thyrocare | Laparoscopy</div>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title("Bhavya Clinics")
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin", ["Appointments", "Medical Database"])
        if menu == "Appointments":
            st.header("📅 Appointments")
            st.dataframe(df[df['Type']=='APPOINTMENT'])
        else:
            st.dataframe(df)

    else:
        menu = st.sidebar.radio("Menu", ["Dashboard", "Lab Tracker", "Vitals & BMI", "Medical Library", "Book Appointment"])

        # --- LAB TRACKER (Hb & TSH GRAPHS) ---
        if menu == "Lab Tracker":
            st.title("🧪 Lab Trend Monitoring")
            with st.form("lab_f"):
                c1, c2, c3 = st.columns(3)
                hb = c1.number_input("Hb %", 5.0, 20.0, 12.0)
                tsh = c2.number_input("TSH", 0.0, 50.0, 2.5)
                urine = c3.selectbox("Urine", ["Normal", "Infection", "Sugar"])
                if st.form_submit_button("Save Labs"):
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "LAB_RESULT", "Details": f"Hb: {hb} | TSH: {tsh} | Urine: {urine}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success("Saved!")
                    st.rerun()

            user_labs = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'LAB_RESULT')].copy()
            if not user_labs.empty:
                user_labs['Hb'] = user_labs['Details'].apply(lambda x: extract_val(x, "Hb"))
                user_labs['TSH'] = user_labs['Details'].apply(lambda x: extract_val(x, "TSH"))
                user_labs['Date'] = pd.to_datetime(user_labs['Timestamp'])
                st.subheader("Hb & TSH Trends")
                st.line_chart(user_labs.set_index('Date')[['Hb', 'TSH']])

        # --- VITALS & BMI ---
        elif menu == "Vitals & BMI":
            st.title("📊 Vitals & BMI")
            with st.form("v_f"):
                c1, c2 = st.columns(2)
                wt = c1.number_input("Weight (kg)", 30.0, 150.0, 60.0)
                ht = c2.number_input("Height (cm)", 100.0, 220.0, 160.0)
                if st.form_submit_button("Calculate BMI"):
                    bmi = round(wt / ((ht/100)**2), 2)
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "VITALS", "Details": f"BMI: {bmi}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
