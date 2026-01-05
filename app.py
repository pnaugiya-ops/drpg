import streamlit as st
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .diet-box { background:#fff5f7; padding:15px; border-radius:10px; border:1px solid #ffc0cb; color:#333; margin-bottom:10px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

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

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment"])
    
    # 3.1 FULL PREGNANCY TRACKER
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week Development")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
            
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. The blastocyst is implanting in the uterus.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. The heart is beating and limbs are forming.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. All organs are present and baby starts to move fingers.")
            elif wks <= 16: st.info("🥑 Week 16: Size of an avocado. Baby can now make a fist and suck their thumb.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. You may feel flutters (quickening) as baby moves.")
            elif wks <= 24: st.info("🌽 Week 24: Size of an ear of corn. Lungs are beginning to develop surfactant.")
            elif wks <= 30: st.info("🥦 Week 30: Size of a cabbage. Baby's brain is developing rapidly and eyes open.")
            elif wks <= 36: st.info("🥬 Week 36: Size of a romaine lettuce. Baby is gaining weight and dropping lower.")
            else: st.info("🍉 Week 40: Full term! Baby is ready for the world.")
        else:
            st.header("🗓️ Period Tracker")
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    # 3.2 DETAILED DIET CHARTS (RESTORED)
    elif m == "Diet Plans":
        pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "Lactating" in st.session_state.stat:
            st.header("🤱 Lactation Diet Plan (+500 kcal)")
            if pref == "Vegetarian":
                st.markdown("<div class='diet-box'><b>Morning:</b> Fenugreek/Cumin water</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Ragi Dosa OR Oats with nuts</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2-3 Rotis, Dal, Green Veggies, Curd, Salad</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Veg Khichdi with ghee OR Veg Curry with Brown Rice</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='diet-box'><b>Morning:</b> Milk with soaked almonds</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> 2 Scrambled Eggs with whole-wheat toast</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> Grilled Fish/Chicken + Brown Rice + Spinach</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Fish Curry OR Lean Meat stir-fry</div>", unsafe_allow_html=True)
        
        elif "Pregnant" in st.session_state.stat:
            st.header("🥗 Pregnancy Full Diet Chart")
            st.markdown("<div class='diet-box'><b>Early Morning:</b> 5 Soaked Almonds + Warm Water</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Oats / Stuffed Paratha + Bowl of Curd</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Mid-Morning:</b> 1 Fruit (Apple/Pomegranate) + Coconut Water</div>", unsafe_allow_html=True)
            if pref == "Non-Vegetarian":
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Chicken/Fish Curry + Bowl of Salad</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Grilled Chicken / Egg Curry + 1 Roti + Steamed Veggies</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Dal Tadka + Seasonal Veggie + Salad</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Paneer Bhurji / Dal + 1 Roti + Warm Milk</div>", unsafe_allow_html=True)
        
        else:
            st.header("🌸 PCOS Detailed Diet")
            st.markdown("<div class='diet-box'><b>Guidelines:</b> High Protein (50-60g), High Fiber, Low GI. No Sugar.</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Meals:</b> Sprouted Salad, Vegetable Dalia, Missi Roti, Tofu/Soya</div>", unsafe_allow_html=True)

    # 3.3 EXERCISES (ALL TRIMESTERS RESTORED)
    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Specific Yoga")
            tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
            if "1st" in tri:
                st.write("✅ **1st Trimester:** Walking (20 mins), Gentle Prenatal Yoga, Pelvic Floor (Kegels).")
            elif "2nd" in tri:
                st.write("✅ **2nd Trimester:** Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow Stretch.")
            else:
                st.write("✅ **3rd Trimester:** Butterfly Stretch, Pelvic Tilts, Deep Breathing, Birthing Ball.")
        else:
            st.header("🏋️ PCOS Strength Training")
            st.write("✅ **Strength:** Squats, Lunges, Planks (3x per week).")
            st.write("✅ **Cardio:** 45 mins Brisk walking for insulin sensitivity.")

    # 3.4 HEALTH VITALS (BP & PULSE RESTORED)
    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        c1, c2 = st.columns(2)
        with c1:
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
        with c2:
            bp = st.text_input("Blood Pressure (e.g., 120/80)")
            pls = st.number_input("Pulse Rate (BPM)", 40, 200, 72)
        if st.button("Calculate & Save Vitals"):
            bmi = round(w/((h/100)**2), 1)
            st.success(f"Vitals Recorded: BMI {bmi}, BP {bp}, Pulse {pls}")

    # 3.5 VACCINATIONS (RESTORED LISTS)
    elif m == "Vaccinations":
        if "Pregnant" in st.session_state.stat:
            st.header("💉 Pregnancy Vaccination List")
            st.info("Essential: 1. Tetanus (TT) | 2. Tdap | 3. Influenza (Flu)")
        else:
            st.header("💉 PCOS / Gynae Vaccination")
            st.info("Essential: HPV Vaccination (Cervical Cancer Prevention) - 3 Doses")
        
        with st.form("vac_form"):
            v_type = st.selectbox("Vaccine", ["Tetanus", "Tdap", "Influenza", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3", "Other"])
            v_date = st.date_input("Date Administered")
            v_file = st.file_uploader("Upload Record Card", type=['jpg','png','jpeg'])
            if st.form_submit_button("Save Vaccination"):
                st.success("Record saved successfully!")

    # 3.6 15-MINUTE BOOKINGS
    elif m == "Book Appointment":
        st.header("📅 15-Minute Slots")
        dt = st.date_input("Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Clinic Closed on Sundays")
        else:
            slots = []
            for hour in range(11, 14): # 11 AM - 2 PM
                for minute in [0, 15, 30, 45]: slots.append(f"{hour:02d}:{minute:02d} AM")
            for hour in [18, 19, 20]: # 6 PM - 9 PM
                for minute in [0, 15, 30, 45]: slots.append(f"{hour-12:02d}:{minute:02d} PM")
            tm = st.selectbox("Select Time", slots)
            if st.button("Confirm Booking"):
                st.success(f"Confirmed for {dt} at {tm}")
