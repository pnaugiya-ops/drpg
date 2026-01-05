import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'lab_records' not in st.session_state:
    st.session_state.lab_records = []
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'blocked_dates' not in st.session_state:
    st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state:
    st.session_state.broadcasts = []

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
        <div>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
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

# --- 3. DOCTOR DASHBOARD ---
elif st.session_state.get('role') == "D":
    st.sidebar.markdown(f"### 👩‍⚕️ Welcome, {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    
    dm = st.sidebar.radio("Doctor Panel", ["Manage Appointments", "Review Patient Reports", "Block Clinic Dates", "Broadcast Media"])

    if dm == "Manage Appointments":
        st.header("📅 Patient Appointments")
        if st.session_state.appointments:
            st.table(pd.DataFrame(st.session_state.appointments))
        else:
            st.info("No appointments currently booked.")

    elif dm == "Review Patient Reports":
        st.header("📋 Patient Lab Records")
        if st.session_state.lab_records:
            st.dataframe(pd.DataFrame(st.session_state.lab_records))
        else:
            st.info("No lab records found.")

    elif dm == "Block Clinic Dates":
        st.header("🚫 Date Management")
        b_date = st.date_input("Select Date to Block")
        if st.button("Block Date for All Bookings"):
            st.session_state.blocked_dates.append(b_date)
            st.success(f"Clinic bookings disabled for {b_date}")

    elif dm == "Broadcast Media":
        st.header("📢 Video Broadcast")
        v_url = st.text_input("Enter YouTube Video Link")
        v_desc = st.text_area("Video Title/Description")
        if st.button("Broadcast to Dashboard"):
            st.session_state.broadcasts.append({"url": v_url, "desc": v_desc})
            st.success("Video successfully broadcasted.")

# --- 4. PATIENT DASHBOARD ---
elif st.session_state.get('role') == "P":
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment", "Doctor's Updates"])
    
    # 4.1 FULL PREGNANCY WEEK-BY-WEEK CHART
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
            
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. Implantation is occurring.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. Heart is beating regularly.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. Baby starts moving fingers and toes.")
            elif wks <= 16: st.info("🥑 Week 16: Size of an avocado. Eyes and ears are moving to position.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. Halfway! You may feel kicks.")
            elif wks <= 24: st.info("🌽 Week 24: Size of an ear of corn. Lungs are beginning to form.")
            elif wks <= 28: st.info("🍆 Week 28: Size of an eggplant. Eyes can open and see light.")
            elif wks <= 32: st.info("🥬 Week 32: Size of a squash. Baby is practicing breathing.")
            elif wks <= 36: st.info("🍈 Week 36: Size of a papaya. Baby is dropping into the pelvis.")
            elif wks <= 40: st.info("🍉 Week 40: Full term! Ready for birth.")
        else:
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected Period: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    # 4.2 FULL LAB MONITORING (Hb, CBC, TSH, Sugar, Urine)
    elif m == "Lab Reports & Trends":
        st.header("📊 Comprehensive Lab Report Tracker")
        with st.form("lab_entry"):
            c1, c2 = st.columns(2)
            with c1:
                hb = st.number_input("Hemoglobin (g/dL)", 5.0, 20.0, 12.0)
                tsh = st.number_input("TSH (mIU/L)", 0.0, 20.0, 2.5)
                cbc = st.number_input("WBC Count (CBC)", 1000, 20000, 7000)
            with c2:
                sugar = st.number_input("Blood Sugar (mg/dL)", 50, 500, 90)
                urine = st.selectbox("Urine Test (Protein/Sugar)", ["Nil", "Trace", "1+", "2+", "3+"])
                pulse = st.number_input("Pulse Rate (BPM)", 40, 200, 72)
            
            if st.form_submit_button("Save Entry & Update Charts"):
                st.session_state.lab_records.append({
                    "Date": date.today(), "Hb": hb, "TSH": tsh, 
                    "CBC": cbc, "Sugar": sugar, "Urine": urine, "Pulse": pulse
                })
                st.success("Record Added!")

        if st.session_state.lab_records:
            df = pd.DataFrame(st.session_state.lab_records)
            st.subheader("📈 Trend Monitoring")
            metric = st.selectbox("Select Metric", ["Hb", "TSH", "Sugar", "Pulse", "CBC"])
            st.line_chart(df.set_index("Date")[metric])
            st.table(df)

    # 4.3 DIET PLANS (UNTOUCHED)
    elif m == "Diet Plans":
        pref = st.radio("Select Preference", ["Vegetarian", "Non-Vegetarian"])
        if "Pregnant" in st.session_state.stat:
            st.header(f"🤰 Detailed {pref} Pregnancy Diet")
            if pref == "Vegetarian":
                st.write("**Early Morning:** 5 Soaked Almonds + Warm Milk.")
                st.write("**Breakfast:** Veggie Poha OR Moong Dal Chilla OR Paneer Paratha with Curd.")
                st.write("**Mid-Morning:** 1 Fruit + Coconut Water.")
                st.write("**Lunch:** 2 Roti + 1 Bowl Dal + Green Veggie + Salad.")
                st.write("**Dinner:** 2 Roti + Paneer Bhurji + Warm Milk.")
            else:
                st.write("**Early Morning:** 1 Boiled Egg + 5 Soaked Almonds.")
                st.write("**Breakfast:** Egg Omelet OR Chicken Keema Paratha.")
                st.write("**Lunch:** 2 Roti + Chicken/Fish Curry + Spinach + Salad.")
                st.write("**Dinner:** Grilled Fish OR Egg Curry + 1 Roti.")

        elif "PCOS" in st.session_state.stat:
            st.header(f"🌸 Detailed {pref} PCOS Diet")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Cinnamon Water OR ACV.")
                st.write("**Breakfast:** Besan Chilla OR Vegetable Oats.")
                st.write("**Lunch:** 2 Missi Roti + Dal + Curd + Large Salad.")
                st.write("**Dinner:** Soya Chunks OR Tofu Stir-fry.")
            else:
                st.write("**Early Morning:** Lemon water OR Fenugreek water.")
                st.write("**Breakfast:** 2 Egg White Omelet with Mushrooms.")
                st.write("**Lunch:** Grilled Chicken + small portion Brown Rice + Salad.")
                st.write("**Dinner:** Baked Fish OR Chicken Salad.")

    # 4.4 DETAILED EXERCISES (RESTORED FROM DOCUMENTS)
    elif m == "Exercise & Yoga":
        if "Lactating" in st.session_state.stat:
            st.header("🧘 Detailed Lactation Exercise Phase")
            st.write("**Weeks 0–6 (Immediate):** Walking (5-30 mins), Kegels (3 sets of 10), Belly breathing, Pelvic Tilts.")
            st.write("**Weeks 6–12 (Post-Checkup):** Swimming, stationary cycling, modified squats, lunges, and Yoga.")
            st.write("**After 12 Weeks:** Slowly reintroduce jogging or light weights.")
            st.info("Tip: Exercise immediately AFTER feeding to avoid engorgement discomfort.")
        elif "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Wise
