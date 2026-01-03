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
    .ai-box { background:#f0f7ff; padding:20px; border-radius:15px; border-left:5px solid #003366; margin-bottom:20px; }
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
        m = st.sidebar.radio("Menu", ["AI Assistant", "Vitals & BMI", "Vaccination Guide", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "AI Assistant":
            st.title("🤖 Clinical AI Assistant")
            st.markdown("<div class='ai-box'>Welcome! I can help explain your reports or clinical terms. Note: For emergencies or specific medical advice, please consult Dr. Priyanka.</div>", unsafe_allow_html=True)
            query = st.text_input("How can I assist you today?")
            if query:
                st.info(f"Regarding '{query}': Generally, maintaining a balanced diet and regular vitals tracking is key. Dr. Priyanka can provide a detailed review during your next visit.")

        elif m == "Vitals & BMI":
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
                    st.success(f"Recorded! Your BMI is {bmi}")

        elif m == "Vaccination Guide":
            st.title("💉 Vaccination Schedule")
            if "Pregnant" in st.session_state.stat:
                st.markdown("<div class='vax-card'><b>Tetanus (TT1):</b> At confirmation.<br><b>T-Dap:</b> 27-36 weeks.<br><b>Influenza:</b> Anytime during pregnancy.</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("<div class='vax-card'><b>HPV Vaccine:</b> 3 doses (0, 1, 6 months) for Cervical Cancer prevention.</div>", unsafe_allow_html=True)
                

        elif m == "Diet & Yoga":
            st.title("🧘 Nutrition & Exercise")
            if "Pregnant" in st.session_state.stat:
                d1, d2, d3 = st.tabs(["1st Trimester", "2nd Trimester", "3rd Trimester"])
                with d1: 
                    st.write("**Diet:** Folic Acid rich foods. **Yoga:** Butterfly, Cat-Cow."); 
                with d2: 
                    st.write("**Diet:** Iron & Calcium focus. **Yoga:** Palm Tree, Warrior."); 

[Image of 2nd trimester pregnancy diet chart]

                with d3: 
                    st.write("**Diet:** Small frequent meals. **Yoga:** Squats with support."); 
            else:
                st.subheader("PCOS Management")
                st.write("**Diet:** Low GI, High Fiber. **Yoga:** Surya Namaskar, Bow Pose."); 

        elif m == "Upload Reports":
            st.title("🧪 Upload Reports")
            with st.form("u_form"):
                f = st.file_uploader("Select Image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
                note = st.text_input("Note for Doctor")
                if st.form_submit_button("Upload Now"):
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"UPLOAD", "Details":note, "Attachment":img_to_b64(f), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success("Report successfully sent!")

        elif m == "Book Appointment":
            st.title("📅 Book Appointment")
            with st.form("app_form"):
                dt = st.date_input("Select Date", min_value=datetime.now().date())
                tm = st.selectbox("Available Time Slot", ["10:00 AM", "11:00 AM", "12:00 PM", "05:00 PM", "06:00 PM", "07:00 PM"])
                if st.form_submit_button("Confirm Booking"):
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"APP", "Details":f"Date: {dt} Time: {tm}", "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Confirmed for {dt} at {tm}")

    if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
