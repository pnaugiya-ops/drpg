import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .diet-card { background:#ffffff; padding:15px; border-radius:10px; border-left:5px solid #ff4b6b; margin-bottom:10px; color: #333; }
    .stButton>button { background:#ff4b6b !important; color:white !important; border-radius:8px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
for key in ['logged_in', 'labs', 'vitals', 'apts', 'blocked']:
    if key not in st.session_state: st.session_state[key] = False if key=='logged_in' else []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h2>Dr. Priyanka Gupta</h2><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Login", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter") and n:
                st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.text_input("Password", type="password") == "clinicadmin786" and st.form_submit_button("Login"):
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 4. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.sidebar.markdown(f"### 📋 {st.session_state.name}\n**{st.session_state.stat}**")
    m = st.sidebar.radio("MENU", ["Tracker", "Diet Plans", "Exercises", "Blood Reports", "Vitals & BMI", "Social Feed", "Book Appointment"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if m == "Tracker":
        st.header("📈 Health Tracker")
        if st.session_state.stat == "Pregnant":
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"Due Date: {(lmp + timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
        else: st.info("Welcome to your dashboard.")

    elif m == "Diet Plans":
        st.header(f"🥗 Diet: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1: st.markdown("<div class='diet-card'><b>T1:</b> 5 Almonds morning. Poha/Oats. Roti, Dal, Curd. Roasted Makhana.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>T2:</b> Coconut Water, Fruits, Spinach, Paneer, Sprouts. High protein.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>T3:</b> 6 small meals. Milk with Ghee/Dates. Focus on hydration.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS:</b> Low GI. Flax seeds. Cinnamon water. High protein. No sugar/Maida.</div>", unsafe_allow_html=True)
        else: st.markdown("<div class='diet-card'><b>Lactation:</b> Soaked Methi, Jeera, Garlic, Gond Ladoo, Shatavari.</div>", unsafe_allow_html=True)

    elif m == "Exercises":
        st.header("🧘 Exercises")
        st.write("- **Butterfly Pose:** For pelvic flexibility.\n- **Cat-Cow:** For back relief.\n- **Walking:** 20 mins daily.")

    elif m == "Blood Reports":
        st.header("📊 Blood Reports Tracking")
        with st.form("lab_f"):
            h = st.number_input("Hemoglobin (Hb)", 5.0, 18.0, 12.0)
            s = st.number_input("Blood Sugar", 50, 400, 90)
            t = st.number_input("Thyroid (TSH)", 0.0, 50.0, 2.5)
            u = st.selectbox("Urine Test", ["Normal", "Trace", "+1", "+2"])
            if st.form_submit_button("Save & Update"):
                st.session_state.labs.append({"User":st.session_state.name, "Date":date.today(), "Hb":h, "Sugar":s, "TSH":t, "Urine":u})
        df = pd.DataFrame([r for r in st.session_state.labs if r['User']==st.session_state.name])
        if not df.empty: st.line_chart(df.set_index('Date')[['Hb', 'Sugar', 'TSH']])

    elif m == "Vitals & BMI":
        st.header("📈 Vitals & BMI")
        with st.form("v_f"):
            p, bp = st.number_input("Pulse", 40, 150, 72), st.text_input("BP", "120/80")
            wt, ht = st.number_input("Weight (kg)", 30.0, 150.0, 60.0), st.number_input("Height (cm)", 100.0, 220.0, 160.0)
            if st.form_submit_button("Log Vitals"):
                bmi = round(wt / ((ht/100)**2), 2)
                st.session_state.vitals.append({"User":st.session_state.name, "Date":date.today(), "BMI":bmi, "Pulse":p, "BP":bp})
                st.info(f"BMI: {bmi}")

    elif m == "Social Feed":
        st.header("📺 Social Media Updates")
        if st.session_state.social["yt"]: st.video(st.session_state.social["yt"])
        if st.session_state.social["ig"]: st.info(f"Instagram: {st.session_state.social['ig']}")

    elif m == "Book Appointment":
        st.header("📅 Schedule")
        # 15-min slots: 11:15-2:00 and 6:00-8:00
        slots = [f"11:{m:02d} AM" for m in [15, 30, 45]] + [f"12:{m:02d} PM" for m in [0, 15, 30, 45]] + [f"1:{m:02d} PM" for m in [0, 15, 30, 45]] + ["2:00 PM"]
        slots += [f"{h}:{m:02d} PM" for h in [6, 7] for m in [0, 15, 30, 45]] + ["8:00 PM"]
        d = st.date_input("Date", min_value=date.today())
        t = st.selectbox("Slot", slots)
        if st.button("Request"):
            if d in st.session_state.blocked: st.error("Closed today.")
            else:
                st.session_state.apts.append({"Patient":st.session_state.name, "Date":d, "Time":t})
                st.success("Requested!")

# --- 5. ADMIN PORTAL ---
elif st.session_state.role == "D":
    st.sidebar.title("👩‍⚕️ Admin")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    t1, t2, t3, t4 = st.tabs(["Appointments", "Patient Records", "Manage Dates", "Social Media"])
    with t1:
        st.table(pd.DataFrame(st.session_state.apts) if st.session_state.apts else "No Bookings.")
    with t2:
        st.subheader("Lab Data")
        st.dataframe(pd.DataFrame(st.session_state.labs))
        st.subheader("Vital Data")
        st.dataframe(pd.DataFrame(st.session_state.vitals))
    with t3:
        bd = st.date_input("Block Date")
        if st.button("Block"):
            st.session_state.blocked.append(bd)
            st.success(f"{bd} Blocked")
        st.write("Blocked:", st.session_state.blocked)
    with t4:
        yt = st.text_input("YouTube Link", st.session_state.social["yt"])
        ig = st.text_input("Instagram Link", st.session_state.social["ig"])
        if st.button("Save Feed"):
            st.session_state.social.update({"yt":yt, "ig":ig})
            st.success("Updated!")
