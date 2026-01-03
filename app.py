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
    .clinic-name { font-size: 36px; font-weight: bold; }
    .dr-name { font-size: 28px; font-weight: bold; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; color: #003366; }
    .chat-bubble-user { padding: 12px; border-radius: 15px 15px 0px 15px; margin-bottom: 10px; background-color: #f0f2f6; border: 1px solid #ddd; text-align: right; }
    .chat-bubble-ai { padding: 12px; border-radius: 15px 15px 15px 0px; margin-bottom: 10px; background-color: #e6f0ff; border: 1px solid #b3d1ff; text-align: left; color: #003366; }
    .vax-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 10px; }
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

# --- UPGRADED AI ASSISTANT ---
def get_ai_response(query):
    query = query.lower()
    responses = {
        "pain": "Mild cramping is common after Gynae procedures. **Action:** Rest and use prescribed meds. If pain is sharp or you have fever, call Dr. Priyanka immediately.",
        "bleeding": "Spotting is normal for 2-3 days after a Pap smear. **Warning:** If you soak 1 pad/hour, call the clinic emergency number 9676712517.",
        "sugar": "For Fasting Blood Sugar, do not eat/drink anything except water for 8-10 hours before your test.",
        "diet": "Focus on high protein (paneer, eggs, pulses) and 3-4 Liters of water. Avoid outside oily food.",
        "thyroid": "Always take Thyroid meds on an empty stomach, 30 mins before tea. It is vital for baby's brain development.",
        "vaccine": "Vaccines are safe and essential. HPV prevents cervical cancer. T-Dap and Influenza during pregnancy protect both mother and baby.",
        "hpv": "HPV vaccination is best taken between ages 9-26 but can be taken up to 45. It requires 2 or 3 doses depending on age."
    }
    for key in responses:
        if key in query: return responses[key]
    return "Please book a 15-min slot so Dr. Priyanka can review your specific reports in detail."

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><div class='clinic-name'>BHAVYA LABS & CLINICS</div><div class='dr-name'>Dr. Priyanka Gupta</div><div style='font-size:20px; color:#ff4b6b;'>MS (Obs & Gynae)</div><div style='font-size:16px; color:#ced4da;'>Infertility Specialist & Laparoscopic Surgeon</div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Patient Name")
            status = st.radio("Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter"):
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role = True, "Doctor"
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "Doctor":
        st.title("👨‍⚕️ Admin Dashboard")
        t1, t2 = st.tabs(["Records", "Schedule"])
        with t1: st.dataframe(df.sort_values(by='Timestamp', ascending=False))
        with t2:
            c1, c2 = st.columns(2)
            with c1:
                b_dt = st.date_input("Block Date", min_value=datetime.now().date())
                if st.button("Confirm Block"):
                    new = pd.DataFrame([{"Name": "ADMIN", "Type": "BLOCK", "Date": str(b_dt), "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()
            with c2:
                for i, r in df[df['Type'] == 'BLOCK'].iterrows():
                    if st.button(f"❌ Unblock {r['Date']}", key=f"un_{i}"):
                        conn.update(data=df.drop(i)); st.rerun()
    else
