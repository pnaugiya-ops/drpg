import streamlit st
import pandas as pd
from datetime import datetime, date, timedelta
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIG & GLOBAL CONNECTION ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

# Central connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_clinic_sheets(p_name, category, detail_text):
    """Saves any data (Appointments/Vitals/Labs) to the cloud sheet"""
    try:
        existing_df = conn.read(worksheet="Appointments", ttl=0)
        new_row = pd.DataFrame([{
            "Name": p_name,
            "Type": category,
            "Details": detail_text,
            "Attachment": "N/A",
            "Timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }])
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        conn.update(worksheet="Appointments", data=updated_df)
        return True
    except:
        return False

# --- 2. UI STYLING ---
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

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'blocked' not in st.session_state: st.session_state.blocked = []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN & BRANDING ---
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

# --- 4. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.markdown(f"### 📋 Patient: {st.session_state.name} ({st.session_state.age} yrs)")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    m = st.segmented_control("SELECT VIEW", options=["Health Tracker", "Cycle Tracker","Diet Plans", "Exercise", "Lab Reports", "Vitals", "Social", "Book Slot"], default="Health Tracker")
    st.divider()

    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks
