import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta
import re

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    .dr-header { 
        background-color: #003366; color: white; padding: 25px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
    }
    .dr-name { font-size: 30px; font-weight: bold; }
    .dr-degree { font-size: 20px; color: #ff4b6b; font-weight: bold; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: DATA PARSING ---
def extract_val(details, key):
    try:
        # Looking for "Key: Value" pattern
        match = re.search(f"{key}: ([\d.]+)", str(details))
        return float(match.group(1)) if match else None
    except: return None

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><div class='dr-name'>Dr. Priyanka Gupta</div><div class='dr-degree'>MS (Obs & Gynae)</div><div style='color:#e0e0e0;'>Obstetrician & Gynecologist | Infertility Specialist | Laparoscopic Surgeon</div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Current Status", ["Pregnant", "Non-Pregnant (PCOS/Gynae)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin", ["Appointments", "Medical Database"])
        if menu == "Appointments":
            st.dataframe(df[df['Type']=='APPOINTMENT'])
        else:
            st.dataframe(df)
    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Book Appointment", "Lab Trend Tracker", "Vitals & BMI", "Diet & Nutrition", "Baby's Growth & Scans", "Medical Library"])

        # --- LAB TRACKER (Hb, TSH, Sugar) ---
        if menu == "Lab Trend Tracker":
            st.title("🧪 Lab Reports History")
            with st.form("lab_f"):
                c1, c2, c3, c4 = st.columns(4)
                hb = c1.number_input("Hemoglobin (Hb %)", 5.0, 18.0, 11.0)
                tsh = c2.number_input("Thyroid (TSH)", 0.0, 50.0, 2.5)
                sugar = c3.number_input("Blood Sugar (mg/dL)", 50.0, 500.0, 100.0)
                urine = c4.selectbox("Urine Test", ["Normal", "Infection", "Sugar Found"])
                if st.form_submit_button("Log Current Visit Results"):
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "LAB_RESULT", "Details": f"Hb: {hb} | TSH: {tsh} | Sugar: {sugar} | Urine: {urine}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success("Results added to your history!")
                    st.rerun()

            user_labs = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'LAB_RESULT')].copy()
            if not user_labs.empty:
                user_labs['Hb'] = user_labs['Details'].apply(lambda x: extract_val(x, "Hb"))
                user_labs['TSH'] = user_labs['Details'].apply(lambda x: extract_val(x, "TSH"))
                user_labs['Sugar'] = user_labs['Details'].apply(lambda x: extract_val(x, "Sugar"))
                user_labs['Date'] = pd.to_datetime(user_labs['Timestamp'])
                st.subheader("📊 Your Lab Trends (History)")
                st.line_chart(user_labs.set_index('Date')[['Hb', 'TSH', 'Sugar']])

        # --- VITALS & BMI (Pulse & BP Fixed) ---
        elif menu == "Vitals & BMI":
            st.title("📊 Clinical Vitals")
            with st.form("v_f"):
                c1, c2, c3, c4 = st.columns(4)
                wt = c1.number_input("Weight (kg)", 30.0, 150.0, 60.0)
                ht = c2.number_input("Height (cm)", 120.0, 200.0, 160.0)
                pulse = c3.number_input("Pulse (bpm)", 40, 180, 72)
                bp = c4.text_input("BP (e.g. 120/80)")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wt / ((ht/100)**2), 2)
                    v_detail = f"BMI: {bmi} | Pulse: {pulse} | BP: {bp}"
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "VITALS", "Details": v_detail, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success(f"Vitals Saved! BMI: {bmi}")
                    st.rerun()

            user_v = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'VITALS')].copy()
            if not user_v.empty:
                user_v['BMI'] = user_v['Details'].apply(lambda x: extract_val(x, "BMI"))
                user_v['Date'] = pd.to_datetime(user_v['Timestamp'])
                st.subheader("Weight/BMI History")
                st.line_chart(user_v.set_index('Date')['BMI'])
                st.write("**Recent Records:**")
                st.table(user_v[['Timestamp', 'Details']].tail(5))

        # --- OTHER SECTIONS (DASHBOARD, BOOKING, DIET, ETC.) ---
        elif menu == "Dashboard":
            st.title(f"Welcome, {st.session_state.patient_name}")
            st.markdown(f"<div class='status-box'>Profile: <b>{st.session_state.status}</b></div>", unsafe_allow_html=True)
            if st.session_state.status == "Pregnant":
                lmp = st.date_input("Enter LMP (Last Period Date)")
                weeks = (datetime.now().date() - lmp).days // 7
                st.metric("Weeks Completed", f"{weeks} Weeks")

        elif menu == "Book Appointment":
            st.header("📅 Book 15-Min Slot")
            date = st.date_input("Select Date", min_value=datetime.now().date())
            def get_slots():
                slots = []
                for h in [11, 12, 13, 18, 19]:
                    for m in [0, 15, 30, 45]:
                        slots.append(datetime.strptime(f"{h}:{m}", "%H:%M").strftime("%I:%M %p"))
                return slots
            time = st.selectbox("Select Time Slot", get_slots())
            service = st.text_input("Reason for Visit")
            if st.button("Confirm Booking"):
                new_row = pd.DataFrame([{"Name":st.session_state.patient_name, "Type":"APPOINTMENT", "Date":str(date), "Time":time, "Details": service, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
                st.success("Booked!")
        
        elif menu == "Diet & Nutrition":
            st.title("🥗 Diet & Exercise")
            stage = st.selectbox("Choose Stage", ["1st Trimester", "2nd Trimester", "3rd Trimester", "Lactation", "PCOS"])
            plans = {"1st Trimester": ("Folic Acid, Ginger Tea, Light Meals", "Walking, Yoga"), "2nd Trimester": ("Iron, Calcium, Protein, Fruits", "Butterfly Stretch"), "3rd Trimester": ("Fiber, Flax seeds, Less Spice", "Squats, Kegels"), "Lactation": ("Methi, Saunf, Garlic, 4L Water", "Deep Breathing"), "PCOS": ("Low GI, High Protein, Ragi", "HIIT/Strength")}
            diet, exe = plans[stage]
            c1, c2 = st.columns(2)
            c1.info(f"**Diet Plan:**\n\n{diet}")
            c2.success(f"**Safe Exercise:**\n\n{exe}")

        elif menu == "Baby's Growth & Scans":
            st.title("👶 Baby's Progress")
            st.warning("**NT/NB Scan:** 11-13.6 Weeks | **TIFFA Scan:** 18-20 Weeks")
            wk = st.slider("Select Current Week", 4, 40, 12)
            if wk < 13: st.write("Organs are forming.")
            elif wk < 28: st.write("Baby can hear sounds.")
            else: st.write("Gaining weight for birth.")

        elif menu == "Medical Library":
            st.title("📚 Medical Library")
            with st.expander("Vaccines"): st.write("TT (2 doses) and HPV (Safe in Lactation)")
            with st.expander("Gynae Procedures"): st.write("IUI, Laparoscopy, Follicular Monitoring")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
