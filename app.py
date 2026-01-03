import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import re

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { 
        border-radius: 12px; background-color: #ff4b6b; color: white; 
        font-weight: bold; border: none; height: 3em; width: 100%;
    }
    .status-box { 
        padding: 15px; border-radius: 10px; background-color: #e6f0ff; 
        border-left: 6px solid #003366; color: #003366; margin-bottom: 20px;
    }
    .stExpander { background-color: white; border: 1px solid #e0e0e0; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: DATA PARSING ---
def extract_val(details, key):
    try:
        match = re.search(f"{key}: ([\d.]+)", str(details))
        return float(match.group(1)) if match else None
    except: return None

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 Bhavya Labs & Clinics")
    st.markdown("<div class='status-box'><b>Services:</b> Gynae Consultation | Ultrasound | Pharmacy | Thyrocare Franchise | Laparoscopy & Infertility</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.info("📞 Contact: 9676712517")
    col2.info("📧 Email: pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Are you currently pregnant?", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter My Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Enter Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title("Bhavya Clinics")
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin Menu", ["Appointments", "Medical Database", "Post Updates"])
        if menu == "Appointments":
            st.header("📅 Patient Schedule")
            st.dataframe(df[df['Type']=='APPOINTMENT'].sort_values(by='Timestamp', ascending=False))
        elif menu == "Medical Database":
            st.header("📋 All Patient Records")
            st.dataframe(df)

    else:
        menu = st.sidebar.radio("Navigation", ["Home Dashboard", "Book Appointment", "Lab Tracker", "Vitals & BMI", "Diet & Nutrition", "Medical Library"])

        # --- HOME DASHBOARD ---
        if menu == "Home Dashboard":
            st.title(f"Welcome, {st.session_state.patient_name}")
            st.markdown(f"<div class='status-box'>Profile: <b>{st.session_state.status}</b></div>", unsafe_allow_html=True)
            # Latest Broadcast News
            if not df.empty:
                news = df[df['Type'] == 'BROADCAST'].tail(1)
                if not news.empty:
                    st.warning(f"📣 **Latest Update:** {news['Details'].values[0]}")

        # --- BOOK APPOINTMENT ---
        elif menu == "Book Appointment":
            st.header("📅 Schedule a Visit")
            st.info("Available for Consultation, Ultrasound, and Thyrocare Blood Tests.")
            date = st.date_input("Select Date", min_value=datetime.now().date())
            is_sun = date.weekday() == 6
            slots = ["11:00 AM", "12:00 PM"] if is_sun else ["11:00 AM", "12:00 PM", "06:00 PM", "07:00 PM"]
            time = st.selectbox("Slot", slots)
            note = st.text_input("Reason for visit (e.g., Routine Checkup, Blood Test)")
            if st.button("Confirm Appointment"):
                new_row = pd.DataFrame([{"Name":st.session_state.patient_name, "Type":"APPOINTMENT", "Status":st.session_state.status, "Date":str(date), "Time":time, "Details":note, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
                st.success("Booked Successfully!")

        # --- LAB TRACKER ---
        elif menu == "Lab Tracker":
            st.title("🧪 Lab Trend Monitoring")
            with st.form("lab_f"):
                c1, c2, c3 = st.columns(3)
                hb = c1.number_input("Hb %", 5.0, 20.0, 12.0)
                tsh = c2.number_input("TSH", 0.0, 50.0, 2.5)
                urine = c3.selectbox("Urine Test", ["Normal", "Infection", "Sugar"])
                if st.form_submit_button("Save Labs"):
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "LAB_RESULT", "Details": f"Hb: {hb} | TSH: {tsh} | Urine: {urine}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success("Results Saved!")
                    st.rerun()

            user_labs = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'LAB_RESULT')].copy()
            if not user_labs.empty:
                user_labs['Hb'] = user_labs['Details'].apply(lambda x: extract_val(x, "Hb"))
                user_labs['TSH'] = user_labs['Details'].apply(lambda x: extract_val(x, "TSH"))
                user_labs['Date'] = pd.to_datetime(user_labs['Timestamp'])
                st.subheader("Hb & TSH Trends")
                st.line_chart(user_labs.set_index('Date')[['Hb', 'TSH']])

        # --- VITALS & BMI ---
        elif menu == "Vitals & BMI":
            st.title("📊 Physical Vitals")
            with st.form("v_f"):
                c1, c2, c3, c4 = st.columns(4)
                wt = c1.number_input("Weight (kg)", 30.0, 150.0, 60.0)
                ht = c2.number_input("Height (cm)", 100.0, 220.0, 160.0)
                pulse = c3.number_input("Pulse", 40, 180, 72)
                bp = c4.text_input("BP", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wt / ((ht/100)**2), 2)
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "VITALS", "Details": f"BMI: {bmi} | Pulse: {pulse} | BP: {bp}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success(f"BMI Calculated: {bmi}")
                    st.rerun()

            user_v = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'VITALS')].copy()
            if not user_v.empty:
                user_v['BMI'] = user_v['Details'].apply(lambda x: extract_val(x, "BMI"))
                user_v['Date'] = pd.to_datetime(user_v['Timestamp'])
                st.subheader("BMI Trend")
                st.line_chart(user_v.set_index('Date')['BMI'])

        # --- DIET & NUTRITION ---
        elif menu == "Diet & Nutrition":
            st.title("🥗 Clinical Nutrition Plans")
            diet_pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
            
            if st.session_state.status == "Pregnant":
                stage = st.selectbox("Select Stage", ["1st Trimester", "2nd Trimester", "3rd Trimester", "Lactation"])
                if stage == "1st Trimester":
                    st.subheader("🍎 1st Trimester (1800-2000 kcal)")
                    st.write("**Focus:** Folic Acid. Managing Nausea with small meals. Avoid raw papaya/pineapple.")
                elif stage == "2nd Trimester":
                    st.subheader("🥩 2nd Trimester (2200-2400 kcal)")
                    st.write("**Focus:** Iron & Calcium for fetal bone growth. Increase protein intake.")
                elif stage == "3rd Trimester":
                    st.subheader("🥛 3rd Trimester (2400-2600 kcal)")
                    st.write("**Focus:** Energy & Fiber. Prevent acidity & constipation. Rich in Omega-3.")
                elif stage == "Lactation":
                    st.subheader("🤱 Lactation Diet (2600-2800 kcal)")
                    st.write("**Galactagogues:** Fenugreek (Methi), Saunf, Oats, Garlic. Stay hydrated (3L water).")
            else:
                st.subheader("🩸 PCOS & Weight Management")
                st.write("Focus: Low Glycemic Index (GI) and High Fiber. Use Ragi/Jowar instead of White Rice.")

        # --- MEDICAL LIBRARY ---
        elif menu == "Medical Library":
            st.title("📚 Bhavya Health Library")
            if st.session_state.status == "Pregnant":
                with st.expander("💉 Pregnancy Vaccinations"):
                    st.write("**Tetanus (TT/Td):** Mandatory 2 doses. **Influenza:** Safe in all trimesters.")
                with st.expander("💉 Post-Delivery / Lactation"):
                    st.write("**HPV Vaccine:** Safe to take while breastfeeding. Protects against cervical cancer.")
                with st.expander("🧘 Yoga & Exercise"):
                    st.write("Safe Poses: Butterfly stretch, Cat-cow. Avoid lying flat on back.")
            else:
                with st.expander("🔬 Infertility & IUI"):
                    st.write("Follicular monitoring, Serial Ultrasounds, and IUI processing.")
                with st.expander("🏥 Laparoscopy"):
                    st.write("Keyhole surgery for Ovarian Cysts, Fibroids, and Tubal patency checks.")
                with st.expander("🛡️ Preventive Care"):
                    st.write("Pap Smear and HPV Vaccination for Cervical Cancer prevention.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
