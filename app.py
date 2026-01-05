import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG & PERMANENT STYLING ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:20px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .timing-card { background:#f0f7ff; padding:15px; border-radius:10px; border-left:5px solid #003366; font-size:0.9em; margin-bottom:10px; }
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def process_img(f):
    if not f: return ""
    try:
        img = Image.open(f)
        img.thumbnail((500, 500))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=40)
        return base64.b64encode(buf.getvalue()).decode()
    except: return ""

def show_img(b):
    if b: st.image(io.BytesIO(base64.b64decode(b)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            age = st.number_input("Age", 1, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                st.session_state.update({"logged_in":True, "name":n, "age":age, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.form_submit_button("Login") and st.text_input("Pass", type="password") == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    # --- GLOBAL SIDEBAR (Always Visible) ---
    st.sidebar.markdown(f"### Welcome, {st.session_state.get('name', 'Doctor')}")
    st.sidebar.markdown("### 🕒 Clinic Timings")
    st.sidebar.markdown("""
    <div class='timing-card'>
    <b>Mon-Sat:</b> 11:00 AM - 2:00 PM & 6:00 PM - 8:00 PM<br>
    <b>Sun:</b> 11:00 AM - 2:00 PM
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("Logout", key="logout_global"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    # --- DOCTOR VIEW ---
    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals Tracker", "📅 Manage Schedule"])
        
        with t_adm[0]:
            if not df.empty:
                apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().contains(search))]
                for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                    st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)
        
        with t_adm[1]:
            reps = df[(df['Type'] == 'REPORT') & (df['Name'].str.lower().contains(search))] if not df.empty else pd.DataFrame()
            for _, row in reps.iterrows():
                with st.expander(f"Report: {row['Name']} - {row['Timestamp']}"):
                    st.write(f"Note: {row['Details']}")
                    show_img(row['Attachment'])

        with t_adm[2]:
            st.dataframe(df[df['Type'] == 'VITALS'], use_container_width=True)

        with t_adm[3]:
            st.subheader("Manage Availability")
            block_dt = st.date_input("Block Date", min_value=date.today())
            if st.button("Confirm Block"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()

    # --- PATIENT VIEW ---
    else:
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccines & Screening", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        # 1. VITALS
        if m == "Vitals & BMI":
            st.header("📊 Health Tracker")
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160)
                wi = st.number_input("Weight (kg)", 30, 200, 60)
                pu = st.number_input("Pulse (bpm)", 40, 200, 72)
                bp = st.text_input("Blood Pressure", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"VITALS","Details":f"BMI: {bmi}, BP: {bp}, Pulse: {pu}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"BMI Saved: {bmi}")

        # 2. VACCINES (HPV & PAP SMEAR RESTORED)
        elif m == "Vaccines & Screening":
            st.header("💉 Vaccination & Screening")
            if "PCOS" in st.session_state.stat:
