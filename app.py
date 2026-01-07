import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:4px 12px; border-radius:15px; font-weight:bold; display:inline-block; margin:3px; font-size:13px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border-left:5px solid #ff4b6b; margin-bottom:10px; color: #333; line-height:1.5; }
    .stButton>button { background:#ff4b6b !important; color:white !important; border-radius:8px !important; font-weight:bold !important; width: 100% !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERMANENT DATA STORAGE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'labs' not in st.session_state: st.session_state.labs = []
if 'vitals' not in st.session_state: st.session_state.vitals = []
if 'apts' not in st.session_state: st.session_state.apts = []
if 'blocked' not in st.session_state: st.session_state.blocked = []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN FLOW ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h2>Dr. Priyanka Gupta</h2><p>MS (Obs & Gynae)</p><div><span class='clinic-badge'>Infertility Specialist</span><span class='clinic-badge'>Ultrasound</span><span class='clinic-badge'>Thyrocare Lab</span></div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Access", "Admin Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Patient Full Name")
            s = st.radio("Clinical Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter Dashboard") and n:
                st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.text_input("Clinic Password", type="password") == "clinicadmin786" and st.form_submit_button("Admin Login"):
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 4. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}\n**{st.session_state.stat}**")
    m = st.sidebar.radio("NAVIGATE", ["Tracker", "Diet Plans", "Exercises", "Lab Reports", "Vitals & BMI", "Social Feed", "Book Appointment"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if m == "Tracker":
        st.header("🤰 Pregnancy & Health Progress")
        if st.session_state.stat == "Pregnant":
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"Estimated Due Date: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | You are in Week {wks}")
        else: st.info("Welcome to your clinic dashboard. Use the sidebar to track your health.")

    elif m == "Diet Plans":
        st.header(f"🥗 Detailed Diet Chart: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1: st.markdown("<div class='diet-card'><b>Focus: Folic Acid.</b><br>Early Morning: 5 Almonds + 2 Walnuts. Breakfast: Veggie Poha/Oats. Lunch: 2 Roti + Dal + Green Sabzi + Curd. Evening: Roasted Makhana + Milk.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>Focus: Iron & Calcium.</b><br>Include Coconut Water, 1 seasonal fruit, Spinach (twice a week), Paneer, and Sprouted salads. High protein intake is essential.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>Focus: Energy.</b><br>6 small meals. Milk with 1 tsp Ghee. Bedtime Milk with 2 Dates. Focus on hydration and fiber-rich foods.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Protocol:</b><br>Low GI Foods (Millets/Brown Rice). 1 tsp Flax seeds daily. Cinnamon water in morning. High protein (Sprouts/Soya). Strictly avoid sugar and Maida.</div>", unsafe_allow_html=True)
        else: st.markdown("<div class='diet-card'><b>Lactation:</b><br>Soaked Methi seeds, Jeera-water, Garlic in meals, Gond Ladoo, Shatavari with milk. Ensure 4 Liters of water daily.</div>", unsafe_allow_html=True)

    elif m == "Exercises":
        st.header("🧘 Exercises & Yoga")
        st.write("1. **Butterfly Pose:** Improves pelvic floor flexibility.\n2. **Cat-Cow Stretch:** Relieves back pressure.\n3. **Prenatal Walking:** 20-30 mins daily.\n4. **Breathing:** 10 mins Anulom Vilom for stress.")

    elif m == "Lab Reports":
        st.header("📊 Lab Tracking (CBC/Sugar/Thyroid)")
        with st.form("lab_f"):
            hb, sugar, tsh = st.number_input("Hemoglobin (Hb)", 5.0, 18.0, 12.0), st.number_input("Blood Sugar", 50, 400, 90), st.number_input("Thyroid (TSH)",
