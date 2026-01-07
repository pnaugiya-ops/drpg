import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:4px 12px; border-radius:15px; font-weight:bold; display:inline-block; margin:3px; font-size:13px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border-left:5px solid #ff4b6b; margin-bottom:10px; color: #333; line-height:1.5; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:8px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'labs' not in st.session_state: st.session_state.labs = []
if 'vitals' not in st.session_state: st.session_state.vitals = []
if 'apts' not in st.session_state: st.session_state.apts = []
if 'blocked' not in st.session_state: st.session_state.blocked = []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h2>Dr. Priyanka Gupta</h2><p>MS (Obs & Gynae)</p><div><span class='clinic-badge'>Infertility Specialist</span><span class='clinic-badge'>Ultrasound</span><span class='clinic-badge'>Thyrocare Lab</span></div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Login", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Access Dashboard") and n:
                st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.text_input("Password", type="password") == "clinicadmin786" and st.form_submit_button("Admin Login"):
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 4. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}\n**{st.session_state.stat}**")
    m = st.sidebar.radio("NAVIGATE", ["Tracker", "Diet Plans", "Exercises", "Blood Reports", "Vitals & BMI", "Social Feed", "Book Appointment"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if m == "Tracker":
        st.header("🤰 Pregnancy & Health Tracker")
        if st.session_state.stat == "Pregnant":
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"Due Date: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | Current: Week {wks}")
        else: st.info("Welcome to your daily health overview.")

    elif m == "Diet Plans":
        st.header(f"🥗 Diet Chart: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1: st.markdown("<div class='diet-card'><b>T1 Focus:</b> Folic Acid. 5 Almonds morning. Poha/Oats. Dal-Roti-Sabzi-Curd. Roasted Makhana.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>T2 Focus:</b> Iron/Calcium. Coconut Water, Fruits, Spinach, Paneer, Sprouts.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>T3 Focus:</b> Energy. 6 small meals. Milk with Ghee/Dates. High hydration.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS:</b> Low GI. Flax seeds, Cinnamon water, High protein (Soya/Sprouts). No sugar.</div>", unsafe_allow_html=True)
        else: st.markdown("<div class='diet-card'><b>Lactation:</b> Methi, Jeera, Garlic, Gond Ladoo, Shatavari with milk. 4L water.</div>", unsafe_allow_html=True)

    elif m == "Exercises":
        st.header("🧘 Therapeutic Exercises")
        st.write("- **Butterfly Pose:** For pelvic floor health.\n- **Cat-Cow Stretch:** For back pain relief.\n- **Walking:** 20-30 mins daily.\n- **Breathing:** 10 mins Anulom Vilom.")

    elif m == "Blood Reports":
        st.header("📊 Lab Tracking (CBC/Sugar/Thyroid)")
        with st.form("lab_f"):
            hb = st.number_input("Hemoglobin (Hb)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar", 50, 400, 90)
            tsh = st.number_input("Thyroid (TSH)", 0.0, 50.0, 2.5)
            urine = st.selectbox("Urine Test", ["Normal", "Trace", "+1", "+2"])
            if st.form_submit_button("Record & Chart"):
                st.session_state.labs.append({"User": st.session_state.name, "Date": date.today(), "Hb": hb, "Sugar": sugar, "TSH": tsh, "Urine": urine})
        df = pd.DataFrame([r for r in st.session_state.labs if r['User'] == st.session_state.name])
        if not df.empty: st.line_chart(df.set_index('Date')[['Hb', 'Sugar', 'TSH']])

    elif m == "Vitals & BMI":
        st.header("📈 Vitals & BMI Calculator")
        with st.form("v_f"):
            c1, c2 = st.columns(2)
            p = c1.number_input("Pulse Rate", 40, 150, 72)
            bp = c2.text_input("Blood Pressure", "120/80")
            wt = c1.number_input("Weight (kg)", 30.0, 150.0, 60.0)
            ht = c2.number_input("Height (cm)", 100.0, 220.0, 160.0)
            if st.form_submit_button("Update Vitals"):
                bmi = round(wt / ((ht/100)**2), 2)
                st.session_state.vitals.append({"User": st.session_state.name, "Date": date.today(), "BMI": bmi, "Pulse": p, "BP": bp})
                st.info(f"Calculated BMI: {bmi}")

    elif m == "Social Feed":
        st.header("📺 Health Awareness")
        if st.session_state.social["yt"]: st.video(st.session_state.social["yt"])
        if st.session_state
