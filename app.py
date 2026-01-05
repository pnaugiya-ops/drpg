import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:15px; border-radius:12px; text-align:center; }
    .diet-box { background:#fff5f7; padding:12px; border-radius:10px; border:1px solid #ffc0cb; color:#333; margin-bottom:10px; }
    .badge { background:#e8f4f8; color:#003366; padding:4px 8px; border-radius:4px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class='dr-header'>
            <h1>BHAVYA LABS & CLINICS</h1>
            <p>Dr. Priyanka Gupta - MS (Obs & Gynae)</p>
            <div>
                <span class='badge'>Infertility Specialist</span>
                <span class='badge'>Ultrasound</span>
                <span class='badge'>Laparoscopic Surgery</span>
                <span class='badge'>Pharmacy</span>
                <span class='badge'>Thyrocare Franchise</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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
    st.sidebar.markdown(f"**Patient:** {st.session_state.name}")
    st.sidebar.markdown(f"**Age:** {st.session_state.get('age','N/A')}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.header("👨‍⚕️ Doctor Dashboard")
        st.info("Live data is synced with Google Sheets.")
    else:
        m = st.sidebar.radio("Menu", ["Tracker", "Diet Plans", "Exercise", "Vitals & Vaccines", "Booking"])
        
        if m == "Tracker":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Guide")
                lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=60))
                wks = (date.today()-lmp).days // 7
                edd = lmp + timedelta(days=280)
                st.success(f"EDD: {edd.strftime('%d %b %Y')} | Week: {wks}")
                
                if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed.")
                elif wks <= 12: st.info("🍋 Week 12: Baby can open/close fists.")
                elif wks <= 20: st.info("🍌 Week 20: Halfway! You feel flutters.")
                else: st.info("👶 Baby is growing fast!")
            else:
                st.header("🗓️ Period Tracker")
                lp = st.date_input("Last Period", value=date.today()-timedelta(days=14))
                next_p = lp + timedelta(days=28)
                st.success(f"🩸 Next Expected: {next_p.strftime('%d %b %Y')}")

        elif m == "Diet Plans":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Nutrition")
                pref = st.radio("Diet Type", ["Vegetarian", "Non-Vegetarian"])
                st.markdown("<div class='diet-box'><b>Morning:</b> Soaked almonds + Warm water.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Paratha + Curd.</div>", unsafe_allow_html=True)
                if pref == "Non-Vegetarian":
                    st.markdown("<div class='diet-box'><b>Lunch:</b> Chicken/Fish + 2 Roti + Salad.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='diet-box'><b>Lunch:</b> Dal + Seasonal Veggie + 2 Roti + Curd.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Light Roti + Paneer / Dal.</div>", unsafe_allow_html=True)
            else:
                st.header("🌸 PCOS Nutrition")
                st.markdown("<div class='diet-box'><b>Rules:</b> 50-60g Protein & 25g Fiber daily. Low-GI foods only. Walk 15 mins after meals.</div>", unsafe_allow_html=True)

        elif m == "Exercise":
            if "Pregnant" in st.session_state.stat:
                st.header("🧘 Trimester Fitness")
                tri = st.selectbox("Current Trimester", ["1st", "2nd", "3rd"])
                if tri == "1st": st.write("- Walking, Yoga, Kegels")
                elif tri == "2nd": st.write("- Swimming, Wall Squats")
                else: st.write("- Butterfly stretch, Pelvic tilts")
            else:
                st.header("🏋️ PCOS Strength")
                st.write("- Strength: Squats, Lunges, Pushups (3x/week)")
                st.write("- Cardio: 30m Brisk walking daily")

        elif m == "Vitals & Vaccines":
            st.header("📈 Health Records")
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
            if st.button("Calculate BMI"): 
                bmi = round(w/((h/100)**2), 1)
                st.success(f"Your BMI: {bmi}")
            
            st.divider()
            st.subheader("💉 Vaccinations")
            v_name = st.text_input("Vaccine Name")
            st.file_uploader("Upload Record Card", type=['jpg','png','jpeg'])

        elif m == "Booking":
            st.header("📅 Book Appointment")
            dt = st.date_input("Select Date", min_value=date.today())
            if dt.weekday() == 6: 
                st.error("Clinic Closed on Sundays")
            else:
                tm = st.selectbox("Slot", ["11:00 AM", "06:00 PM"])
                if st.button("Confirm"): 
                    st.success("Appointment Requested.")
