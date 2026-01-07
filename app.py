import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(
    page_title="Bhavya Labs", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:5px 15px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border:1px solid #e0e0e0; border-left:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    /* Force Sidebar Visibility */
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; min-width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

# --- 2. LOGIN PAGE ---
if not st.session_state.get('logged_in'):
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
                    st.session_state.logged_in = True
                    st.session_state.name = n
                    st.session_state.age = a
                    st.session_state.stat = s
                    st.session_state.role = "P"
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.logged_in = True
                    st.session_state.role = "D"
                    st.rerun()

# --- 3. PATIENT DASHBOARD (VISIBLE AFTER LOGIN) ---
elif st.session_state.role == "P":
    # Sidebar is created here - it MUST appear now
    st.sidebar.markdown(f"## Welcome, {st.session_state.name}")
    st.sidebar.markdown(f"**Status:** {st.session_state.stat}")
    
    menu = st.sidebar.radio("DASHBOARD MENU", [
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
    if menu == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ EDD: {edd} | Current Week: {wks}")
            
            weeks_data = {
                4: "🌱 Embryo is implanting. Size of a poppy seed.",
                12: "🍋 First trimester ending. Organs are formed.",
                20: "🍌 Halfway! Baby kicks are becoming stronger.",
                28: "🍆 Third trimester. Eyes are opening.",
                36: "🍈 Baby is preparing for birth.",
                40: "🍉 Full term."
            }
            st.info(weeks_data.get(wks, "🍉 Your baby is growing well!"))
            

[Image of fetal development stages during pregnancy]

        
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
    elif menu == "Detailed Diet Plans":
        st.header(f"🥗 Detailed Diet Chart: {st.session_state.stat}")
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>Trimester 1:</b> Folic acid focus. Almonds, Milk, Poha, Dal, Roti, Curd.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Trimester 2:</b> Iron & Calcium. Fruits, Coconut water, Paneer, Spinach.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Trimester 3:</b> High energy. Light Khichdi, Milk with Ghee, small frequent meals.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Diet:</b> High fiber oats, Flax seeds, Cinnamon water, Lean protein. Avoid sugar.</div>", unsafe_allow_html=True)

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Lactation:</b> Soaked Methi, Garlic, Gond Ladoo, 4 liters of fluid.</div>", unsafe_allow_html=True)

    # --- DETAILED EXERCISE ---
    elif menu == "Exercise & Yoga":
        st.header(f"🧘 Wellness for {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Butterfly Pose:** For pelvic strength.")
            st.write("2. **Cat-Cow Stretch:** For back pain.")
            st.write("3. **Walking:** 20 mins brisk walk.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** Hormonal balance.")
            st.write("2. **Strength Training:** Insulin sensitivity.")
        else:
            st.write("1. **Kegels:** Pelvic recovery.")
            st.write("2. **Deep Breathing:** Stress reduction.")

    # --- LABS, VITALS, VACCINATIONS ---
    elif menu == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab"):
            hb = st.number_input("Hb (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Saved!")

    elif menu == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure")
        if st.button("Log"): st.success("Recorded.")

    elif menu == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        v = st.selectbox("Dose", ["TT-1", "TT-2", "Tdap", "Flu"])
        if st.button("Confirm"): st.success(f"Logged {v}")

    elif menu == "Book Appointment":
        st.header("📅 Book Appointment")
        d = st.date_input("Date", min_value=date.today())
        if st.button("Confirm Booking"): st.success("Requested!")

# --- 4. DOCTOR DASHBOARD ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin Panel")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor Dashboard")
    st.write("Recent Patient Activity:")
    st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No appointments.")
