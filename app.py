import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

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
except Exception:
    st.error("Database Connection Error.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN SYSTEM ---
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
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            pass_in = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APP ---
else:
    # Always show Logout in Sidebar
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    try:
        df = conn.read(ttl=0)
        df = df.fillna('') if df is not None else pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])
    except:
        df = pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        st.write("View Patient Appointments and Reports in Google Sheets.")
    
    else: # Patient Portal
        st.sidebar.markdown(f"### Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Book Appointment", "Vitals & BMI", "Upload Reports"])
        
        # --- 3.1 TRACKER & BABY GUIDE ---
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Week-by-Week Guide")
                lmp = st.date_input("Select LMP", value=date.today() - timedelta(days=30))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Stage: {weeks} Weeks")
                
                # Logic from "Here is a week.docx"
                if weeks <= 4: st.info("🌱 **Week 4 (Poppy Seed):** Tiny ball of cells snuggling into the womb.")
                elif weeks <= 5: st.info("💓 **Week 5 (Sesame Seed):** Brain, spine, and heart start forming.")
                elif weeks <= 8: st.info("🍇 **Week 8 (Raspberry):** Fingers and toes are sprouting.")
                elif weeks <= 12: st.info("🍋 **Week 12 (Lime):** Baby can open/close fists and make sucking motions.")
                elif weeks <= 20: st.info("🍌 **Week 20 (Banana):** Halfway mark! You will feel 'flutters'.")
                elif weeks <= 27: st.info("🥦 **Week 27 (Cauliflower):** Baby can open/blink eyes and has sleep cycles.")
                elif weeks <= 34: st.info("🍈 **Week 34 (Cantaloupe):** Putting on fat to stay warm; skin not see-through.")
                elif weeks >= 38: st.info("🍉 **Week 40 (Watermelon):** Full term and ready for the world!")
                else: st.info("👶 Baby is growing fast and developing senses.")
                            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=28))
                st.success(f"🩸 Next Period Expected: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")

        # --- 3.2 DIET & EXERCISE (FROM DOCUMENTS) ---
        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Exercise & Nutrition")
                t1, t2 = st.tabs(["🥗 Nutrition", "🧘 Exercises"])
                with t1:
                    st.markdown("""<div class='diet-box'><b>General Focus:</b><br>
                    - Early Morning: Warm water + 4-5 soaked almonds.<br>
                    - Breakfast: Veggie Poha / Upma + Milk.<br>
                    - Lunch: Brown rice + Dal + Sautéed Veggies.<br>
                    - Dinner: Chapati + Rajma/Chole + Curd.</div>""", unsafe_allow_html=True)
                with t2:
                    # Data from "Below are basic exercises recommended for each trimester.docx"
                    tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                    if "1st" in tri:
                        st.write("**Focus:** Fatigue & Breath awareness.")
                        st.write("- Walking & Prenatal Yoga\n- Pelvic Floor (Kegels)\n- Cat-Cow Stretch")
                    elif "2nd" in tri:
                        st.write("**Focus:** Moderate resistance & balance.")
                        st.
