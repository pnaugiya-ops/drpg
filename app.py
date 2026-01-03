import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fffafa; }
    .stButton>button { border-radius: 20px; background-color: #ff4b6b; color: white; border: none; font-weight: bold; }
    .stExpander { background-color: white; border-radius: 10px; margin-bottom: 10px; box-shadow: 1px 1px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 Welcome to Bhavya Labs & Clinics")
    with st.container(border=True):
        st.markdown("**Services:** Gynae Consultation | Ultrasound | Pharmacy | Thyrocare Franchise | Laparoscopy & Infertility")
        c1, c2 = st.columns(2)
        c1.markdown("📞 **Call:** +91 9676712517")
        c2.markdown("📧 **Email:** pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Patient Name")
            status = st.radio("Current Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae/Fertility)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name = True, name
                st.session_state.status, st.session_state.role = status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title("Bhavya Clinics")
    
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Clinic Admin", ["Appointments", "Patient Database", "Post Updates"])
        df = conn.read(ttl=0)
        
        if menu == "Appointments":
            st.header("📅 Patient Appointments")
            if not df.empty and 'Type' in df.columns:
                appts = df[df['Type'] == 'APPOINTMENT'].sort_values(by='Timestamp', ascending=False)
                st.dataframe(appts[['Name', 'Status', 'Date', 'Time', 'Details']], use_container_width=True)
            else: st.info("No bookings yet.")

        elif menu == "Post Updates":
            st.header("📢 Broadcast to Patients")
            msg = st.text_input("Video/News Title")
            url = st.text_input("YouTube Link")
            if st.button("Publish"):
                new_row = pd.DataFrame([{"Name":"Dr. Admin", "Type":"BROADCAST", "Details":f"{msg}|{url}", "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
                st.success("Notification sent!")

    # --- PATIENT INTERFACE ---
    else:
        # Appointment is now available for BOTH Pregnant and Non-Pregnant
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Book Appointment", "Diet Plans", "Medical Library", "My Records"])
        df = conn.read(ttl=0)

        if menu == "Dashboard":
            st.title(f"Hello, {st.session_state.patient_name}")
            if st.session_state.status == "Pregnant":
                st.markdown("### 🤰 Pregnancy Tracker")
                # LMP/EDD Logic
            else:
                st.markdown("### 🌸 Gynae & Wellness Hub")
                st.write("Welcome to your health portal. Use the menu to book visits or view diet charts.")

        elif menu == "Book Appointment":
            st.header("📅 Schedule Your Visit")
            st.info("Available for Consultation, Ultrasound, and Thyrocare Blood Tests.")
            date = st.date_input("Date", min_value=datetime.now().date())
            is_sun = date.weekday() == 6
            slots = ["11:00 AM", "12:00 PM"] if is_sun else ["11:00 AM", "12:00 PM", "06:00 PM", "07:00 PM"]
            time = st.selectbox("Time Slot", slots)
            note = st.text_input("Reason (e.g., Follow-up, PCOS, Blood Test)")
            
            if st.button("Confirm Appointment"):
                new_appt = pd.DataFrame([{
                    "Name": st.session_state.patient_name,
                    "Status": st.session_state.status,
                    "Type": "APPOINTMENT",
                    "Date": str(date),
                    "Time": time,
                    "Details": note,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                conn.update(data=pd.concat([df, new_appt], ignore_index=True))
                st.success("Appointment Booked! Dr. Admin will see this on the schedule.")

        elif menu == "Diet Plans":
            st.title("🥗 Clinical Nutrition")
            # Trimester/Lactation/PCOS diet logic...

        elif menu == "Medical Library":
            st.title("📚 Bhavya Health Library")
            if st.session_state.status == "Pregnant":
                with st.expander("💉 Vaccinations (TT, Flu)"):
                    st.write("Mandatory Tetanus schedule details.")
            else:
                with st.expander("🔬 Infertility & IUI"):
                    st.write("Follicular monitoring and IUI procedures.")
                with st.expander("🏥 Laparoscopy"):
                    st.write("Keyhole surgery for Cysts and Fibroids.")
                with st.expander("🛡️ HPV & Pap Smear"):
                    st.write("Preventative screening for Cervical Cancer.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
