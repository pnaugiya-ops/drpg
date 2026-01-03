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
        background-color: #003366; color: white; padding: 30px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
        border-bottom: 5px solid #ff4b6b;
    }
    .clinic-name { font-size: 36px; font-weight: bold; letter-spacing: 1px; }
    .dr-name { font-size: 28px; font-weight: bold; margin-top: 10px; }
    .dr-degree { font-size: 20px; color: #ff4b6b; font-weight: bold; }
    .dr-spec { font-size: 16px; color: #ced4da; font-style: italic; }
    h1, h2, h3 { color: #003366; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; }
    .chat-bubble { padding: 12px; border-radius: 15px; margin-bottom: 10px; background-color: #f0f2f6; border: 1px solid #ddd; }
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

# --- AI ASSISTANT LOGIC ---
def get_ai_response(query):
    query = query.lower()
    if "pain" in query: return "Mild cramping can be normal after a biopsy or D&C. However, severe pain or fever requires an immediate visit."
    elif "sugar" in query or "fasting" in query: return "For fasting blood sugar, do not eat for 8-10 hours. Water is allowed."
    elif "diet" in query: return "Focus on high protein, low sugar, and 3-4 liters of water. Avoid oily food."
    return "Please book a 15-minute slot so Dr. Priyanka can review your case in detail."

# --- 2. LOGIN SCREEN (BRANDED HEADER) ---
if not st.session_state.logged_in:
    st.markdown("""
        <div class='dr-header'>
            <div class='clinic-name'>BHAVYA LABS & CLINICS</div>
            <div class='dr-name'>Dr. Priyanka Gupta</div>
            <div class='dr-degree'>MS (Obstetrics & Gynaecology)</div>
            <div class='dr-spec'>Infertility Specialist & Laparoscopic Surgeon</div>
        </div>
    """, unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            status = st.radio("Profile Type", ["Pregnant", "Non-Pregnant (PCOS/Infertility/Gynae)"])
            if st.form_submit_button("Enter My Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. CLINIC INTERFACE ---
else:
    df = conn.read(ttl=0)

    if st.session_state.role == "Doctor":
        st.title("👨‍⚕️ Admin: Bhavya Labs & Clinics")
        
        adm_menu = st.tabs(["Patient Data", "Manage Schedule"])
        
        with adm_menu[0]:
            st.subheader("All Patient Records")
            st.dataframe(df.sort_values(by='Timestamp', ascending=False))
            
        with adm_menu[1]:
            st.subheader("Block Dates (Vacation/Emergency)")
            block_date = st.date_input("Select Date to Block", min_value=datetime.now().date())
            block_reason = st.text_input("Reason (Optional)", "Doctor Unavailable")
            if st.button("Block This Date"):
                new_row = pd.DataFrame([{"Name": "ADMIN", "Type": "BLOCKED_DATE", "Date": str(block_date), "Details": block_reason, "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new_row], ignore_index=True))
                st.success(f"Date {block_date} is now blocked for appointments.")
                st.rerun()
            
            st.write("**Currently Blocked Dates:**")
            blocked_list = df[df['Type'] == 'BLOCKED_DATE']
            st.table(blocked_list[['Date', 'Details']])

    else:
        st.sidebar.markdown(f"**BHAVYA CLINICS**\n\nDr. Priyanka Gupta\nMS (Obs & Gynae)")
        menu = st.sidebar.radio("Navigation", ["Dashboard", "AI Assistant", "Lab Trend Tracker", "Follicular Monitoring", "Vitals & BMI", "Medical Library", "Book Appointment"])

        # --- APPOINTMENT (WITH BLOCK CHECK) ---
        if menu == "Book Appointment":
            st.header("📅 Book 15-Min Slot")
            dt = st.date_input("Select Date", min_value=datetime.now().date())
            
            # Check if date is blocked
            blocked_dates = df[df['Type'] == 'BLOCKED_DATE']['Date'].values
            if str(dt) in blocked_dates:
                st.error("⚠️ Dr. Priyanka Gupta is not available on this date due to clinical commitments or emergency. Please select another date.")
            else:
                def slots():
                    s = []
                    for h in [11, 12, 13, 18, 19]:
                        for m in [0, 15, 30, 45]:
                            s.append(datetime.strptime(f"{h}:{m}", "%H:%M").strftime("%I:%M %p"))
                    return s
                tm = st.selectbox("Available Time", slots())
                reason = st.text_input("Reason for Visit")
                if st.button("Confirm Appointment"):
                    new_row = pd.DataFrame([{"Name":st.session_state.patient_name, "Type":"APPOINTMENT", "Date":str(dt), "Time":tm, "Details": reason, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.success("Your appointment is confirmed!")

        # --- (REST OF THE NAVIGATION CODE CONTINUES HERE - AI, LABS, ETC.) ---
        elif menu == "AI Assistant":
            st.title("🤖 AI FAQ Assistant")
            user_q = st.text_input("Ask about symptoms, diet, or procedures:")
            if user_q:
                ans = get_ai_response(user_q)
                st.markdown(f"<div class='chat-bubble'><b>You:</b> {user_q}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='chat-bubble' style='background-color:#e6f0ff;'><b>AI:</b> {ans}</div>", unsafe_allow_html=True)

        elif menu == "Lab Trend Tracker":
            st.title("🧪 Lab History")
            with st.form("lab_f"):
                c1, c2, c3 = st.columns(3)
                hb = c1.number_input("Hb %", 5.0, 18.0, 11.0)
                tsh = c2.number_input("TSH", 0.0, 50.0, 2.5)
                sugar = c3.number_input("Blood Sugar", 50.0, 500.0, 100.0)
                if st.form_submit_button("Save Lab Data"):
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "LAB", "Details": f"Hb: {hb} | TSH: {tsh} | Sugar: {sugar}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.rerun()
            
            user_data = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'LAB')].copy()
            if not user_data.empty:
                user_data['Hb'] = user_data['Details'].apply(lambda x: extract_val(x, "Hb"))
                user_data['TSH'] = user_data['Details'].apply(lambda x: extract_val(x, "TSH"))
                user_data['Sugar'] = user_data['Details'].apply(lambda x: extract_val(x, "Sugar"))
                user_data['Date'] = pd.to_datetime(user_data['Timestamp'])
                st.line_chart(user_data.set_index('Date')[['Hb', 'TSH', 'Sugar']])

        elif menu == "Follicular Monitoring":
            st.title("🥚 Follicular Study Tracker")
            with st.form("fol_f"):
                c1, c2, c3 = st.columns(3)
                day = c1.number_input("Cycle Day", 1, 30, 9)
                rt = c2.number_input("Right Ovary (mm)", 0.0, 30.0, 10.0)
                lt = c3.number_input("Left Ovary (mm)", 0.0, 30.0, 10.0)
                if st.form_submit_button("Record Scan"):
                    new_row = pd.DataFrame([{"Name": st.session_state.patient_name, "Type": "FOL", "Details": f"Day: {day} | Right: {rt} | Left: {lt}", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new_row], ignore_index=True))
                    st.rerun()
            fol_data = df[(df['Name'] == st.session_state.patient_name) & (df['Type'] == 'FOL')].copy()
            if not fol_data.empty:
                st.dataframe(fol_data[['Timestamp', 'Details']])

        elif menu == "Medical Library":
            st.title("📚 Bhavya Procedure Guide")
            with st.expander("🔬 Diagnostics"):
                st.write("**Pap Smear:** Cervical cancer screening.")
                st.write("**Endometrial Biopsy:** Checking uterine lining.")
            with st.expander("🏥 Surgery"):
                st.write("**D&C & MTP:** Safe pregnancy management.")
                st.write("**Laparoscopy:** Keyhole surgery for infertility/cysts.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
