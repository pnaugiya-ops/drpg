import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & SECURITY STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

# This hides the 'Deploy', 'Edit', and 'Menu' buttons from patients
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebarNav"] { background-color: #f8f9fa; }
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'lab_records' not in st.session_state: st.session_state.lab_records = []
if 'appointments' not in st.session_state: st.session_state.appointments = []
if 'blocked_dates' not in st.session_state: st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state: st.session_state.broadcasts = []

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
elif st.session_state.role == "D":
    st.sidebar.markdown(f"### 👩‍⚕️ Welcome, {st.session_state.name}")
    dm = st.sidebar.radio("Doctor Panel", ["Manage Appointments", "Review Patient Reports", "Block Clinic Dates", "Broadcast Media"])
    
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if dm == "Manage Appointments":
        st.header("📅 Patient Appointments")
        if st.session_state.appointments:
            st.table(pd.DataFrame(st.session_state.appointments))
        else: st.info("No appointments currently booked.")

    elif dm == "Review Patient Reports":
        st.header("📋 Patient Lab Records")
        if st.session_state.lab_records:
            st.dataframe(pd.DataFrame(st.session_state.lab_records))
        else: st.info("No lab records found.")

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
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    m = st.sidebar.radio("Go To:", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment", "Doctor's Updates"])
    
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week Tracker")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd_calc = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ EDD: {edd_calc} | Current Week: {wks}")
            
            weeks_data = {
                4: "🌱 Size of a poppy seed. Implantation is occurring.",
                8: "🍇 Size of a raspberry. Heart is beating regularly.",
                12: "🍋 Size of a lime. Baby starts moving fingers and toes.",
                16: "🥑 Size of an avocado. Eyes and ears are moving to position.",
                20: "🍌 Size of a banana. Halfway! You may feel kicks.",
                24: "🌽 Size of an ear of corn. Lungs are beginning to form.",
                28: "🍆 Size of an eggplant. Eyes can open and see light.",
                32: "🥬 Size of a squash. Baby is practicing breathing.",
                36: "🍈 Size of a papaya. Baby is dropping into the pelvis.",
                40: "🍉 Week 40: Full term! Ready for birth."
            }
            current_info = next((v for k, v in weeks_data.items() if wks <= k), "🍉 Reaching full term!")
            st.info(current_info)
        else:
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected Period: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

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
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Hb": hb, "TSH": tsh, "CBC": cbc, "Sugar": sugar, "Urine": urine, "Pulse": pulse})
                st.success("Record Saved!")

    elif m == "Diet Plans":
        pref = st.radio("Select Preference", ["Vegetarian", "Non-Vegetarian"])
        if "Pregnant" in st.session_state.stat:
            st.header(f"🤰 Detailed {pref} Pregnancy Diet")
            d1, d2, d3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with d1:
                if pref == "Vegetarian":
                    st.write("**Early Morning:** 5 soaked almonds + 2 walnuts. \n\n**Breakfast:** Veggie Poha OR Moong Dal Chilla. \n\n**Lunch:** 2 Multigrain Rotis + 1 bowl Dal + Green Veggie + Curd. \n\n**Dinner:** Lauki Sabzi + 1 Roti + Warm Milk.")
                else:
                    # FIXED LINE 157
                    st.write("**Early Morning:** 1 Boiled Egg + 5 almonds. \n\n**Breakfast:** Egg Omelet with veggies. \n\n**Lunch:** Grilled Fish/Chicken + Spinach + Brown rice. \n\n**Dinner:** Chicken Soup + 1 Roti.")
            with d2:
                if pref == "Vegetarian":
                    st.write("**Early Morning:** Soaked nuts + 1 Fig. \n\n**Breakfast:** Ragi Dosa OR Stuffed Paneer Paratha. \n\n**Lunch:** 2 Rotis + Chole/Rajma + Salad + Curd. \n\n**Dinner:** Paneer Bhurji + Veggie Pulao.")
                else:
                    st.write("**Early Morning:** 1 Boiled Egg + 2 Walnuts. \n\n**Breakfast:** Egg Bhurji + 2 Brown bread slices. \n\n**Lunch:** 2 Rotis + Fish Curry + Sprouted salad. \n\n**Dinner:** Lean Meat stir-fry OR Chicken Khichdi.")
            with d3:
                if pref == "Vegetarian":
                    st.write("**Early Morning:** Milk with 1 tsp Ghee + 2 Dates. \n\n**Breakfast:** Oats Porridge OR Veggie Upma. \n\n**Lunch:** 2 Rotis + Dal + Green leafy vegetable + Curd. \n\n**Dinner:** Vegetable Khichdi + Ghee + Warm Milk.")
                else:
                    st.write("**Early Morning:** Milk with dates + 5 almonds. \n\n**Breakfast:** 2 Boiled eggs OR Egg pancakes. \n\n**Lunch:** 2 Rotis + Grilled Fish/Chicken + Steamed Broccoli. \n\n**Dinner:** Chicken Soup OR Egg Curry.")

        elif "PCOS" in st.session_state.stat:
            st.header(f"🌸 Detailed {pref} PCOS Diet Chart")
            st.write("**Early Morning:** Warm water with Cinnamon OR ACV (1 tsp). \n\n**Breakfast:** Besan Chilla with veggies OR Vegetable Oats. \n\n**Mid-Morning:** 1 bowl Papaya OR 5-10 Almonds. \n\n**Lunch:** 1-2 Missi Rotis + 1 bowl Dal + 1 bowl Curd + Salad. \n\n**Evening:** Green Tea + Roasted Makhana. \n\n**Dinner:** Soya chunks curry OR Grilled Protein + 1 Roti.")

        elif "Lactating" in st.session_state.stat:
            st.header(f"🤱 Detailed {pref} Lactation Diet Plan")
            st.write("**Early Morning:** Soaked Methi seeds water. \n\n**Breakfast:** Ragi Porridge OR Methi Paratha. \n\n**Mid-Morning:** 1 fruit + Buttermilk. \n\n**Lunch:** 2-3 Rotis + Masoor Dal + Green leafy veg + Curd. \n\n**Evening:** Warm Milk with 1 Methi/Gond Ladoo. \n\n**Dinner:** Vegetable Khichdi with Ghee.")

    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Detailed Pregnancy Exercise")
            et1, et2, et3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with et1: st.write("- Walking (20 mins), Pelvic Tilts, Deep Breathing.")
            with et2: st.write("- Butterfly Pose, Wall Squats, Cat-Cow Stretch.")
            with et3: st.write("- Birthing Ball, Kegels, Slow Walking.")
        elif "Lactating" in st.session_state.stat:
            st.header("🤱 Postpartum Recovery")
            st.write("- Deep breathing, Kegels, and light walking.")
        else:
            st.header("🏋️ PCOS Strength & Cardio")
            st.write("- Surya Namaskar, Squats, and 45 mins Brisk walking.")

    elif m == "Health Vitals":
        st.header("📈 Record Vitals")
        c1, c2 = st.columns(2)
        with c1:
            h = st.number_input("Height (cm)", 100, 250, 160
