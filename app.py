import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import re

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    .dr-header { 
        background-color: #003366; color: white; padding: 30px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
        border-bottom: 5px solid #ff4b6b;
    }
    .clinic-name { font-size: 36px; font-weight: bold; letter-spacing: 1px; }
    .dr-name { font-size: 28px; font-weight: bold; margin-top: 10px; }
    .dr-degree { font-size: 20px; color: #ff4b6b; font-weight: bold; }
    .dr-spec { font-size: 16px; color: #ced4da; font-style: italic; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; }
    .chat-bubble-user { padding: 12px; border-radius: 15px 15px 0px 15px; margin-bottom: 10px; background-color: #f0f2f6; border: 1px solid #ddd; text-align: right; }
    .chat-bubble-ai { padding: 12px; border-radius: 15px 15px 15px 0px; margin-bottom: 10px; background-color: #e6f0ff; border: 1px solid #b3d1ff; text-align: left; color: #003366; }
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

# --- UPGRADED AI ASSISTANT LOGIC ---
def get_interactive_ai_response(query):
    query = query.lower()
    responses = {
        "pain": "Mild lower abdominal cramping is common after procedures like D&C or Biopsy. **Action:** Rest and use prescribed analgesics. If pain is sharp, constant, or accompanied by fever (>100°F), please contact Dr. Priyanka immediately.",
        "bleeding": "Spotting is normal for 2-3 days after a Pap smear or biopsy. **Warning:** If you are soaking more than one pad per hour or seeing large clots, this is an emergency. Please call 9676712517.",
        "sugar": "For an accurate Fasting Blood Sugar test, please do not consume anything except water for 8-10 hours before the test.",
        "diet": "1. **Protein:** Include paneer, pulses, or eggs. \n2. **Hydration:** 3-4 Liters of water daily. \n3. **Avoid:** Excess salt, sugar, and processed 'maida' foods.",
        "thyroid": "TSH levels are crucial during pregnancy. If your TSH is high, it may affect baby's development. Always take your Thyronorm/Eltroxin on an empty stomach 30 mins before tea.",
        "scan": "1. **NT/NB Scan:** Done between 11-13 weeks (checks for chromosomal issues). \n2. **TIFFA/Anomaly Scan:** Done between 18-20 weeks (detailed organ check).",
        "pcos": "PCOS management requires a Low GI diet and at least 30 mins of brisk walking. Focus on reducing weight to improve ovulation cycles."
    }
    for key in responses:
        if key in query: return responses[key]
    return "I am here to help with general doubts about your reports and symptoms. For this specific query, I recommend booking a quick 15-minute consultation so Dr. Priyanka can review your history."

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'><div class='clinic-name'>BHAVYA LABS & CLINICS</div><div class='dr-name'>Dr. Priyanka Gupta</div><div class='dr-degree'>MS (Obstetrics & Gynaecology)</div><div class='dr-spec'>Infertility Specialist & Laparoscopic Surgeon</div></div>""", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Profile Type", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter My Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. CLINIC INTERFACE ---
else:
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        st.title("👨‍⚕️ Admin: Bhavya Labs & Clinics")
        adm_tabs = st.tabs(["Patient Records", "Manage Schedule"])
        with adm_tabs[0]: st.dataframe(df.sort_values(by='Timestamp', ascending=False))
        with adm_tabs[1]:
            c1, c2 = st.columns(2)
            with c1:
                b_date = st.date_input("Block Date", min_value=datetime.now().date())
                if st.button("Confirm Block"):
                    new_row = pd.DataFrame([{"Name": "ADMIN", "Type": "BLOCKED_DATE", "Date": str(b_date), "Details": "Doctor Unavailable", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True)); st.rerun()
            with c2:
                blocked_df = df[df['Type'] == 'BLOCKED_DATE']
                for i, r in blocked_df.iterrows():
                    if st.button(f"❌ Unblock {r['Date']}", key=f"un_{i}"):
                        conn.update(data=df.drop(i)); st.rerun()

    else:
        st.sidebar.markdown(f"**BHAVYA CLINICS**\nDr. Priyanka Gupta")
        menu = st.sidebar.radio("Navigation", ["Dashboard", "AI Assistant", "Lab Trend Tracker", "Vitals & BMI", "Medical Library", "Book Appointment"])

        # --- DASHBOARD ---
        if menu == "Dashboard":
            st.title(f"Welcome, {st.session_state.patient_name}")
            st.markdown(f"<div class='status
