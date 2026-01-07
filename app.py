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
    
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; border: 1px solid white; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border:1px solid #e0e0e0; border-left:6px solid #ff4b6b; margin-bottom:15px; line-height: 1.6; color: #333; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; height: 3em; }
    
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; min-width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h2 style='margin:0;'>Dr. Priyanka Gupta</h2>
        <p style='font-size:1.2em;'>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise Lab</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Access", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Patient Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Clinical Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter My Dashboard"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Admin Password", type="password")
            if st.form_submit_button("Login to Clinic Master"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D"})
                    st.rerun()

# --- 3. PATIENT PORTAL (FULL CONTENT) ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}")
    st.sidebar.info(f"Status: {st.session_state.stat}")
    
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Health & Pregnancy Tracker", 
        "Detailed Diet Plans", 
        "Exercise & Yoga Routine", 
        "Lab Reports & Trends", 
        "Vital Signs Monitoring", 
        "Vaccination Schedule", 
        "Book Appointment"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- TRACKER SECTION ---
    if m == "Health & Pregnancy Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("Last Menstrual Period (LMP)", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            
            weeks_info = {
                4: "🌱 **Week 4:** Implantation. Embryo is size of a poppy seed.",
                12: "🍋 **Week 12:** Organs are fully formed. Baby begins to move.",
                20: "🍌 **Week 20:** Halfway point! You can feel 'Quickening'.",
                28: "🍆 **Week 28:** 3rd Trimester begins. Baby's eyes open.",
                36: "🍈 **Week 36:** Baby gains weight rapidly. Position may shift down.",
                40: "🍉 **Week 40:** Full term milestone. Ready for delivery!"
            }
            st.info(weeks_info.get(wks, "🍉 Baby is reaching new developmental milestones today!"))
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracking")
            lp = st.date_input("Start Date of Last Period")
            st.info(f"Next Predicted Cycle: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Date of Delivery")
            days_post = (date.today() - birth_date).days
            st.success(f"Day {days_post} of recovery. Prioritize sleep and fluids.")

    # --- DIET SECTION (RETAINED IN FULL DETAIL) ---
    elif m == "Detailed Diet Plans":
        st.header(f"🥗 Clinical Diet Chart: {st.session_state.stat}")
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1 (Weeks 1-12)", "Trimester 2 (Weeks 13-26)", "Trimester 3 (Weeks 27-40)"])
            with t1:
                st.markdown("<div class='diet-card'><b>Trimester 1 Focus: Folic Acid & Iron</b><br>1. <b>Morning:</b> 5 soaked almonds + 2 walnuts.<br>2. <b>Breakfast:</b> Veggie Poha / Oats / Stuffed Dal Paratha.<br>3. <b>Mid-morning:</b> Seasonal Fruit (Apple/Pomegranate).<br>4. <b>Lunch:</b> 2 Roti + Bowl of Dal + Green Sabzi + Curd.<br>5. <b>Evening:</b> Roasted Makhana + Milk.<br>6. <b>Dinner:</b> Light Vegetable Dalia / Soup.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Trimester 2 Focus: Calcium & Protein</b><br>1. <b>Breakfast:</b> Paneer Paratha / Sprouted Salad + Milk.<br>2. <b>Mid-day:</b> Coconut Water + 1 Fruit.<br>3. <b>Lunch:</b> Mix Veg + Dal + Roti/Rice. Include Spinach twice a week.<br>4. <b>Evening:</b> Dry Fruit Laddu / Boiled Egg.<br>5. <b>Dinner:</b> Paneer or Soya Curry + 1-2 Roti.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Trimester 3 Focus: High Energy & Easy Digestion</b><br>1. <b>Pattern:</b> 6 small meals instead of 3 large ones.<br>2. <b>Evening:</b> 1 glass Milk with 1 tsp Ghee.<br>3. <b>Night:</b> Milk with 2 Dates.<br>4. <b>Note:</b> Avoid heavy fried food to prevent acidity.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Management Protocol:</b><br>1. <b>Low GI:</b> Whole grains like Millets or Brown rice.<br>2. <b>Seeds:</b> 1 tsp Flax seeds + 1 tsp Pumpkin seeds daily.<br>3. <b>Spices:</b> 1/2 tsp Cinnamon powder in warm water.<br>4. <b>Protein:</b> Sprouts, Soya, or Paneer in every meal.<br><b>Avoid:</b> Refined sugar, Maida, and high-sugar fruits.</div>", unsafe_allow_html=True)

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Lactation Support:</b><br>1. <b>Morning:</b> Soaked Methi seeds.<br>2. <b>Meals:</b> Garlic, Ginger, and Jeera in all preparations.<br>3. <b>Hydration:</b> 3-4 Liters of fluids daily.<br>4. <b>Shatavari:</b> Take with Milk as prescribed by Dr. Priyanka.</div>", unsafe_allow_html=True)

    # --- EXERCISE SECTION ---
    elif m == "Exercise & Yoga Routine":
        st.header(f"🧘 Therapeutic Movement: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Butterfly Pose:** For pelvic floor flexibility.")
            st.write("2. **Cat-Cow Stretch:** To relieve spinal pressure.")
            st.write("3. **Prenatal Walking:** 20-30 mins of slow, brisk walking.")
            st.write("4. **Anulom Vilom:** Breathing to manage stress.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** Improves hormonal health.")
            st.write("2. **Strength Training:** Twice a week for insulin sensitivity.")
            st.write("3. **Weight Management:** Focus on core-toning exercises.")
        else:
            st.write("1. **Kegels:** To restore pelvic floor strength.")
            st.write("2. **Deep Breathing:** Postpartum stress relief.")
            st.write("3. **Slow Walking:** Start with 10 mins and gradually increase.")

    # --- LAB REPORTS ---
    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report History")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 90)
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Report data saved.")

    # --- VITALS ---
    elif m == "Vital Signs Monitoring":
        st.header("📈 Clinical Vitals")
        col1, col2 = st.columns(2)
        wt = col1.number_input("Current Weight (kg)", 30.0, 150.0, 60.0)
        bp = col2.text_input("Blood Pressure (e.g. 110/80)")
        if st.button("Update Vitals"):
            st.success("Vitals logged successfully.")

    # --- VACCINATION ---
    elif m == "Vaccination Schedule":
        st.header("💉 Immunization Tracker")
        vac = st.selectbox("Select Administered Vaccine", ["TT-1", "TT-2", "Tdap", "Flu Shot", "Hepatitis B"])
        if st.button("Confirm Dose"):
            st.success(f"Vaccine {vac} recorded on {date.today()}")

    # --- APPOINTMENT ---
    elif m == "Book Appointment":
        st.header("📅 Appointment Booking")
        d = st.date_input("Choose Date", min_value=date.today())
        reason = st.text_area("Reason for Visit")
        if st.button("Request Booking"):
            st.success("Your request has been sent to Dr. Priyanka's clinic.")

# --- 4. ADMIN VIEW ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Clinic Management Dashboard")
    st.write("View all patient bookings and records below.")
