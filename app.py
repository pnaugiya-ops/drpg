import streamlit as st
from streamlit_gsheets import GSheetsConnection
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

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.info("Live patient data is connected via Google Sheets.")
    else:
        m = st.sidebar.radio("Navigation", ["Health Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment"])
        
        # 3.1 TRACKER
        if m == "Health Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Week-by-Week")
                lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
                wks = (date.today()-lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
            elif "Lactating" in st.session_state.stat:
                st.header("🤱 Postpartum Recovery")
                st.info("Focus on healing and supporting your baby's growth.")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        # 3.2 DIET PLANS
        elif m == "Diet Plans":
            pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
            
            if "Lactating" in st.session_state.stat:
                st.header("🤱 Lactation Diet Plan")
                [cite_start]st.info("Goal: +300–500 extra calories per day for milk production[cite: 1].")
                if pref == "Vegetarian":
                    [cite_start]st.markdown("<div class='diet-box'><b>Early Morning:</b> Soaked fenugreek seeds or cumin water[cite: 8].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Breakfast:</b> Ragi dosa or Oats porridge with almonds/walnuts[cite: 8].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Lunch:</b> Whole wheat rotis, Moong/Masoor dal, Spinach/Methi, Curd, and Salad[cite: 8].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Evening:</b> Roasted Makhana or Paneer tikka or Methi/Gond ladoo with milk[cite: 8].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Dinner:</b> Vegetable Khichdi with ghee or mixed vegetable curry[cite: 8].</div>", unsafe_allow_html=True)
                else:
                    [cite_start]st.markdown("<div class='diet-box'><b>Early Morning:</b> Fenugreek water or Milk with almonds[cite: 11].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Breakfast:</b> 2 Scrambled/Boiled eggs with whole-wheat toast[cite: 11].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Lunch:</b> Grilled/Curried Chicken or Fish (Salmon/Trout) with brown rice and spinach[cite: 11].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Evening:</b> Chicken/Lentil soup or Walnuts and raisins[cite: 11].</div>", unsafe_allow_html=True)
                    [cite_start]st.markdown("<div class='diet-box'><b>Dinner:</b> Fish curry (low mercury) or Lean meat stir-fry with quinoa[cite: 11].</div>", unsafe_allow_html=True)
            
            elif "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Diet Chart")
                st.markdown("<div class='diet-box'><b>Morning:</b> Soaked Almonds + Warm Water</div>", unsafe_allow_html=True)
                if pref == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Chicken/Fish Curry + Salad</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Dal + Veggie + Curd</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> 1 Roti + Paneer/Dal/Egg + Milk</div>", unsafe_allow_html=True)
            
            else:
                st.header("🌸 Detailed PCOS Diet Plan")
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Sprouted Salad / Veg Dalia (Low sugar)</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Missi Roti + 1 Bowl Dal + Green Veggie + Salad</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Clear Soup + Tofu/Soya/Grilled Veggies</div>", unsafe_allow_html=True)

        # 3.3 EXERCISE
        elif m == "Exercise & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🧘 Trimester Fitness")
                tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                if "1st" in tri: st.write("✅ Walking (20 mins), Prenatal Yoga, Kegels.")
                elif "2nd" in tri: st.write("✅ Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow Stretch.")
                else: st.write("✅ Butterfly Stretch, Pelvic Tilts, Deep Breathing, Birthing Ball.")
            else:
                st.header("🏋️ Detailed PCOS Exercise Plan")
                st.write("✅ **Strength (3x/Week):** Squats, Lunges, Planks to improve insulin sensitivity.")
                st.write("✅ **HIIT/Cardio:** 15 mins HIIT or 45 mins Brisk Walking daily.")
                st.write("✅ **Yoga:** Surya Namaskar and Cobra Pose for hormonal balance.")

        # 3.4 HEALTH VITALS
        elif m == "Health Vitals":
            st.header("📈 Health Vitals")
            c1, c2 = st.columns(2)
            with c1:
                h = st.number_input("Height (cm)", 100, 250, 160)
                w = st.number_input("Weight (kg)", 30, 200, 60)
            with c2:
                bp = st.text_input("Blood Pressure (e.g., 120/80)")
                pls = st.number_input("Pulse Rate (BPM)", 40, 200, 72)
            if st.button("Calculate and Save"):
                bmi = round(w/((h/100)**2), 1)
                st.success(f"BMI: {bmi} | BP: {bp} | Pulse: {pls}")

        # 3.5 VACCINATIONS
        elif m == "Vaccinations":
            if "Pregnant" in st.session_state.stat:
                st.header("💉 Pregnancy Vaccinations")
                st.info("Essential: 1. Tetanus (TT) | 2. Tdap | 3. Influenza (Flu)")
            else:
                st.header("💉 PCOS / Gynae Vaccinations")
                st.info("Essential: HPV Vaccination (Cervical Cancer Prevention) - 3 Doses")
            
            with st.form("vac"):
                v = st.selectbox("Vaccine Type", ["Tetanus", "Tdap", "Influenza", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3", "Other"])
                d = st.date_input("Date Received")
                f = st.file_uploader("Upload Record", type=['jpg','png','jpeg'])
                if st.form_submit_button("Save Vaccination"): st.success("Record Saved!")

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
                tm = st.selectbox("Time", slots)
                if st.button("Confirm"): st.success(f"Request sent for {dt} at {tm}")
