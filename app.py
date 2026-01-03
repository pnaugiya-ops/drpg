import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP ---
st.set_page_config(page_title="GynaeCare Hub", page_icon="🏥", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Change this to your preferred secret password
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = "Patient"

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 GynaeCare Digital Clinic")
    tab1, tab2 = st.tabs(["Patient Portal", "Doctor Login"])
    
    with tab1:
        with st.form("patient_login"):
            name = st.text_input("Full Name")
            status = st.radio("Status", ["Pregnant", "Non-Pregnant / PCOS"])
            if st.form_submit_button("Enter Portal"):
                if name:
                    st.session_state.logged_in, st.session_state.patient_name = True, name
                    st.session_state.status, st.session_state.role = status, "Patient"
                    st.rerun()

    with tab2:
        with st.form("dr_login"):
            pw = st.text_input("Enter Clinic Password", type="password")
            if st.form_submit_button("Login as Doctor"):
                if pw == DR_PASSWORD:
                    st.session_state.logged_in, st.session_state.role = True, "Doctor"
                    st.session_state.patient_name = "Dr. Admin"
                    st.rerun()
                else:
                    st.error("Incorrect Password")

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title(f"Logged in: {st.session_state.patient_name}")
    
    # --- DOCTOR ADMIN VIEW ---
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Clinic Management", ["Appointments", "Patient Database", "Post Video/Updates"])
        
        df = conn.read(ttl=0)

        if menu == "Appointments":
            st.header("📅 Today's Appointments")
            if not df.empty and 'Type' in df.columns:
                appts = df[df['Type'] == 'APPOINTMENT']
                st.table(appts[['Name', 'Date', 'Time', 'Details']])
            else:
                st.info("No appointments booked yet.")

        elif menu == "Patient Database":
            st.header("📋 All Patient Medical Logs")
            st.dataframe(df, use_container_width=True)

        elif menu == "Post Video/Updates":
            st.header("📢 Broadcast to Patients")
            new_msg = st.text_input("Announcement Title")
            video_url = st.text_input("YouTube/Instagram Link")
            if st.button("Publish Update"):
                new_row = pd.DataFrame([{"Name": "Dr. Admin", "Role": "Doctor", "Type": "BROADCAST", "Details": f"{new_msg}|{video_url}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
                st.success("Notification published!")

    # --- PATIENT VIEW ---
    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Book Appointment", "Diet & Advice", "Medical Feed", "Log Records"])
        df = conn.read(ttl=0)

        # Show Latest Doctor Announcement at the top
        if not df.empty and 'Type' in df.columns:
            latest_news = df[df['Type'] == 'BROADCAST'].tail(1)
            if not latest_news.empty:
                st.warning(f"🔔 **News from Dr:** {latest_news['Details'].values[0]}")

        if menu == "Dashboard":
            st.title("📊 My Health Dashboard")
            if st.session_state.status == "Pregnant":
                lmp = st.date_input("LMP Date")
                edd = lmp + timedelta(days=280)
                st.metric("Weeks Completed", f"{(datetime.now().date() - lmp).days // 7} Weeks")
                st.info(f"📅 EDD: {edd.strftime('%d %B %Y')}")
            else:
                st.subheader("Period Tracker")
                last_p = st.date_input("Last Period Start")
                st.success(f"Next Period Expected: {(last_p + timedelta(days=28)).strftime('%d %b')}")

        elif menu == "Book Appointment":
            st.header("📅 Fix Appointment")
            date = st.date_input("Select Date", min_value=datetime.now().date())
            is_sun = date.weekday() == 6
            slots = ["11:00 AM", "12:00 PM", "01:00 PM"] if is_sun else ["11:00 AM", "12:00 PM", "06:00 PM", "07:00 PM"]
            time = st.selectbox("Time Slot", slots)
            if st.button("Confirm"):
                new_appt = pd.DataFrame([{"Name": st.session_state.patient_name, "Role": "Patient", "Type": "APPOINTMENT", "Date": str(date), "Time": time, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_appt], ignore_index=True))
                st.success("Booked!")

        elif menu == "Diet & Advice":
            st.header("🍏 Nutrition Guide")
            if st.session_state.status == "Pregnant":
                st.write("Focus on Protein, Iron, and Folic Acid.")
            else:
                st.write("PCOS Focus: Low GI Foods, No Sugar.")

        elif menu == "Medical Feed":
            st.header("🎥 Education Videos")
            if not df.empty:
                videos = df[df['Type'] == 'BROADCAST']
                for v in videos['Details']:
                    if "|" in v:
                        title, url = v.split("|")
                        st.subheader(title)
                        st.video(url)

        elif menu == "Log Records":
            st.header("📝 Save Vitals")
            bp = st.text_input("BP")
            wt = st.number_input("Weight", 0.0)
            if st.button("Save"):
                log = pd.DataFrame([{"Name": st.session_state.patient_name, "Role": "Patient", "Type": "VITALS", "BP": bp, "Weight": wt, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, log], ignore_index=True))
                st.success("Saved!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
