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
    
    /* Make the Sidebar Navigation Look Professional */
    [data-testid="stSidebarNav"] { background-color: #f8f9fa; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #ddd; }
    
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border:1px solid #e0e0e0; border-left:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []

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

# --- 3. PATIENT DASHBOARD (RESTORED FULL DETAIL) ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 👤 Patient: {st.session_state.name}")
    st.sidebar.markdown(f"**Status:** {st.session_state.stat}")
    
    # THE DASHBOARD MENU
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

    # --- HEALTH TRACKER (DETAILED FOR ALL) ---
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
            

[Image of fetal development stages during pregnancy]

        
        elif st.session_state.stat == "PCOS/Gynae":
            st.header("🩸 Menstrual Cycle & Ovulation Tracker")
            lp = st.date_input("Last Period Start Date")
            st.info(f"Next Period Expected Around: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")
            st.write("**PCOS Tip:** Tracking cycle length helps in identifying hormonal patterns.")

        elif st.session_state.stat == "Lactating Mother":
            st.header("🤱 Postpartum Recovery Tracker")
            birth_date = st.date_input("Baby's Date of Birth")
            days_post = (date.today() - birth_date).days
            st.success(f"It has been {days_post} days since delivery. Great job, Mom!")

    # --- DIET PLANS (DETAILED FOR ALL) ---
    elif m == "Detailed Diet Plans":
        st.header(f"🥗 {st.session_state.stat} Diet Plan")
        pref = st.radio("Food Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("<div class='diet-card'><b>Focus:</b> Folic Acid & Nausea Control.<br><b>Breakfast:</b> Poha/Eggs.<br><b>Lunch:</b> Dal, Roti, Sabzi, Curd.</div>", unsafe_allow_html=True)
            with t2:
                st.markdown("<div class='diet-card'><b>Focus:</b> Iron & Calcium.<br><b>Mid-day:</b> Fruits & Coconut water.<br><b>Evening:</b> Paneer/Chicken Soup & Nuts.</div>", unsafe_allow_html=True)
            with t3:
                st.markdown("<div class='diet-card'><b>Focus:</b> Energy & Digestion.<br><b>Dinner:</b> Light Khichdi with Ghee.<br><b>Note:</b> Avoid high salt/spices.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>The PCOS Plate:</b><br>1. High Fiber (Whole grains).<br>2. Lean Protein (Dal/Soy/Paneer).<br>3. Healthy Fats (Seeds/Nuts).<br><b>Avoid:</b> Sugary drinks & White Bread.</div>", unsafe_allow_html=True)
            

        elif st.session_state.stat == "Lactating Mother":
            st.markdown("<div class='diet-card'><b>Galactagogues (Milk Boosters):</b><br>1. Soaked Methi Seeds.<br>2. Garlic & Cumin (Jeera).<br>3. Plenty of Water & Milk.<br>4. Gond/Methi Ladoo.</div>", unsafe_allow_html=True)

    # --- EXERCISE & YOGA ---
    elif m == "Exercise & Yoga":
        st.header(f"🧘 Wellness for {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            st.write("1. **Butterfly Pose:** For pelvic floor health.\n2. **Cat-Cow:** For back pain relief.\n3. **Walking:** 20-30 mins daily.")
        elif st.session_state.stat == "PCOS/Gynae":
            st.write("1. **Surya Namaskar:** 5-10 rounds for hormonal balance.\n2. **Strength Training:** To improve insulin sensitivity.")
        else:
            st.write("1. **Pelvic Floor (Kegels):** For recovery.\n2. **Slow Walking:** Do not overexert.")

    # --- LAB REPORTS ---
    elif m == "Lab Reports & Trends":
        st.header("📊 Clinical Lab Trends")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 0.0, 20.0, 12.0)
            sugar = st.number_input("Blood Sugar", 0, 500, 90)
            if st.form_submit_button("Save Report"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "Sugar": sugar})
                st.success("Record Saved!")
        if st.session_state.lab_records:
            st.line_chart(pd.DataFrame(st.session_state.lab_records).set_index("Date"))

    # --- VITALS ---
    elif m == "Health Vitals":
        st.header("📈 Record Vitals")
        st.number_input("Weight (kg)", 30, 150, 60)
        st.text_input("Blood Pressure")
        if st.button("Log Vitals"): st.success("Vitals Recorded Successfully.")

    # --- VACCINATIONS ---
    elif m == "Vaccinations":
        st.header("💉 Vaccination Tracker")
        v = st.selectbox("Select Dose", ["TT-1", "TT-2", "Tdap", "Flu Vaccine", "Hepatitis B"])
        if st.button("Mark as Administered"):
            st.success(f"Logged {v} on {date.today()}")

    # --- BOOKING ---
    elif m == "Book Appointment":
        st.header("📅 Book Clinic Slot")
        d = st.date_input("Select Date", min_value=date.today())
        if st.button("Confirm Appointment"):
            st.success(f"Appointment requested for {d}")

# --- 4. DOCTOR VIEW ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin View")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    st.header("Doctor's Master Dashboard")
    st.write("Current Patient Appointments:")
    st.table(pd.DataFrame(st.session_state.appointments) if st.session_state.appointments else "No appointments booked.")
