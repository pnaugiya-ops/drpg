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
    .diet-box { background: #fff5f7; padding: 15px; border-radius: 10px; border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; font-size: 14px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 2px; font-size: 11px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database Connection Error.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div>
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
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}\n\n**Age:** {st.session_state.get('age', 'N/A')}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.write("Access records via Google Sheets.")
    
    else: # Patient View
        m = st.sidebar.radio("Menu", ["Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccination Record", "Book Appointment"])
        
        # 3.1 TRACKER (Source: Here is a week.docx)
        if m == "Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Guide")
                lmp = st.date_input("LMP Date", value=date.today() - timedelta(days=60))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Week: {weeks}")
                
                if weeks <= 4: st.info("🌱 **Week 4 (Poppy Seed):** Snuggling into the womb.")
                elif weeks <= 8: st.info("🍇 **Week 8 (Raspberry):** Fingers and toes sprouting.")
                elif weeks <= 12: st.info("🍋 **Week 12 (Lime):** Baby can make sucking motions.")
                elif weeks <= 20: st.info("🍌 **Week 20 (Banana):** Halfway mark! You'll feel 'flutters'.")
                else: st.info("👶 Baby is growing vital senses daily.")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")
                

        # 3.2 DETAILED DIET (Integrated Detailed Veg/Non-Veg)
        elif m == "Diet Plans":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Diet Chart")
                pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
                st.markdown("<div class='diet-box'><b>Early Morning:</b> Soaked almonds + Warm water.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Stuffed Paratha + Curd.</div>", unsafe_allow_html=True)
                if pref == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>Protein:</b> 2 Boiled Egg Whites (Mid-day) or Chicken/Fish (Lunch).</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> Dal + Seasonal Veggie + 2 Roti + Salad.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Light Chapati + Paneer(Veg) or Grilled Chicken(Non-Veg).</div>", unsafe_allow_html=True)
            else:
                st.header("🌸 PCOS Nutrition")
                st.markdown("<div class='diet-box'><b>PCOS Basics:</b> 50-60g Protein & 25g Fiber daily. Low-GI foods only. Walk 15 mins after meals.</div>", unsafe_allow_html=True)

        # 3.3 EXERCISE (Source: Trimester & Strength docs)
        elif m == "Exercise & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🧘 Trimester Fitness")
                tri = st.selectbox("Select Trimester", ["1st", "
