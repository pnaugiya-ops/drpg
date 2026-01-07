import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; border: 1px solid white; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border:1px solid #e0e0e0; border-left:6px solid #ff4b6b; margin-bottom:15px; line-height: 1.6; color: #333; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
for key in ['logged_in', 'lab_records', 'vital_records', 'appointments']:
    if key not in st.session_state: 
        st.session_state[key] = False if key == 'logged_in' else []
if 'availability' not in st.session_state: st.session_state.availability = {"blocked": []}
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h2 style='margin:0;'>Dr. Priyanka Gupta</h2><p>MS (Obs & Gynae)</p><div style='margin-top:10px;'><span class='clinic-badge'>Infertility Specialist</span><span class='clinic-badge'>Ultrasound</span><span class='clinic-badge'>Pharmacy</span><span class='clinic-badge'>Thyrocare Franchise Lab</span></div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Access", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter Dashboard"):
                if n: st.session_state.update({"logged_in":True,"name":n,"stat":s,"role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.text_input("Admin Password", type="password") == "clinicadmin786" and st.form_submit_button("Login"):
                st.session_state.update({"logged_in":True,"role":"D"})
                st.rerun()

# --- 3. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}\n**Status:** {st.session_state.stat}")
    m = st.sidebar.radio("MENU", ["Health Tracker", "Detailed Diet Plans", "Exercise Routine", "Lab Reports", "Vitals & BMI", "Social Feed", "Book Appointment"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if m == "Health Tracker":
        st.header("🤰 Tracker")
        if st.session_state.stat == "Pregnant":
            lmp = st.date_input("LMP", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"Due Date: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
            weeks_info = {4: "🌱 Implantation.", 12: "🍋 End of T1.", 20: "🍌 Halfway!", 28: "🍆 T3 begins.", 40: "🍉 Full Term."}
            st.info(weeks_info.get(wks, "🍉 Your baby is growing well!"))
        else:
            st.info("Keep tracking your daily health goals here.")

    elif m == "Detailed Diet Plans":
        st.header(f"🥗 Diet: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1: st.markdown("<div class='diet-card'><b>T1:</b> 5 Almonds morning. Breakfast: Poha/Oats. Lunch: Roti, Dal, Curd.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>T2:</b> Fruits, Coconut Water, Spinach, Paneer, Sprouted salads.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>T3:</b> 6 small meals. Milk with Ghee. Bedtime Milk with Dates.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS:</b> Low GI. Flax seeds. Cinnamon water. High protein. No sugar.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='diet-card'><b>Lactation:</b> Soaked Methi, Jeera-water, Garlic, Gond Ladoo, Shatavari.</div>", unsafe_allow_html=True)

    elif m == "Exercise Routine":
        st.
