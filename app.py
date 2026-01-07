import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Branding and Layout */
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:5px 15px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border:1px solid #e0e0e0; border-left:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    
    /* Sidebar Navigation Appearance */
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; }
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

# --- 3. PATIENT DASHBOARD (DETAILED COMPONENTS) ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 👤 Patient: {st.session_state.name}")
    
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Pregnancy/Cycle Tracker", 
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

    # SECTION: TRACKER
    if m == "Pregnancy/Cycle Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            
            weeks_data = {
                4: "🌱 Size of a poppy seed. The embryo is implanting.",
                12: "🍋 Size of a lime. Baby's heart is beating and organs are forming.",
                20: "🍌 Halfway! You will feel kicks (Quickening).",
                28: "🍆 Third Trimester starts. Baby can open eyes.",
                36: "🍈 Rapid weight gain. Baby is dropping into the pelvis.",
                40: "🍉 Full term. Monitor for contractions."
            }
            st.info(weeks_data.get(wks, "🍉 Your baby is growing beautifully every day!"))
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Baby's Birth Date")
            days_post = (date.today() - birth_date).days
            st.success(f"It has been {days_post} days since delivery. Recovery is a journey!")

    # SECTION: DIET PLANS (FULL DETAIL)
    elif m == "Detailed Diet Plans":
        st.header(f"🥗 Detailed Diet Chart for {st.session_state.stat}")
        pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>Early Morning:</b> 5 Almonds + Milk.<br><b>Breakfast:</b> Veggie Poha/Eggs.<br><b>Lunch:</b> 2 Roti, Dal, Green Veggie, Curd.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Focus:</b> Iron & Calcium.<br><b>Mid-day:</b> Seasonal Fruit + Coconut Water.<br><b>Evening:</b> Roasted Makhana + Milk.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Focus:</b> Energy.<br><b>Dinner:</b> Light Khichdi or Soup.<br><b>Note:</b> Small frequent meals to avoid acidity.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Management:</b><br>1. High Fiber (Whole Grains/Oats).<br>2. Lean Protein (Pulses/Soy/Paneer).<br>3. Healthy Fats (Flax & Pumpkin seeds).<br><b>Avoid:</b> Refined sugar and maida.</div>", unsafe_allow_html=True)

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Lactation Support:</b><br>1. Soaked Methi seeds.<br>2. Garlic & Cumin in meals.<br>3. Milk with Shatavari.<br>4. High fluid intake (3-4 Liters).</div>", unsafe_allow_html=True)

    # SECTION: EXERCISE (FULL DETAIL)
    elif m == "Exercise & Yoga":
        st.header(f"🧘 Exercise Guidance for {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Butterfly Pose (Baddha Konasana):** Strengthens the pelvic floor.")
            st.write("2. **Cat-Cow Stretch:** For relieving pregnancy-related back pain.")
            st.write("3. **Brisk Walking:** 20-30 minutes daily is safest and best.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** To improve metabolic and hormonal balance.")
            st.write("2. **Strength Training:** To help manage insulin resistance.")
        else:
            st.write("1. **Kegels:** Essential for postpartum pelvic recovery.")
            st.write("2. **Slow Walking:** Start with light movement as per comfort.")

    # SECTION: LABS
    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Record Saved Successfully!")

    # SECTION: VITALS
    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure (e.g. 120/80)")
        if st.button("Log Vitals"): st.success("Vitals Updated.")

    # SECTION: VACCINATIONS
    elif m == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        v = st.selectbox("Select Dose", ["TT-1", "TT-2", "Tdap", "Flu Vaccine", "Hepatitis B"])
        if st.button("Mark as Done"): st.success(f"Logged {v} on {date.today()}")

    # SECTION: BOOKING
    elif m == "Book Appointment":
        st.header("📅 Book Clinic Appointment")
        d = st.date_input("Choose Date", min_value=date.today())
        if st.button("Confirm Booking"): st.success("Appointment Requested!")

# --- 4. DOCTOR DASHBOARD ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor Dashboard")
    st.write("Recent Patient Appointments:")
    st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No current data.")
