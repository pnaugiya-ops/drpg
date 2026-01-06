import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & TOGGLE LOGIC ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

# Initialize Session States
if 'show_menu' not in st.session_state: st.session_state.show_menu = True
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []
if 'blocked_dates' not in st.session_state: st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state: st.session_state.broadcasts = []

# CSS to Hide technical headers and style the Dashboard
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stButton>button.toggle-btn {
        background-color: #003366;
        color: white;
        border-radius: 20px;
        border: 2px solid #ff4b6b;
    }
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .diet-box { background:#f0f7f9; padding:15px; border-radius:10px; border-left:5px solid #003366; margin-bottom:10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
        <p>Infertility Specialist | Ultrasound | Laparoscopic Surgery</p>
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
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("☰ DASHBOARD MENU", key="toggle"):
            st.session_state.show_menu = not st.session_state.show_menu
            st.rerun()

    if st.session_state.show_menu:
        m = st.sidebar.radio("NAVIGATE TO:", [
            "Pregnancy Tracker", 
            "Detailed Diet Plans", 
            "Exercise & Yoga", 
            "Lab Trends", 
            "Health Vitals", 
            "Vaccinations", 
            "Appointments"
        ])
    else:
        m = "Pregnancy Tracker"

    if m == "Pregnancy Tracker":
        st.header("🤰 Pregnancy Week-by-Week Tracker")
        if "Pregnant" in st.session_state.stat:
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ EDD: {edd} | Week: {wks}")
            
            weeks_info = {
                4: "🌱 Implantation Stage. Size of a poppy seed.",
                12: "🍋 First Trimester end. Baby starts moving fingers.",
                20: "🍌 Halfway! Gender is clear and kicks start.",
                28: "🍆 Third Trimester. Eyes open and light can be felt.",
                36: "🍈 Baby is dropping into the pelvis.",
                40: "🍉 Full Term. Ready for birth."
            }
            st.info(weeks_info.get(wks, "🍉 Your baby is growing and developing beautifully!"))
        else:
            lp = st.date_input("Last Period Date")
            st.info(f"Next Cycle Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Detailed Diet Plans":
        st.header("🥗 Detailed Clinical Diet Chart")
        pref = st.radio("Select Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        if "Pregnant" in st.session_state.stat:
            d1, d2, d3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with d1:
                st.markdown("<div class='diet-box'><b>Early Morning:</b> 5 soaked almonds + 2 walnuts.<br><b>Breakfast:</b> Veggie Poha or Moong Dal Chilla.<br><b>Lunch:</b> 2 Rotis + Dal + Green Veggie + Curd.</div>", unsafe_allow_html=True)
            with d2:
                st.markdown("<div class='diet-box'><b>Mid-Morning:</b> 1 bowl seasonal fruit.<br><b>Lunch:</b> Add Paneer/Fish (if Non-Veg) + Sprout Salad.<br><b>Evening:</b> Roasted Makhana + Milk.</div>", unsafe_allow_html=True)
            with d3:
                st.markdown("<div class='diet-box'><b>Note:</b> Small frequent meals. Avoid heavy spicy food.<br><b>Early Morning:</b> Milk with Ghee/Dates.<br><b>Dinner:</b> Light Khichdi or Soup.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='diet-box'><b>PCOS/Gynae Focus:</b> High fiber, Low sugar. Add Flax seeds and Cinnamon water daily.</div>", unsafe_allow_html=True)

    elif m == "Exercise & Yoga":
        st.header("🧘 Detailed Yoga & Movement")
        st.write("1. **Deep Breathing (Pranayama):** 10 minutes daily.")
        st.write("2. **Butterfly Pose:** For pelvic floor flexibility.")
        st.write("3. **Brisk Walking:** 20-30 minutes daily.")

    elif m == "Lab Trends":
        st.header("📊 Lab Records")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Log Report"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Report Saved!")

    elif m == "Health Vitals":
        st.header("📈 Health Tracker")
        st.number_input("Current Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure")
        if st.button("Save Vitals"): st.success("Vitals Updated")

    elif m == "Vaccinations":
        st.header("💉 Vaccination Log")
        vac = st.selectbox("Select Dose", ["TT Dose 1", "TT Dose 2", "Tdap", "Flu Shot"])
        if st.button("Confirm"): st.success("Logged")

    elif m == "Appointments":
        st.header("📅 Book Appointment")
        dt_a = st.date_input("Select Date", min_value=date.today())
        if st.button("Book Now"): st.success("Confirmed!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor Dashboard")
    st.write("Recent Appointments:")
    st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No current data")
