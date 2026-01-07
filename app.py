import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & PERMANENT SIDEBAR ---
# Setting initial_sidebar_state to "expanded" forces the dashboard to be visible
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Ensuring the sidebar is clearly visible */
    [data-testid="stSidebarNav"] { background-color: #f8f9fa; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #ddd; }
    
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:5px 15px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border:1px solid #e0e0e0; border-left:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

# --- 2. LOGIN PAGE & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
        <div>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise Lab</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Current Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":a,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D","name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. PATIENT DASHBOARD ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 👤 Patient: {st.session_state.name}")
    
    # THE DASHBOARD MENU (FORCED VISIBLE)
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Health Tracker", 
        "Detailed Diet Plans", 
        "Exercise & Yoga", 
        "Lab Reports & Trends", 
        "Health Vitals", 
        "Vaccinations", 
        "Book Appointment"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- HEALTH TRACKER ---
    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            
            weeks_data = {
                4: "🌱 Size of a poppy seed. Implantation is occurring.",
                12: "🍋 Size of a lime. Baby's heart is beating clearly.",
                20: "🍌 Halfway! You will feel the 'quickening' (kicks).",
                28: "🍆 Baby can open eyes and sense light.",
                36: "🍈 Baby is gaining weight rapidly for birth.",
                40: "🍉 Full term. Monitor for labor pains."
            }
            st.info(weeks_data.get(wks, "🍉 Your baby is growing and reaching new milestones every day!"))
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Baby's Date of Birth")
            days_post = (date.today() - birth_date).days
            st.success(f"Days since delivery: {days_post}")

    # --- DETAILED DIET PLANS ---
    elif m == "Detailed Diet Plans":
        st.header(f"🥗 {st.session_state.stat} Diet Plan")
        pref = st.radio("Food Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>Early Morning:</b> 5 soaked almonds + 2 walnuts.<br><b>Breakfast:</b> Veggie Poha or Moong Dal Chilla.<br><b>Lunch:</b> 2 Rotis + Dal + Green Veggie + Curd.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Mid-Morning:</b> Seasonal fruit + Coconut water.<br><b>Lunch:</b> Roti + Paneer/Chicken + Salad.<br><b>Evening:</b> Roasted Makhana + Milk.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Dinner:</b> Light Khichdi or Soup.<br><b>Note:</b> Increase calcium intake; small frequent meals.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>Breakfast:</b> Oats with seeds or Besan Chilla.<br><b>Lunch:</b> Missi Roti + Sprouted Salad + Curd.<br><b>Snack:</b> Green Tea + Walnuts.<br><b>Avoid:</b> Processed sugar and white flour.</div>", unsafe_allow_html=True)

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Dietary Essentials:</b><br>1. Soaked Methi water (Empty stomach).<br>2. Garlic in meals.<br>3. Gond/Methi Ladoo with Milk.<br>4. High fluid intake (3-4 Liters).</div>", unsafe_allow_html=True)

    # --- DETAILED EXERCISE ---
    elif m == "Exercise & Yoga":
        st.header(f"🧘 {st.session_state.stat} Wellness")
        if st.session_state.stat == "Pregnant":
            st.write("**1. Butterfly Pose (Baddha Konasana):** Strengthens pelvic floor.")
            st.write("**2. Cat-Cow Stretch:** Relieves back tension.")
            st.write("**3. Walking:** 20-30 minutes of brisk walking is ideal.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("**1. Surya Namaskar:** 5-10 rounds for metabolic health.")
            st.write("**2. Strength Training:** To improve insulin sensitivity.")
        else:
            st.write("**1. Pelvic Floor (Kegels):** Crucial for recovery.")
            st.write("**2. Deep Breathing:** Reduces postpartum stress.")

    # --- LAB REPORTS ---
    elif m == "Lab Reports & Trends":
        st.header("📊 Clinical Lab Trends")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save Report"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Record Saved!")

    # --- VITALS ---
    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure (e.g., 120/80)")
        if st.button("Log Vitals"): st.success("Vitals Recorded.")

    # --- VACCINATIONS ---
    elif m == "
