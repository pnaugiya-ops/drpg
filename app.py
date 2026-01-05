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
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 15px; margin-bottom: 10px; }
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

# --- 2. LOGIN & CLINIC DASHBOARD ---
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
            <span class='clinic-badge'>Thyrocare Franchise</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "age":a, "stat":s, "role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APP ---
else:
    # Sidebar Logout & Profile
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}")
    if st.session_state.role == "P":
        st.sidebar.markdown(f"**Age:** {st.session_state.age}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor's Dashboard")
        st.info("Clinic Management & Patient Records Access")
    
    else: # Patient View
        m = st.sidebar.radio("Navigation", ["Pregnancy/Period Tracker", "Detailed Diet Plan", "Yoga & Exercise", "Vaccination Portal", "Vitals & BMI", "Book Appointment", "Upload Reports"])
        
        # 3.1 TRACKER (Using "Here is a week.docx")
        if m == "Pregnancy/Period Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Week-by-Week Guide")
                lmp = st.date_input("LMP Date", value=date.today() - timedelta(days=60))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ You are at {weeks} Weeks")
                
                if weeks <= 4: st.info("🌱 **Week 4 (Poppy Seed):** Tiny ball of cells snuggling into the womb.")
                elif weeks <= 8: st.info("🍇 **Week 8 (Raspberry):** Fingers and toes sprouting; baby makes jerky movements.")
                elif weeks <= 12: st.info("🍋 **Week 12 (Lime):** Baby can open/close fists and make sucking motions.")
                elif weeks <= 20: st.info("🍌 **Week 20 (Banana):** Halfway mark! You will feel the first flutters.")
                elif weeks <= 27: st.info("🥦 **Week 27 (Cauliflower):** Baby begins regular sleep/wake cycles.")
                elif weeks >= 38: st.info("🍉 **Week 40 (Watermelon):** Full term! Lungs and brain are mature.")
                else: st.info("👶 Your baby is growing and developing vital senses daily.")
                
            else:
                st.header("🗓️ Menstrual Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")

        # 3.2 DETAILED DIET PLAN (Restored)
        elif m == "Detailed Diet Plan":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Nutrition Chart")
                diet_type = st.radio("Choose Diet Preference", ["Vegetarian", "Non-Vegetarian"])
                
                with st.container():
                    st.markdown("<div class='diet-box'><b>Early Morning:</b> Soaked almonds + Glass of warm water.</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Oats / Stuffed Paratha + Curd.</div>", unsafe_allow_html=True)
                    if diet_type == "Non-Vegetarian":
                        st.markdown("<div class='diet-box'><b>Mid-Day:</b> 2 Boiled Egg Whites or Chicken Soup.</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Chapati + Dal + seasonal Veggie + Salad.</div>", unsafe_allow_html=True)
                    if diet_type == "Non-Vegetarian":
                        st.markdown("<div class='diet-box'><b>Dinner Option:</b> Grilled Fish or Lean Chicken with Steamed Veggies.</div>", unsafe_allow_html=
