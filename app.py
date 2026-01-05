import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 15px; border-radius: 10px; border: 1px solid #ffc0cb; color: #333; margin-bottom: 10px; font-size: 14px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 2px; font-size: 11px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("Database Connection Error.")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & CLINIC BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "age":a, "stat":s, "role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APPLICATION ---
else:
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}\n\n**Age:** {st.session_state.get('age', 'N/A')}")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.write("Access records via Google Sheets.")
    
    else:
        m = st.sidebar.radio("Menu", ["Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccination Record", "Book Appointment"])
        
        # 3.1 TRACKER (Source: Here is a week.docx)
        if m == "Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Guide")
                lmp = st.date_input("LMP Date", value=date.today() - timedelta(days=60))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Week: {weeks}")
                
                if weeks <= 4: st.info("🌱 **Week 4:** Baby is the size of a poppy seed.")
                elif weeks <= 8: st.info("🍇 **Week 8:** Raspberry size. Fingers and toes sprouting.")
                elif weeks <= 12: st.info("🍋 **Week 12:** Lime size. Baby can make sucking motions.")
                elif weeks <= 20: st.info("🍌 **Week 20:** Banana size. You'll feel 'flutters'.")
                elif weeks >= 38: st.info("🍉 **Week 40:** Watermelon size. Ready for birth!")
                else: st.info("👶 Baby is growing vital senses daily.")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=14))
                st.success(f"🩸 Next Expected: {(lp + timedelta(days=28)).strftime('%d %b %Y')}")
                

        # 3.2 DIET PLANS (Detailed Integrated)
        elif m == "Diet Plans":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Diet")
                pref = st.radio("Type", ["Vegetarian", "Non-Vegetarian"])
                st.markdown("<div class='diet-box'><b>Early Morning:</b> Soaked almonds + Warm water.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Stuffed Paratha + Curd.</div>", unsafe_allow_html=True)
                if pref == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>Lunch Option:</b> Grilled Fish or Lean Chicken + 2 Roti + Salad.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='diet-box'><b>Lunch Option:</b> Dal + Seasonal Veggie + 2 Roti + Curd.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Light Chapati + Paneer / Dal / Steamed Veggies.</div>", unsafe_allow_html=True)
            else:
                st.header("🌸 PCOS Nutrition")
                st.markdown("<div class='diet-box'><b>PCOS Plan:</b> 50-60g Protein & 25g Fiber daily. Low-GI foods only. Walk 15 mins after every meal.</div>", unsafe_allow_html=True)

        # 3.3 EXERCISE (Source: Trimester & Strength docs)
        elif m == "Exercise & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🧘 Trimester Fitness")
                tri = st.selectbox("Current Trimester", ["1st", "2nd", "3rd"])
                if tri == "1st": st.write("- Walking & Prenatal Yoga\n- Pelvic Floor (Kegels)")
                elif tri == "2nd": st.write("- Swimming & Wall Squats\n- Side-Lying Leg Lifts")
                else: st.write("- Butterfly Stretch & Pelvic Tilts\n- Birthing Ball")
                
            else:
                st.header("🏋️ PCOS Strength Training")
                st.write("- **Strength:** Squats, Lunges, Push-ups (3-4x/week)")
                st.write("- **LISS:** Brisk walking (30-45 mins) for insulin sensitivity")

        # 3.4 VITALS & VACCINATION
        elif m == "Health Vitals":
            st.header("📈 Track Health Vitals")
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
            bp = st.text_input("Blood Pressure (e.g. 120/80)")
            sugar = st.number_input("Blood Sugar", 50, 500, 100)
            if st.button("Calculate BMI"):
                bmi = round(w / ((h/100)**2), 1)
                st.success(f"BMI: {bmi}")
                

[Image of BMI category chart]


        elif m == "Vaccination Record":
            st.header("💉 Vaccination Portal")
            v_name = st.text_input("Vaccine Name")
            st.file_uploader("Upload Record Card", type=['jpg','png','jpeg'])
            if st.button("Save"): st.success("Record Saved!")

        elif m == "Book Appointment":
            st.header("📅 Clinic Booking")
            dt = st.date_input("Date", min_value=date.today())
            if dt.weekday() == 6: st.error("Clinic Closed on Sundays")
            else:
                tm = st.selectbox("Slot", ["11:00 AM", "12:00 PM", "06:00 PM", "07:00 PM"])
                if st.button("Confirm"): st.success("Appointment Requested.")
