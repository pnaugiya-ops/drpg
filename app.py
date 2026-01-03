import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import re

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    .dr-header { 
        background-color: #003366; color: white; padding: 25px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
    }
    .dr-name { font-size: 30px; font-weight: bold; }
    .dr-degree { font-size: 20px; color: #ff4b6b; font-weight: bold; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; }
    .chat-bubble { padding: 10px; border-radius: 15px; margin-bottom: 10px; background-color: #f0f2f6; border: 1px solid #ddd; }
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

# --- AI FAQ ASSISTANT LOGIC ---
def get_ai_response(query):
    query = query.lower()
    if "pain" in query: return "Mild cramping is normal after procedures, but severe pain with fever requires immediate clinic contact."
    elif "bleeding" in query: return "Spotting can occur after Pap Smear or Biopsy. If bleeding is heavier than a period, please call Dr. Priyanka."
    elif "diet" in query: return "Stick to light, home-cooked meals. Avoid spicy food and stay hydrated with 3-4 liters of water."
    elif "scan" in query: return "Important scans include NT/NB (11-13 weeks) and TIFFA (18-20 weeks). Please check the 'Baby Growth' section for details."
    elif "fasting" in query: return "For Blood Sugar (Fasting), do not eat for 8-10 hours. For Ultrasound, usually a full bladder is required."
    else: return "That's a good question. For specific medical advice, please discuss this during your next 15-minute slot with Dr. Priyanka Gupta."

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><div class='dr-name'>Dr. Priyanka Gupta</div><div class='dr-degree'>MS (Obs & Gynae)</div><div style='color:#e0e0e0;'>Obstetrician & Gynecologist | Infertility Specialist | Laparoscopic Surgeon</div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Current Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
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
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin", ["Appointments", "Medical Database"])
        if menu == "Appointments":
            st.dataframe(df[df['Type']=='APPOINTMENT'])
        else:
            st.dataframe(df)
    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "AI Health Assistant", "Book Appointment", "Lab Trend Tracker", "Vitals & BMI", "Diet & Nutrition", "Baby's Growth & Scans", "Medical Library"])

        # --- AI FAQ ASSISTANT ---
        if menu == "AI Health Assistant":
            st.title("🤖 Bhavya AI FAQ Assistant")
            st.write("Ask common questions about your pregnancy, procedures, or reports.")
            user_q = st.text_input("Type your doubt here (e.g., 'What to eat?' or 'Is bleeding normal?')")
            if user_q:
                response = get_ai_response(user_q)
                st.markdown(f"<div class='chat-bubble'><b>You:</b> {user_q}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-bubble' style='background-color:#e6f0ff;'><b>AI Assistant:</b> {response}</div>", unsafe_allow_html=True)

        # --- UPDATED MEDICAL LIBRARY ---
        elif menu == "Medical Library":
            st.title("📚 Procedure & Health Library")
            
            with st.expander("🔬 Diagnostic & Screening"):
                st.write("**Pap Smear:** A simple test to screen for cervical cancer. Recommended for all women.")
                st.write("**Endometrial Biopsy:** Taking a small tissue sample from the uterine lining to check for abnormal cells.")
            
            with st.expander("🏥 Surgical Procedures"):
                st.write("**D&C (Dilation & Curettage):** Procedure to remove tissue from inside the uterus.")
                st.write("**MTP (Medical Termination of Pregnancy):** Safe and confidential services for pregnancy termination.")
                st.write("**Laparoscopy:** Keyhole surgery for cysts, fibroids, and infertility checks.")
                st.write("**Suction & Evacuation:** A safe method used for certain gynaecological requirements.")

            with st.expander("💉 Vaccinations"):
                st.write("- **Tetanus (TT):** Prevents maternal and neonatal tetanus.")
                st.write("- **HPV Vaccine:** Protects against cervical cancer. Best taken early or during lactation.")

        # --- LAB TRACKER (Hb, TSH, Sugar, Urine) ---
        elif menu == "Lab Trend Tracker":
            st.title("🧪 Visit-wise Lab History")
            with st.form("lab_f"):
                c1, c2, c3, c4 = st.columns(4)
                hb = c1.number_input("Hb %", 5.0, 18.0, 11.0)
                tsh = c2.number_input("TSH", 0.0, 50.0, 2.5)
                sugar = c3.number_input("Blood
