import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG & ENHANCED UI STYLING ---
st.set_page_config(page_title="Bhavya Labs Admin", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:20px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .metric-card { background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #003366; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 15px; }
    .timing-card { background:#f0f7ff; padding:10px; border-radius:10px; border-left:4px solid #003366; font-size:0.9em; }
    .type-tag { background: #003366; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; text-transform: uppercase; }
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
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.name if 'name' in st.session_state else 'Dr. Priyanka'}")
    if st.sidebar.button("Logout", key="logout_final"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        
        # --- TOP METRICS ---
        if not df.empty:
            c1, c2, c3 = st.columns(3)
            today_str = date.today().strftime("%Y-%m-%d")
            apps_today = len(df[(df['Type'] == 'APP') & (df['Details'].str.contains(today_str))])
            reports_total = len(df[df['Type'] == 'REPORT'])
            vitals_total = len(df[df['Type'] == 'VITALS'])
            
            with c1: st.markdown(f"<div class='metric-card'><h3>📅 Today's Apps</h3><h2>{apps_today}</h2></div>", unsafe_allow_html=True)
            with c2: st.markdown(f"<div class='metric-card'><h3>🧪 Reports</h3><h2>{reports_total}</h2></div>", unsafe_allow_html=True)
            with c3: st.markdown(f"<div class='metric-card'><h3>📊 Vitals Sent</h3><h2>{vitals_total}</h2></div>", unsafe_allow_html=True)

        st.write("---")
        
        t_adm = st.tabs(["📋 Patient Appointments", "🧪 Lab Reports", "📈 Vitals Tracker", "📅 Manage Schedule"])
        
        with t_adm[0]: # Appointments
            st.subheader("Upcoming Appointments")
            if not df.empty:
                apps = df[df['Type'] == 'APP'].sort_values(by='Details', ascending=False)
                for _, row in apps.iterrows():
                    st.markdown(f"""
                    <div class='patient-card'>
                        <b>👤 {row['Name']}</b><br>
                        📅 Schedule: {row['Details']}<br>
                        <span class='type-tag'>Appointment</span>
                    </div>
                    """, unsafe_allow_html=True)

        with t_adm[1]: # Reports
            st.subheader("Patient Uploaded Reports")
            reps = df[df['Type'] == 'REPORT'].sort_values(by='Timestamp', ascending=False)
            for _, row in reps.iterrows():
                with st.container():
                    st.write(f"**Patient:** {row['Name']} | **Time:** {row['Timestamp']}")
                    st.info(f"Note: {row['Details']}")
                    if str(row['Attachment']) != "nan": show_img(row['Attachment'])
                    st.write("---")

        with t_adm[2]: # Vitals
            st.subheader("Patient Vitals History")
            vits = df[df['Type'] == 'VITALS'].sort_values(by='Timestamp', ascending=False)
            st.dataframe(vits[['Timestamp', 'Name', 'Details']], use_container_width=True)

        with t_adm[3]: # Schedule Management
            st.subheader("Clinic Availability")
            c_a, c_b = st.columns(2)
            with c_a:
                block_dt = st.date_input("Select Date to Block", min_value=date.today())
                if st.button("Block Date"):
                    new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"{block_dt} Blocked!"); st.rerun()
            with c_b:
                st.write
