import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }</style>", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def img_to_b64(f): return base64.b64encode(f.read()).decode() if f else ""
def show_img(b): 
    if b: st.image(io.BytesIO(base64.b64decode(b)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Name")
            stat = st.radio("Status", ["Pregnant", "Non-Pregnant (PCOS)"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":name, "stat":stat, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Pass", type="password")
            if st.form_submit_button("Login") and pw == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
            if row['Name'] == "ADMIN": continue
            with st.expander(f"📋 {row['Name']} - {row['Timestamp']}"):
                st.write(f"Type: {row.get('Type','')} | Data: {row.get('Details','')}")
                if 'Attachment' in row and str(row['Attachment']) != "nan": show_img(row['Attachment'])
        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccination Guide", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "Vitals & BMI":
            st.title("📊 Health Trackers")
            with st.form("v"):
                c1, c2, c3 = st.columns(3)
                hi = c1.number_input("Height (cm)", 100, 250, 160)
                wi = c2.number_input("Weight (kg)", 30, 200, 60)
                pu = c3.number_input("Pulse (bpm)", 40, 200, 72)
                bp = st.text_input("Blood Pressure", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wi/((hi/100)**2), 1)
                    det = f"BMI:{bmi}, BP:{bp}, Pulse:{pu}"
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":det,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Recorded! BMI: {bmi}")

        elif m == "Vaccination Guide":
            st.title("💉 Vaccination Schedule")
            if "Pregnant" in st.session_state.stat:
                st.info("T-Dap: 27-36 weeks | Flu: Anytime | Tetanus: Confirmation")
            else:
                st.info("HPV Vaccine: 3 doses (0, 1, 6 months) for Cervical Cancer prevention.")

        elif m == "Diet & Yoga":
            st.title("🧘 Nutrition & Exercise")
            if "Pregnant" in st.session_state.stat:
                d1, d2, d3 = st.tabs(["1st Trimester", "2nd Trimester", "3rd Trimester"])
                with d1: 
                    st.write("**Diet:** Folic Acid focus. **Yoga:** Butterfly, Cat-Cow.")
                with d2: 
                    st.write("**Diet:** Iron & Calcium focus. **Yoga:** Palm Tree, Warrior.")
                with d3: 
                    st.write("**Diet:** High fiber, energy meals. **Yoga:** Supported Squats.")
            else:
                st.subheader("PCOS Management")
                st.write("**Diet:** Low GI, No sugar. **Yoga:** Surya Namaskar, Cobra Pose.")

        elif m == "Upload Reports":
            st.title("🧪 Upload Reports")
            with st.form("u"):
                f = st.file_uploader("Select Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Upload Now"):
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"UPLOAD","Details":n,"Attachment":img_to_b64(f),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success("Sent to Dr. Priyanka!")

        elif m == "Book Appointment":
            st.title("📅 Book Appointment")
            with st.form("b"):
                dt = st.date_input("Select Date")
                tm = st.selectbox("Slot", ["10:00 AM", "11:00 AM", "12:00 PM", "05:00 PM", "06:00 PM", "07:00 PM"])
                if st.form_submit_button("Confirm"):
                    det = f"Date:{dt} Time:{tm}"
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":det,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Booked for {dt} at {tm}")

    if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
