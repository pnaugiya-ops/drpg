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

# --- 3. MAIN APPLICATION ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment"])
    
    # 3.1 PREGNANCY/PERIOD TRACKER
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. Implantation is occurring.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. Heart is beating.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. Baby starts moving fingers.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. Halfway! You feel kicks.")
            elif wks <= 30: st.info("🥦 Week 30: Size of a cabbage. Eyes open.")
            elif wks <= 40: st.info("🍉 Week 40: Full term! Ready for birth.")
        else:
            st.header("🗓️ Period Tracker")
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    # 3.2 RESTORED LAB REPORTS & TRENDS
    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report Monitoring")
        with st.form("lab_entry"):
            col1, col2 = st.columns(2)
            with col1:
                test_date = st.date_input("Test Date", value=date.today())
                hb = st.number_input("Hemoglobin (g/dL)", 5.0, 20.0, 12.0)
                tsh = st.number_input("TSH (mIU/L)", 0.0, 20.0, 2.5)
            with col2:
                cbc = st.number_input("WBC Count (cells/mcL)", 1000, 20000, 7000)
                sugar = st.number_input("Blood Sugar (mg/dL)", 50, 500, 90)
                urine = st.selectbox("Urine Protein/Sugar", ["Nil", "Trace", "1+", "2+", "3+"])
            
            if st.form_submit_button("Add Entry & Update Chart"):
                st.session_state.lab_records.append({
                    "Date": test_date, "Hb": hb, "TSH": tsh, 
                    "WBC": cbc, "Sugar": sugar, "Urine": urine
                })
                st.success("Record Added!")

        if st.session_state.lab_records:
            df = pd.DataFrame(st.session_state.lab_records).sort_values("Date")
            st.subheader("📈 Health Trends Over Time")
            chart_type = st.selectbox("Select Metric to View Trend", ["Hb", "TSH", "Sugar", "WBC"])
            st.line_chart(df.set_index("Date")[chart_type])
            st.write("**History Table**")
            st.table(df)

    # 3.3 DIET PLANS
    elif m == "Diet Plans":
        pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        if "PCOS" in st.session_state.stat:
            st.header("🌸 Detailed PCOS Diet Plan")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with lemon or cinnamon.")
                st.write("**Breakfast:** Moong Dal Chilla OR Vegetable Dalia OR Sprouted Salad.")
                st.write("**Lunch:** 2 Missi Roti + 1 bowl Dal + Green Veggie + Salad.")
                st.write("**Dinner:** Soya Chunks Curry OR Tofu Stir-fry with vegetables.")
            else:
                st.write("**Early Morning:** Apple Cider Vinegar in warm water.")
                st.write("**Breakfast:** 2 Egg Whites + Spinach OR Vegetable Oats.")
                st.write("**Lunch:** Grilled Chicken/Fish + small bowl Brown Rice + Salad.")
                st.write("**Dinner:** Baked Salmon OR Chicken Salad.")
        elif "Lactating" in st.session_state.stat:
            st.header("🤱 Detailed Lactation Diet Plan")
            st.info("Additional 300–500 calories per day to support milk production.")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with soaked fenugreek or cumin water.")
                st.write("**Breakfast:** Oats porridge with nuts OR Ragi dosa OR Methi paratha with curd.")
                st.write("**Lunch:** 2–3 Rotis + 1 bowl Dal + Green leafy vegetable + Curd + Salad.")
                st.write("**Dinner:** Vegetable Khichdi with ghee OR Brown rice with veg curry.")
            else:
                st.write("**Early Morning:** Fenugreek water OR Milk with soaked almonds.")
                st.write("**Breakfast:** 2 Eggs with toast OR Oats porridge with seeds/fruits.")
                st.write("**Lunch:** Chicken/Fish Curry + Brown Rice + Spinach sabzi.")
                st.write("**Dinner:** Fish curry (low mercury) OR Lean meat stir-fry.")
        else:
            st.header("🥗 Detailed Pregnancy Diet Chart")
            st.write("**Early Morning:** 5 Soaked Almonds + Warm Water.")
            st.write("**Breakfast:** Veggie Poha / Oats / Stuffed Paratha + 1 Bowl Curd.")
            st.write("**Lunch:** 2 Roti + Dal Tadka + Seasonal Veggie + Salad.")
            st.write("**Dinner:** 1 Roti + Paneer/Dal/Chicken + Warm Milk.")

    # 3.4 EXERCISES (INCLUDING LACTATION UPDATES)
    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Specific Yoga")
            tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
            if "1st" in tri: st.write("✅ **1st:** Walking (20 mins), Gentle Yoga, Kegels.")
            elif "2nd" in tri: st.write("✅ **2nd:** Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow.")
            else: st.write("✅ **3rd:** Butterfly Stretch, Pelvic Tilts, Birthing Ball.")
        elif "Lactating" in st.session_state.stat:
            st.header("🧘 Postpartum Recovery Exercise")
            st.write("**Weeks 0–6:** Short walks (5-30 mins), Kegels (3 sets of 10), Belly breathing.")
            st.write("**Weeks 6–12:** Swimming, modified squats, and Yoga.")
            st.write("- **Tip:** Exercise *after* feeding to avoid breast engorgement discomfort.")
        else:
            st.header("🏋️ PCOS Strength Training")
            st.write("✅ **Strength:** Squats, Lunges, Planks.")
            st.write("✅ **Cardio:** 45 mins Brisk walking daily.")

    # 3.5 HEALTH VITALS
    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        c1, c2 = st.columns(2)
        with c1:
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
        with c2:
            bp = st.text_input("Blood Pressure (e.g., 120/80)")
            pls = st.number_input("Pulse Rate (BPM)", 40, 200, 72)
        if st.button("Calculate & Save"):
            bmi = round(w/((h/100)**2), 1)
            st.success(f"Vitals Recorded: BMI {bmi}, BP {bp}, Pulse {pls}")

    # 3.6 VACCINATIONS
    elif m == "Vaccinations":
        st.header("💉 Vaccination Records")
        if "Pregnant" in st.session_state.stat:
            st.info("Essential: 1. Tetanus (TT) | 2. Tdap | 3. Influenza (Flu)")
        else:
            st.info("Essential: HPV Vaccination (3 Doses)")
        with st.form("vac_form"):
            v_type = st.selectbox("Vaccine", ["Tetanus", "Tdap", "Influenza", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3", "Other"])
            v_date = st.date_input("Date")
            if st.form_submit_button("Save"): st.success("Record saved!")

    # 3.7 15-MINUTE BOOKINGS
    elif m == "Book Appointment":
        st.header("📅 15-Minute Slots")
        dt = st.date_input("Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Clinic Closed on Sundays")
        else:
            slots = [f"{h:02d}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]] + [f"{h-12:02d}:{m:02d} PM" for h in [18, 19, 20] for m in [0, 15, 30, 45]]
            tm = st.selectbox("Select Time", slots)
            if st.button("Confirm Booking"): st.success(f"Confirmed for {dt} at {tm}")
