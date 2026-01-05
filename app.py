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
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 15px; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; font-size: 12px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Database Connection Error. Please verify secrets.toml.")

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
    # Sidebar Logout Button (Always Visible)
    if st.sidebar.button("🔓 Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        st.info("Check Google Sheets for the latest appointments and reports.")
        
    else: # Patient View
        st.sidebar.markdown(f"### Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Book Appointment", "Vitals & BMI", "Upload Reports"])
        
        # 3.1 TRACKER & CALCULATOR
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy & Baby Tracker")
                lmp = st.date_input("Select LMP", value=date.today() - timedelta(days=30))
                weeks = (date.today() - lmp).days // 7
                st.success(f"🗓️ EDD: {(lmp + timedelta(days=280)).strftime('%d %B %Y')} | ⏳ Stage: {weeks} Weeks")
                
                st.subheader("📖 Week-by-Week Development")
                if weeks <= 4: 
                    st.info("🌱 **Week 4 (Poppy Seed):** Baby is a tiny ball of cells snuggling into the womb.")
                elif weeks <= 8:
                    st.info("🍇 **Week 8 (Raspberry):** Fingers and toes are starting to sprout.")
                elif weeks <= 12:
                    st.info("🍋 **Week 12 (Lime):** Baby can open/close fists and make sucking motions.")
                elif weeks <= 20:
                    st.info("🍌 **Week 20 (Banana):** Halfway mark! You will feel the first flutters.")
                elif weeks >= 38:
                    st.info("🍉 **Week 40 (Watermelon):** Full term! Ready for the world.")
                else:
                    st.info("👶 Baby is growing fast, developing senses, and practicing breathing.")
                
            else:
                st.header("🗓️ Menstrual Cycle Tracker")
                lp = st.date_input("Last Period Start", value=date.today() - timedelta(days=28))
                st.success(f"🩸 Next Period Expected: {(lp + timedelta(days=28)).strftime('%d %B %Y')}")
                

        # 3.2 DIET & YOGA (Fixed and Restored)
        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness Hub")
                d_tab, e_tab = st.tabs(["🥗 Nutrition Plan", "🧘 Trimester Exercises"])
                with d_tab:
                    tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                    if "1st" in tri:
                        st.markdown("""<div class='diet-box'><b>Focus: Folic Acid.</b><br>
                        - Early Morning: Warm water + 5 almonds.<br>
                        - Breakfast: Veggie Poha + Milk.<br>
                        - Lunch: 2 Rotis + Spinach Dal + Curd.</div>""", unsafe_allow_html=True)
                    elif "2nd" in tri:
                        st.markdown("""<div class='diet-box'><b>Focus: Calcium & Iron.</b><br>
                        - Breakfast: Multigrain paratha + Curd.<br>
                        - Lunch: Brown rice + Dal + Sautéed Veggies.<br>
                        - Dinner: Paneer curry + Chapati.</div>""", unsafe_allow_html=True)
                    else:
                        st.markdown("""<div class='diet-box'><b>Focus: High Fiber.</b><br>
                        - Breakfast: Besan Chilla or Oats.<br>
                        - Lunch: Millet Khichdi + Dal + Salad.<br>
                        - Dinner: Chapati + Rajma/Chole + Vegetable Sabzi.</div>""", unsafe_allow_html=True)
                with e_tab:
                    st.write("**1st Tri:** Walking, Prenatal Yoga, Kegels.")
                    st.write("**2nd Tri:** Swimming, Wall Squats, Side-Lying Leg Lifts.")
                    st.write("**3rd Tri:** Butterfly Stretch, Pelvic Tilts, Birthing Ball.")
                    
            else:
                st.header("🌸 PCOS Wellness Hub")
                st.markdown("""<div class='diet-box'><b>PCOS Principles:</b> 50-60g Protein, 25g Fiber daily.<br>
                <b>Strength Training:</b> Squats, Lunges, Push-ups (3-4x
