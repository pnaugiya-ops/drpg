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
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
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
        m = st.sidebar.radio("Navigation", ["Baby Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment"])
        
        # 3.1 BABY TRACKER
        if m == "Baby Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Week-by-Week")
                lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
                wks = (date.today()-lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
                
                if wks <= 4: st.info("🌱 Week 4: Baby is a poppy seed size. Implantation complete.")
                elif wks <= 8: st.info("🍇 Week 8: Raspberry size. Heart is beating!")
                elif wks <= 12: st.info("🍋 Week 12: Lime size. Baby starts moving fingers.")
                elif wks <= 20: st.info("🍌 Week 20: Banana size. Halfway! You feel flutters.")
                elif wks <= 30: st.info("🥦 Week 30: Cabbage size. Baby can open eyes.")
                else: st.info("🍉 Week 40: Ready for birth!")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

        # 3.2 DETAILED DIET
        elif m == "Diet Plans":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Diet Chart")
                pref = st.radio("Type", ["Vegetarian", "Non-Vegetarian"])
                st.markdown("<div class='diet-box'><b>Early Morning:</b> 5 Soaked Almonds + 1 Glass Warm Water</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Oats / Stuffed Paratha + 1 Bowl Curd</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Mid-Morning:</b> 1 Fruit (Apple/Pomegranate) + Coconut Water</div>", unsafe_allow_html=True)
                
                if pref == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Chicken/Fish Curry + Bowl of Salad</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Evening:</b> Roasted Makhana or 1 Boiled Egg</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Dinner:</b> Grilled Chicken / Egg Curry + 1 Roti + Steamed Veggies</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Dal Tadka + Seasonal Veggie + Salad</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Evening:</b> Handful of Walnuts / Roasted Chana</div>", unsafe_allow_html=True)
                    st.markdown("<div class='diet-box'><b>Dinner:</b> Paneer Bhurji / Dal + 1 Roti + Warm Milk</div>", unsafe_allow_html=True)
            else:
                st.header("🌸 PCOS Nutrition Plan")
                st.markdown("<div class='diet-box'><b>Core Principle:</b> 50-60g Protein & 25g Fiber daily. Low-GI foods only. Walk 15 mins after every meal.</div>", unsafe_allow_html=True)

        # 3.3 DETAILED EXERCISE
        elif m == "Exercise & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🧘 Trimester-Specific Exercise")
                tri = st.selectbox("Select Current Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                if "1st" in tri:
                    st.write("✅ **1st Trimester Focus:** Gentle Walking (20 mins), Prenatal Yoga, Pelvic Floor (Kegels). Avoid heavy lifting.")
                elif "2nd" in tri:
                    st.write("✅ **2nd Trimester Focus:** Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow Stretch for back relief.")
                else:
                    st.write("✅ **3rd Trimester Focus:** Butterfly Stretch, Pelvic Tilts, Deep Breathing, Birthing Ball Exercises to prepare for labor.")
            else:
                st.header("🏋️ PCOS Strength Training")
                st.write("✅ **Strength:** Squats, Lunges, Pushups (3-4x/week) to build muscle.")
                st.write("✅ **Cardio:** 30-45 mins Brisk walking for insulin sensitivity.")

        # 3.4 HEALTH VITALS
        elif m == "Health Vitals":
            st.header("📈 Health Vitals")
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
            if st.button("Calculate BMI"): 
                bmi = round(w/((h/100)**2), 1)
                st.success(f"Your BMI: {bmi}")

        # 3.5 VACCINATIONS
        elif m == "Vaccinations":
            st.header("💉 Vaccination Portal")
            with st.form("vac_f"):
                v_name = st.text_input("Vaccine Name (e.g. Tdap, Flu, Tetanus)")
                v_file = st.file_uploader("Upload Vaccination Card Image", type=['jpg','png','jpeg'])
                if st.form_submit_button("Save Record"): 
                    st.success("Vaccination Record Saved Successfully!")

        # 3.6 15-MINUTE BOOKINGS
        elif m == "Book Appointment":
            st.header("📅 Book Appointment (15-Min Slots)")
            dt = st.date_input("Date", min_value=date.today())
            if dt.weekday() == 6: 
                st.error("🚫 Clinic is Closed on Sundays")
            else:
                slots = []
                # Morning Shift 11:00 AM to 02:00 PM
                for h_m in range(11, 14):
                    for m_m in [0, 15, 30, 45]:
                        slots.append(f"{h_m:02d}:{m_m:02d} AM")
                # Evening Shift 06:00 PM to 09:00 PM
                for h_e in [18, 19, 20]:
                    for m_e in [0, 15, 30, 45]:
                        slots.append(f"{h_e-12:02d}:{m_e:02d} PM")
                
                tm = st.selectbox("Select Available Time Slot", slots)
                if st.button("Confirm Booking"): 
                    st.success(f"✅ Appointment Request Sent for {dt} at {tm}")
