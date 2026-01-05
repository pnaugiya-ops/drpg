import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 15px; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; font-size: 12px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Database Connection Error: {e}")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- 2. LOGIN LOGIC ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            pass_in = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. MAIN APP ---
else:
    # Load Data
    try:
        df = conn.read(ttl=0)
        df = df.fillna('') if df is not None else pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])
    except:
        df = pd.DataFrame(columns=["Name", "Type", "Details", "Timestamp"])

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        # Doctor dashboard logic here...
        if st.sidebar.button("Logout"): 
            st.session_state.logged_in = False
            st.rerun()

    else: # Patient View
        st.sidebar.markdown(f"### Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Book Appointment", "Vitals & BMI", "Upload Reports"])
        
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("👶 Pregnancy & Baby Tracker")
                lmp = st.date_input("Last Menstrual Period (LMP)", value=date.today() - timedelta(days=30))
                edd = lmp + timedelta(days=280)
                weeks = (date.today() - lmp).days // 7
                
                st.success(f"🗓️ **EDD:** {edd.strftime('%d %b %Y')} | ⏳ **Stage:** {weeks} Weeks")
                
                st.subheader("📖 Week-by-Week Development")
                if weeks <= 4:
                    st.info("🌱 **Week 1-4 (The Seed):** Baby is a tiny ball of cells the size of a poppy seed.")
                elif weeks <= 5:
                    st.info("💓 **Week 5 (The Heartbeat):** Size of a sesame seed. The tiny heart tube begins to pulse.")
                elif weeks <= 8:
                    st.info("🍇 **Week 8 (Moving Around):** Size of a raspberry. Fingers and toes are starting to sprout.")
                elif weeks <= 12:
                    st.info("🍋 **Week 12 (Reflexes):** Size of a lime. Baby can open/close fists and make sucking motions.")
                elif weeks <= 20:
                    st.info("🍌 **Week 20 (The Halfway Mark):** Size of a banana. You feel first flutters.")
                elif weeks <= 27:
                    st.info("🥦 **Week 27 (Opening Eyes):** Size of cauliflower. Baby develops sleep cycles.")
                elif weeks >= 38:
                    st.info("🍉 **Week 40 (Full Term):** Size of a watermelon. Ready for birth!")
                else:
                    st.info("👶 Baby is growing vital organs and getting stronger every day.")
                
            else:
                st.header("🗓️ Menstrual Cycle Tracker")
                last_p = st.date_input("Last Period Start", value=date.today() - timedelta(days=28))
                clen = st.slider("Cycle Length", 21, 45, 28)
                st.success(f"🩸 **Next Period:** {(last_p + timedelta(days=clen)).strftime('%d %b %Y')}")
                st.warning(f"🥚 **Ovulation Window:** Around {(last_p + timedelta(days=clen-14)).strftime('%d %b %Y')}")
                

        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness")
                t1, t2 = st.tabs(["🥗 Nutrition", "🧘 Exercises"])
                with t1:
                    tri = st.selectbox("Select Trimester", ["1st (Weeks 1-12)", "2nd (Weeks 13-26)", "3rd (Weeks 27-40)"])
                    if "1st" in tri:
                        st.write("**Focus:** Folic Acid & B6. **Breakfast:** Veggie Poha + Milk.")
                    elif "2nd" in tri:
                        st.write("**Focus:** Calcium & Iron. **Lunch:** Brown rice + Dal + Curd.")
                    else:
                        st.write("**Focus:** High Fiber. **Dinner:** Chapati + Rajma + Sabzi.")
                with t2:
                    st.write("**Recommended:** Walking, Prenatal Yoga, and Pelvic Floor (Kegels).")
                    
            else:
                st.header("🌸 PCOS Wellness Hub")
                t1, t2 = st.tabs(["🥗 PCOS Nutrition", "🏋️ PCOS Exercise"])
                with t1:
                    st.markdown("<div class='diet-box'><b>Focus:</b> 50-60g Protein and 25g Fiber daily.</div>", unsafe_allow_html=True)
