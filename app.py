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
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton>button { 
        border-radius: 12px; 
        background-color: #ff4b6b; 
        color: white; 
        font-weight: bold;
        border: none;
        height: 3em;
        width: 100%;
    }
    .status-box { 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #e6f0ff; 
        border-left: 6px solid #003366;
        color: #003366;
        margin-bottom: 20px;
    }
    .stExpander { background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: GRAPH PARSING LOGIC ---
def extract_val(details, key):
    try:
        match = re.search(f"{key}: ([\d.]+)", str(details))
        return float(match.group(1)) if match else None
    except: return None

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 Bhavya Labs & Clinics")
    st.markdown("<div class='status-box'><b>Our Services:</b> Obs & Gynae Consultation | Ultrasound | Pharmacy | Thyrocare Franchise | Laparoscopy & Infertility</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.info("📞 Contact: 9676712517")
    col2.info("📧 Email: pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Are you currently pregnant?", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter My Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name = True, name
                st.session_state.status, st.session_state.role = status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Enter Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title("Bhavya Clinics")
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin Menu", ["Appointments", "Medical Database", "Post Updates"])
        if menu == "Appointments":
            st.header("📅 Patient Schedule")
            st.dataframe(df[df['Type']=='APPOINTMENT'].sort_values(by='Timestamp', ascending=False))
        elif menu == "Medical Database":
            st.header("📋 All Patient Records")
            st.dataframe(df)

    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Lab Test Tracking", "Vitals & BMI Tracker", "Medical Library", "Diet Plans", "Book Appointment"])

        # --- LAB TRACKER (Hb & TSH GRAPHS) ---
        if menu == "Lab Test Tracking":
            st.title("🧪 Lab Trend Monitoring")
            st.write("Keep track of your blood work (Hb and TSH).")
            
            with st.form("lab_form"):
                c1, c2, c3 = st.columns(3)
                hb = c1.number_input("Hemoglobin (Hb %)", 5.0, 20.0, 12.0)
                tsh = c2.number_input("Thyroid (TSH level)", 0.0, 50.0, 2.5)
                urine = c3.selectbox("Urine Test", ["Normal", "Infection", "Sugar Found"])
                if st.form_submit_button("Save Lab Results"):
                    lab_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "LAB_RESULT", "Details": f"Hb: {hb} | TSH: {tsh} | Urine: {urine}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, lab_row], ignore_index=True))
                    st.success("Lab data saved.")
                    st.rerun()

            # Graphing Lab Trends
            user_labs = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'LAB_RESULT')].copy()
            if len(user_labs) >= 1:
                user_labs['Hb'] = user_labs['Details'].apply(lambda x: extract_val(x, "Hb"))
                user_labs['TSH'] = user_labs['Details'].apply(lambda x: extract_val(x, "TSH"))
                user_labs['Date'] = pd.to_datetime(user_labs['Timestamp'])
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.subheader("Hemoglobin (Hb) Trend")
                    st.line_chart(user_labs.set_index('Date')['Hb'])
                with col_g2:
                    st.subheader("Thyroid (TSH) Trend")
                    st.line_chart(user_labs.set_index('Date')['TSH'])

        # --- VITALS & BMI (BMI GRAPH) ---
        elif menu == "Vitals & BMI Tracker":
            st.title("📊 Vitals & BMI Progress")
            with st.form("vitals_form"):
                c1, c2, c3, c4 = st.columns(4)
                wt = c1.number_input("Weight (kg)", 30.0, 150.0, 60.0)
                ht = c2.number_input("Height (cm)", 100.0, 220.0, 160.0)
                pulse = c3.number_input("Pulse", 40, 180, 72)
                bp = c4.text_input("BP", "120/80")
                if st.form_submit_button("Save & Calculate"):
                    bmi = round(wt / ((ht/100)**2), 2)
                    v_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "VITALS", "Details": f"BMI: {bmi} | Pulse: {pulse} | BP: {bp}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, v_row], ignore_index=True))
                    st.success(f"BMI Calculated: {bmi}")
                    st.rerun()

            # Graphing BMI Trend
            user_vitals = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'VITALS')].copy()
            if len(user_vitals) >= 1:
                user_vitals['BMI'] = user_vitals['Details'].apply(lambda x: extract_val(x, "BMI"))
                user_vitals['Date'] = pd.to_datetime(user_vitals['Timestamp'])
                st.subheader("BMI Trend Over Time")
                st.line_chart(user_vitals.set_index('Date')['BMI'])

        # --- OTHER MENUS (Existing Logic) ---
        elif menu == "Dashboard":
            st.title(f"Welcome, {st.session_state.patient_name}")
            st.markdown(f"<div class='status-box'>Profile: <b>{st.session_state.status}</b></div>", unsafe_allow_html=True)
            # Add News/Broadcast check here

        elif menu == "Book Appointment":
            st.header("📅 Schedule a Visit")
            st.checkbox("Request Thyrocare Blood Test Package")
            date = st.date_input("Select Date")
            time = st.selectbox("Slot", ["11:00 AM", "12:00 PM", "06:00 PM", "07:00 PM"])
            if st.button("Confirm"):
                new_row = pd.DataFrame([{"Name":st.session_state.patient_name
