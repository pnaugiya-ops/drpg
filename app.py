import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI ---
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
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; min-width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

# --- 2. LOGIN PAGE & BRANDING ---
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

# --- 3. PATIENT DASHBOARD ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"## Welcome, {st.session_state.name}")
    
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

    if menu == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ EDD: {edd} | Current Week: {wks}")
            
            weeks_data = {
                4: "🌱 Size of a poppy seed. Implantation is occurring.",
                12: "🍋 Size of a lime. Baby's heart is beating clearly.",
                20: "🍌 Halfway! You will feel kicks.",
                28: "🍆 Third trimester starts. Baby can open eyes.",
                36: "🍈 Rapid weight gain for baby.",
                40: "🍉 Full term. Ready for delivery."
            }
            st.info(weeks_data.get(wks, "🍉 Your baby is growing beautifully every day!"))
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Baby's Date of Birth")
            days_post = (date.today() - birth_date).days
            st.success(f"Days since delivery: {days_post}")

    elif menu == "Detailed Diet Plans":
        st.header(f"🥗 Detailed Diet Chart: {st.session_state.stat}")
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>Trimester 1:</b> Folic Acid focus. Soaked almonds, milk, poha, dal-roti-sabzi, curd. Avoid papaya/pineapple.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Trimester 2:</b> Iron & Calcium focus. Fruit at 11am, Coconut water, Paneer, Spinach, Makhana.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Trimester 3:</b> Energy focus. Milk with Ghee/Dates, frequent small meals, light khichdi dinner.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Diet:</b> Low GI foods. Oats, Cinnamon water, Flax seeds, Walnuts, Sprouts. Avoid sugar and Maida.</div>", unsafe_allow_html=True)

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Lactation Diet:</b> Soaked Methi, Jeera-water, Garlic, Gond Ladoo, Milk with Shatavari. High fluid intake.</div>", unsafe_allow_html=True)

    elif menu == "Exercise & Yoga":
        st.header(f"🧘 Wellness for {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Butterfly Pose:** For pelvic floor health.")
            st.write("2. **Cat-Cow:** For back pain relief.")
            st.write("3. **Brisk Walking:** 20 mins daily.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** For hormonal balance.")
            st.write("2. **Strength Training:** To improve insulin sensitivity.")
        else:
            st.write("1. **Kegels:** For pelvic recovery.")
            st.write("2. **Anulom Vilom:** For stress reduction.")

    elif menu == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab"):
            hb = st.number_input("Hb (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Saved!")

    elif menu == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure")
        if st.button("Log Vitals"): st.success("Vitals Recorded.")

    elif menu == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        v = st.selectbox("Select Dose", ["TT-1", "TT-2", "Tdap", "Flu Vaccine"])
        if st.button("Log Vaccination"): st.success(f"Confirmed: {v}")

    elif menu == "Book Appointment":
        st.header("📅 Book Appointment")
        d = st.date_input("Date", min_value=date.today())
        if st.button("Confirm"): st.success("Request Sent!")

# --- 4. DOCTOR DASHBOARD ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor Dashboard")
    st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No bookings.")
