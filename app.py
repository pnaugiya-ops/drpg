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
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; min-width: 320px !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'vital_records' not in st.session_state: st.session_state.vital_records = []
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

# --- 3. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}")
    st.sidebar.info(f"Status: {st.session_state.stat}")
    
    m = st.sidebar.radio("DASHBOARD MENU", [
        "Health Tracker", 
        "Detailed Diet Plans", 
        "Exercise & Yoga Routine", 
        "Lab Reports (CBC/Sugar/Thyroid)", 
        "Vitals & BMI Calculator", 
        "Vaccination Schedule", 
        "Book Appointment"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- TRACKER ---
    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("Last Menstrual Period (LMP)", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            weeks_info = {
                4: "🌱 **Week 4:** Implantation stage. Embryo is size of a poppy seed.",
                12: "🍋 **Week 12:** End of 1st Trimester. Major organs are formed.",
                20: "🍌 **Week 20:** Halfway point! You may feel baby's first kicks.",
                28: "🍆 **Week 28:** 3rd Trimester begins. Baby starts to open eyes.",
                36: "🍈 **Week 36:** Baby is gaining weight rapidly for birth.",
                40: "🍉 **Week 40:** Full term. Keep track of fetal movements."
            }
            st.info(weeks_info.get(wks, "🍉 Your baby is growing beautifully every single day!"))
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle Tracking")
            lp = st.date_input("Start Date of Last Period")
            st.info(f"Next Predicted Cycle: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")
        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery")
            birth_date = st.date_input("Date of Delivery")
            st.success(f"Day {(date.today() - birth_date).days} of recovery. Focus on rest.")

    # --- DETAILED DIET PLANS ---
    elif m == "Detailed Diet Plans":
        st.header(f"🥗 Clinical Diet Chart: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>T1 Focus: Folic Acid.</b><br>5 Almonds + 2 Walnuts morning. Breakfast: Poha/Oats/Dal Chilla. Lunch: 2 Roti, Dal, Green Sabzi, Fresh Curd. Evening: Roasted Makhana/Milk.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>T2 Focus: Iron & Calcium.</b><br>Include Coconut Water, Fruits, Spinach, and Paneer. Add Sprouted salads for extra protein and fiber.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>T3 Focus: Energy & Digestion.</b><br>Eat 6 small meals. Milk with 1 tsp Ghee. Bedtime Milk with 2 Dates. Focus on hydration.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS Protocol:</b><br>Low GI Foods (Brown Rice/Millets). 1 tsp Flax seeds daily. Cinnamon water in morning. High protein (Sprouts/Soya). Avoid refined sugar and Maida.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Lactation Boosters:</b><br>Soaked Methi seeds, Jeera-water, Garlic, Gond Ladoo, Shatavari granules with milk. Minimum 3.5 - 4 Liters of fluids daily.</div>", unsafe_allow_html=True)

    # --- DETAILED EXERCISE ---
    elif m == "Exercise & Yoga Routine":
        st.header(f"🧘 Therapeutic Movement: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Baddha Konasana (Butterfly Pose):** To improve pelvic flexibility.")
            st.write("2. **Marjaryasana (Cat-Cow Stretch):** To relieve back strain.")
            st.write("3. **Prenatal Walking:** 20-30 mins daily on a flat surface.")
            st.write("4. **Deep Breathing:** 10 mins of Anulom Vilom for relaxation.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** 5-10 rounds for hormonal balance.")
            st.write("2. **Strength Training:** To help with insulin resistance.")
            st.write("3. **Kapalbhati:** Useful for weight management (except during periods).")
        else:
            st.write("1. **Kegel Exercises:** Essential for pelvic floor recovery.")
            st.write("2. **Diaphragmatic Breathing:** To manage postpartum stress.")

    # --- LAB REPORTS ---
    elif m == "Lab Reports (CBC/Sugar/Thyroid)":
        st.header("📊 Blood & Urine Report Tracking")
        with st.form("lab_form"):
            c1, c2 = st.columns(2)
            hb = c1.number_input("Hemoglobin - CBC (g/dL)", 5.0, 20.0, 12.0)
            sugar = c2.number_input("Blood Sugar (mg/dL)", 50, 500, 90)
            tsh = c1.number_input("Thyroid - TSH (mIU/L)", 0.0, 50.0, 2.5)
            urine = c2.selectbox("Urine Test (Sugar/Albumin)", ["Negative", "Trace", "+1", "+2", "+3"])
            if st.form_submit_button("Save & Update Trends"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar, "TSH": tsh, "Urine": urine})
                st.success("Report data saved to history.")

        if st.session_state.lab_records:
            df = pd.DataFrame(st.session_state.lab_records)
            st.subheader("📈 Clinical Trend Chart")
            st.line_chart(df.set_index('Date')[['Hb', 'TSH', 'Sugar']])
            st.subheader("📋 Previous Records")
            st.dataframe(df)

    # --- VITALS & BMI ---
    elif m == "Vitals & BMI Calculator":
        st.header("📈 Vital Signs & BMI Tracking")
        with st.form("vital_form"):
            c1, c2 = st.columns(2)
            pulse = c1.number_input("Pulse Rate (BPM)", 40, 200, 72)
            bp = c2.text_input("Blood Pressure (e.g. 110/70)", "110/70")
            weight = c1.number_input("Weight (kg)", 30.0, 200.0, 60.0)
            height = c2.number_input("Height (cm)", 100.0, 250.0, 160.0)
            
            if st.form_submit_button("Calculate BMI & Log Vitals"):
                bmi_val = round(weight / ((height/100)**2), 2)
                st.session_state.vital_records.append({"Date": date.today(), "Pulse": pulse, "BP": bp, "Weight": weight, "Height": height, "BMI": bmi_val})
                st.success(f"Log Updated! Current BMI: {bmi_val}")

        if st.session_state.vital_records:
            current_bmi = st.session_state.vital_records[-1]["BMI"]
            if current_bmi < 18.5: st.warning(f"BMI Result: {current_bmi} (Underweight)")
            elif 18.5 <= current_bmi <= 24.9: st.success(f"BMI Result: {current_bmi} (Normal)")
            else: st.error(f"BMI Result: {current_bmi} (Overweight/Obese)")

    # --- VACCINATION ---
    elif m == "Vaccination Schedule":
        st.header("💉 Immunization Log")
        vac = st.selectbox("Select Vaccine Dose", ["TT-1", "TT-2", "Tdap", "Flu Shot", "Hepatitis B"])
        if st.button("Mark Administered"):
            st.success(f"Verified: {vac} logged for {date.today().strftime('%d %b %Y')}")

    # --- APPOINTMENTS (15-MIN SLOTS) ---
    elif m == "Book Appointment":
        st.header("📅 Schedule a Visit")
        
        # Morning slots: 11:15 AM to 2:00 PM
        m_slots = [f"{h}:{m:02d} AM" for h in [11] for m in [15, 30, 45]] + \
                  [f"{h}:{m:02d} PM" for h in [12, 1] for m in [0, 15, 30, 45]] + ["2:00 PM"]
        
        # Evening slots: 6:00 PM to 8:00 PM
        e_slots = [f"{h}:{m:02d} PM" for h in [6, 7] for m in [0, 15, 30, 45]] + ["8:00 PM"]
        
        col1, col2 = st.columns(2)
        d = col1.date_input("Preferred Date", min_value=date.today())
        t = col2.selectbox("Select Time Slot (15-Min)", m_slots + e_slots)
        
        if st.button("Request Booking"):
            st.balloons()
            st.success(f"Appointment request sent for {d} at {t}. The clinic will contact you.")

# --- 4. ADMIN VIEW ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor's Master Dashboard")
    st.info("Clinical reports and patient vitals are displayed here.")
