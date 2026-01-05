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
    st.error("Database connection issue.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN LOGIC ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
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
    # Sidebar Logout
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        st.info("Check Google Sheets for appointment logs.")
    
    else: # Patient View
        st.sidebar.markdown(f"### Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Book Appointment", "Vitals & BMI", "Upload Reports"])
        
        # 3.1 TRACKER (Milestones from "Here is a week.docx")
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Week-by-Week Guide")
                lmp = st.date_input("Select LMP", value=date.today() - timedelta(days=30))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Stage: {weeks} Weeks")
                
                if weeks <= 4:
                    st.info("🌱 **Week 1-4 (The Seed):** Baby is a tiny ball of cells the size of a poppy seed.")
                elif weeks <= 5:
                    st.info("💓 **Week 5 (The Heartbeat):** Size of a sesame seed. The tiny heart tube begins to pulse.")
                elif weeks <= 8:
                    st.info("🍇 **Week 8 (Moving Around):** Size of a raspberry. Fingers and toes are sprouting.")
                elif weeks <= 12:
                    st.info("🍋 **Week 11-12 (Reflexes):** Size of a lime. Baby can open/close fists and make sucking motions.")
                elif weeks <= 20:
                    st.info("🍌 **Week 20 (Halfway Mark):** Size of a banana. You feel the first 'flutters'.")
                elif weeks <= 27:
                    st.info("🥦 **Week 27 (Opening Eyes):** Size of cauliflower. Baby develops a sleep/wake schedule.")
                elif weeks <= 34:
                    st.info("🍈 **Week 34 (Filling Out):** Size of a cantaloupe. Baby is putting on fat to stay warm.")
                elif weeks >= 38:
                    st.info("🍉 **Week 40 (Full Term):** Size of a watermelon. Ready for the world!")
                else:
                    st.info("👶 Baby is growing fast and developing vital senses.")
                
            else:
                st.header("🗓️ Menstrual Cycle Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=28))
                st.success(f"🩸 Next Period: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")

        # 3.2 DIET & YOGA (From Pregnancy & PCOS Docs)
        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness Hub")
                d_tab, e_tab = st.tabs(["🥗 Nutrition", "🧘 Exercises"])
                with d_tab:
                    st.markdown("""<div class='diet-box'><b>Focus:</b><br>
                    - Early Morning: Warm water + almonds.<br>
                    - Breakfast: Veggie Poha + Milk.<br>
                    - Lunch: Brown rice + Spinach Dal + Curd.<br>
                    - Dinner: Chapati + Rajma + Vegetable Sabzi.</div>""", unsafe_allow_html=True)
                with e_tab:
                    # Data from
                    tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                    if "1st" in tri:
                        st.write("**First Trimester (Gentle Adaptation):**")
                        st.write("- Walking & Prenatal Yoga")
                        st.write("- Pelvic Floor (Kegels) & Cat-Cow Stretch")
                    elif "2nd" in tri:
                        st.write("**Second Trimester (Building Strength):**")
                        st.write("- Swimming & Stationary Cycling")
                        st.write("- Wall Squats & Side-Lying Leg Lifts")
                    else:
                        st.write("**Third Trimester (Mobility & Labor Prep):**")
                        st.write("- Butterfly Stretch & Deep Supported Squats")
                        st.write("- Pelvic Tilts & Birthing Ball Exercises")
                    
            else:
                st.header("🌸 PCOS Strength & Nutrition")
                t1, t2 = st.tabs(["🥗 Nutrition", "🏋️ Exercise"])
                with t1:
                    # Data from
                    st.markdown("""<div class='diet-box'><b>PCOS Principles:</b><br>
                    - Aim for 50-60g Protein and 25g Fiber daily.<br>
                    - Walk 10-15 mins after meals to lower sugar spikes.</div>""", unsafe_allow_html=True)
                with t2:
                    st.write("**Strength (3-4x/week):** Squats, Lunges, Push-ups, Glute Bridges.")
                    st.write("**Cardio:** Brisk walking (30-45 mins) is highly effective.")
                    st.write
