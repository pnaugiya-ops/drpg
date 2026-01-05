import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 15px; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; font-size: 12px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Database Connection Error. Please check secrets.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & CLINIC INFO ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Blood Test</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            age = st.number_input("Age", 1, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "age":age, "stat":s, "role":"P"})
                    st.rerun()
                else: st.warning("Please enter your name")
    with t2:
        with st.form("d_login"):
            pass_in = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()
                else: st.error("Access Denied")

# --- 3. MAIN APP ---
else:
    # Load Data Safely
    try:
        df = conn.read(ttl=0)
        df = df.fillna('') if df is not None else pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])
    except:
        df = pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])

    # --- DOCTOR VIEW ---
    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
        
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📢 Broadcast"])
        
        with t_adm[0]:
            apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().str.contains(search))]
            for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)

    # --- PATIENT VIEW ---
    else:
        st.sidebar.markdown(f"### Hello, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Vaccine Portal", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        # 1. Tracker & Calculator
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("👶 Pregnancy Tracker")
                lmp = st.date_input("Select LMP", value=date.today() - timedelta(days=30))
                edd = lmp + timedelta(days=280)
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ **EDD:** {edd.strftime('%d %B %Y')} | ⏳ **Stage:** {weeks} Weeks")
                
                st.divider()
                st.subheader("📖 Week-by-Week Baby Development")
                if weeks <= 4: st.write("🌱 **Week 4 (Poppy Seed):** Baby is a tiny ball of cells snuggling into the womb.")
                elif weeks <= 5: st.write("💓 **Week 5 (Sesame Seed):** Heart tube begins to pulse.")
                elif weeks <= 8: st.write("🍇 **Week 8 (Raspberry):** Fingers and toes are starting to sprout.")
                elif weeks <= 12: st.write("🍋 **Week 12 (Lime):** Baby can open/close fists and make sucking motions.")
                elif weeks <= 20: st.write("🍌 **Week 20 (Banana):** Halfway mark! You feel the first 'flutters'.")
                elif weeks <= 27: st.write("🥦 **Week 27 (Cauliflower):** Baby begins to develop a sleep/wake schedule.")
                elif weeks >= 38: st.write("🍉 **Week 40 (Watermelon):** Full term! Ready for birth.")
                else: st.write("👶 Baby is growing fast and getting stronger every day.")
                
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=28))
                st.success(f"🩸 **Next Period:** {(lp + timedelta(days=28)).strftime('%d %b %Y')}")
                

        # 2. Diet & Yoga (Data from your exact documents)
        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness Hub")
                t1, t2 = st.tabs(["🥗 Nutrition", "🧘 Exercises"])
                with t1:
                    tri = st.selectbox("Select Trimester
