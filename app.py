import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; width:100%; } .card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; }</style>", unsafe_allow_html=True)

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
            name = st.text_input("Name")
            stat = st.radio("Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":name, "stat":stat, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
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
                col1, col2 = st.columns(2)
                h = col1.number_input("Height (cm)", 100, 250, 160)
                w = col2.number_input("Weight (kg)", 30, 200, 60)
                bp = st.text_input("Blood Pressure (e.g. 120/80)")
                if st.form_submit_button("Save & Calculate BMI"):
                    bmi = round(w / ((h/100)**2), 1)
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"VITALS", "Details":f"BMI: {bmi}, BP: {bp}, Wt: {w}kg", "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"BMI: {bmi}")

        elif m == "Vaccination Guide":
            st.title("💉 Vaccinations")
            if "Pregnant" in st.session_state.stat:
                st.write("**Tetanus:** At confirmation | **T-Dap:** 27-36 weeks | **Flu:** Anytime")
            else:
                st.write("**HPV:** 3 doses at 0, 1, 6 months for Cervical Cancer prevention.")

        elif m == "Diet & Yoga":
            st.title("🧘 Wellness Guide")
            if "Pregnant" in st.session_state.stat:
                st.subheader("Pregnancy Care")
                st.write("**Diet:** High protein, iron, and folic acid. 3L water daily.")
                st.write("**Yoga:** Butterfly pose, Cat-Cow stretch, and Deep breathing (Pranayama).")
            else:
                st.subheader("PCOS Management")
                st.write("**Diet:** Low Glycemic Index (GI) foods, avoid processed sugar/dairy.")
                st.write("**Yoga:** Surya Namaskar, Cobra pose (Bhujangasana), and Malasana.")

        elif m == "Upload Reports":
            st.title("🧪 Upload")
            with st.form("u"):
                f = st.file_uploader("Image", type=['jpg', 'png', 'jpeg'])
                note = st.text_input("Note")
                if st.form_submit_button("Upload"):
                    b64 = img_to_b64(f)
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"UPLOAD", "Details":note, "Attachment":b64, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")

        elif m == "Book Appointment":
            dt = st.date_input("Date", min_value=datetime.now().date())
            if st.button("Confirm"):
                new = pd.DataFrame([{"Name":st.session_state.name, "Type":"APP", "Details":str(dt), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
