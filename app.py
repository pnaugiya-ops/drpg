import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .vax-card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def img_to_b64(file): 
    return base64.b64encode(file.read()).decode() if file else ""

def show_img(b64): 
    if b64: st.image(io.BytesIO(base64.b64decode(b64)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            stat = st.radio("Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter Portal"):
                st.session_state.update({"logged_in":True, "name":name, "stat":stat, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        t_adm = st.tabs(["Patient Submissions", "Appointment Schedule"])
        with t_adm[0]:
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    if row['Name'] == "ADMIN": continue
                    with st.expander(f"📋 {row['Timestamp']} - {row['Name']}"):
                        st.write(f"**Category:** {row.get('Type','')}")
                        st.write(f"**Details:** {row.get('Details', '')}")
                        if 'Attachment' in row and str(row['Attachment']) not in ["nan", ""]: show_img(row['Attachment'])
        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
    else:
        st.sidebar.title(f"Hello, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccination Guide", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "Vitals & BMI":
            st.title("📊 Health Trackers")
            with st.form("v_form"):
                c1, c2, c3 = st.columns(3)
                h = c1.number_input("Height (cm)", 100, 250, 160)
                w = c2.number_input("Weight (kg)", 30, 200, 60)
                p = c3.number_input("Pulse (bpm)", 40, 200, 72)
                bp = st.text_input("Blood Pressure", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(w / ((h/100)**2), 1)
                    det = f"BMI: {bmi} | BP: {bp} | Pulse: {p} | Wt: {w}kg"
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"VITALS", "Details":det, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f
