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
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. Implantation is occurring.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. All major organs are starting to form.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. Baby starts moving fingers and toes.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. Halfway! You will feel the first kicks.")
            elif wks <= 30: st.info("🥦 Week 30: Size of a cabbage. Baby can open eyes and see light.")
            elif wks <= 40: st.info("🍉 Week 40: Full term! Baby is ready to meet the world.")
            
        else:
            st.header("🗓️ Period Tracker")
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")
            

    # 3.2 DETAILED DIET PLANS (PCOS & LACTATION)
    elif m == "Diet Plans":
        pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "PCOS" in st.session_state.stat:
            st.header("🌸 Detailed PCOS Diet Chart")
            if pref == "Vegetarian":
                st.markdown("""<div class='diet-box'><b>Early Morning:</b> Warm water with lemon or cinnamon.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Breakfast:</b> Moong Dal Chilla OR Vegetable Dalia OR Sprouted Salad.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Lunch:</b> 2 Missi Roti + 1 bowl Dal + Green Veggie + Salad.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Dinner:</b> Soya Chunks Curry OR Tofu Stir-fry with vegetables.</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='diet-box'><b>Early Morning:</b> Apple Cider Vinegar in warm water.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Breakfast:</b> 2 Egg Whites + Spinach OR Vegetable Oats.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Lunch:</b> Grilled Chicken/Fish + small bowl Brown Rice + Salad.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Dinner:</b> Baked Salmon OR Chicken Salad (No creamy dressings).</div>""", unsafe_allow_html=True)
        
        elif "Lactating" in st.session_state.stat:
            st.header("🤱 Lactation Diet Plan")
            if pref == "Vegetarian":
                st.markdown("""<div class='diet-box'><b>Breakfast:</b> Oats porridge with nuts OR Ragi dosa.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Lunch:</b> 2-3 Rotis, Dal, Green leafy vegetables, Curd.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Snack:</b> Roasted Makhana OR Methi ladoo with milk.</div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class='diet-box'><b>Breakfast:</b> 2 Scrambled/Boiled eggs with whole-wheat toast.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Lunch:</b> Grilled Chicken/Fish + brown rice + Spinach.</div>""", unsafe_allow_html=True)
                st.markdown("""<div class='diet-box'><b>Dinner:</b> Fish curry (low mercury) OR Lean meat stir-fry.</div>""", unsafe_allow_html=True)

    # 3.3 EXERCISES
    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Specific Yoga")
            tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
            if "1st" in tri: st.write("✅ **1st:** Walking (20 mins), Gentle Yoga, Kegels.")
            elif "2nd" in tri: st.write("✅ **2nd:** Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow.")
            else: st.write("✅ **3rd:** Butterfly Stretch, Pelvic Tilts, Birthing Ball.")
            
        else:
            st.header("🏋️ PCOS Strength Training")
            st.write("✅ **Strength:** Squats, Lunges, Planks (3x per week).")
            st.write("✅ **Cardio:** 45 mins Brisk walking daily.")

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
        if st.button("Calculate & Save"):
            bmi = round(w/((h/100)**2), 1)
            st.success(f"Vitals Recorded: BMI {bmi}, BP {bp}, Pulse {pls}")
            

[Image of BMI category chart]


    # 3.5 VACCINATIONS
    elif m == "Vaccinations":
        if "Pregnant" in st.session_state.stat:
            st.header("💉 Pregnancy Vaccinations")
            st.info("Essential: 1. Tetanus (TT) | 2. Tdap | 3. Influenza (Flu)")
        else:
            st.header("💉 PCOS / Gynae Vaccination")
            st.info("Essential: HPV Vaccination (Cervical Cancer Prevention) - 3 Doses")
        with st.form("vac_form"):
            v_type = st.selectbox("Vaccine", ["Tetanus", "Tdap", "Influenza", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3", "Other"])
            v_date = st.date_input("Date")
            v_file = st.file_uploader("Upload Record Card", type=['jpg','png','jpeg'])
            if st.form_submit_button("Save"): st.success("Record saved!")

    # 3.6 15-MINUTE BOOKINGS
    elif m == "Book Appointment":
        st.header("📅 15-Minute Slots")
        dt = st.date_input("Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Clinic Closed on Sundays")
        else:
            slots = [f"{h:02d}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]] + [f"{h-12:02d}:{m:02d} PM" for h in [18, 19, 20] for m in [0, 15, 30, 45]]
            tm = st.selectbox("Select Time", slots)
            if st.button("Confirm Booking"): st.success(f"Confirmed for {dt} at {tm}")
