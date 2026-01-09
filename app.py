import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIG & CONNECTION ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_sheets(p_name, category, detail_text):
    """Helper function to save any data to your Google Sheet"""
    try:
        existing_df = conn.read(worksheet="Appointments", ttl=0)
        new_row = pd.DataFrame([{
            "Name": p_name,
            "Type": category,
            "Details": detail_text,
            "Attachment": "N/A",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        conn.update(worksheet="Appointments", data=updated_df)
        return True
    except:
        return False

# --- 2. UI STYLING ---
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border-left:6px solid #ff4b6b; margin-bottom:15px; color: #333; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States for login only
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h2>Dr. Priyanka Gupta</h2><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Access", "Admin Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Patient Full Name")
            age = st.number_input("Age", 18, 100, 25)
            s = st.radio("Clinical Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter My Dashboard"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":age,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Admin Password", type="password")
            if st.form_submit_button("Login to Clinic Master"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D"})
                    st.rerun()

# --- 4. PATIENT PORTAL ---
elif st.session_state.role == "P":
    st.markdown(f"### 📋 Patient: {st.session_state.name} | Status: {st.session_state.stat}")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    m = st.segmented_control("SELECT VIEW", options=["Health Tracker", "Diet Plans", "Exercise", "Lab Reports", "Vitals", "Book Slot"], default="Health Tracker")
    st.divider()

    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ EDD: {edd} | Current Week: {wks}")
        elif st.session_state.stat == "Lactating Mother":
            st.info("### Postpartum Care & Contraception")
            st.write("Options: Mini-pills, Copper T, DMPA Injection, Barrier Methods.")
        else:
            st.info("PCOS Progress Tracking Active.")

    elif m == "Diet Plans":
        st.header(f"🥗 Diet Chart: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["T1", "T2", "T3"])
            with t1: st.markdown("<div class='diet-card'><b>Focus: Folic Acid.</b> Almonds, Poha, Dal Chilla.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>Focus: Iron & Calcium.</b> Coconut water, Spinach, Paneer.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>Focus: Energy.</b> 6 small meals, Bedtime Milk + Dates.</div>", unsafe_allow_html=True)
        elif st.session_state.stat == "PCOS/Gynae":
            st.markdown("<div class='diet-card'><b>PCOS:</b> Avoid Sugar/Maida. High Protein (50g+). Jowar/Bajra rotis.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='diet-card'><b>Lactation:</b> Methi, Jeera-water, Shatavari, 4L Fluids.</div>", unsafe_allow_html=True)

    elif m == "Exercise":
        st.write("1. Butterfly Pose | 2. Cat-Cow Stretch | 3. 30-min Walking")

    elif m == "Lab Reports":
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar", 50, 400, 90)
            tsh = st.number_input("TSH", 0.0, 50.0, 2.5)
            urine = st.selectbox("Urine Test", ["Normal", "Trace", "+1", "+2"])
            if st.form_submit_button("Save to Clinic Records"):
                details = f"Hb: {hb}, Sugar: {sugar}, TSH: {tsh}, Urine: {urine}"
                if save_to_sheets(st.session_state.name, "Lab Report", details):
                    st.success("Sent to Doctor!")

    elif m == "Vitals":
        with st.form("vital_form"):
            p, bp = st.number_input("Pulse", 40, 150, 72), st.text_input("BP", "120/80")
            wt, ht = st.number_input("Weight (kg)", 30.0, 150.0, 60.0), st.number_input("Height (cm)", 100.0, 220.0, 160.0)
            if st.form_submit_button("Update Vitals"):
                bmi = round(wt / ((ht/100)**2), 2)
                details = f"Pulse: {p}, BP: {bp}, Wt: {wt}, BMI: {bmi}"
                if save_to_sheets(st.session_state.name, "Vitals", details):
                    st.success("Vitals Updated!")

    elif m == "Book Slot":
        d = st.date_input("Date", min_value=date.today())
        t = st.selectbox("Slot", ["11:15 AM", "12:00 PM", "06:00 PM", "07:30 PM"])
        if st.button("Request Booking"):
            if save_to_sheets(st.session_state.name, "Appointment", f"Date: {d}, Time: {t}"):
                st.success("Booking Sent!")

# --- 5. ADMIN PORTAL ---
elif st.session_state.role == "D":
    st.title("👩‍⚕️ Admin Master (Bhavya Labs)")
    if st.button("Refresh Data"): st.rerun()

    # Pull everything from Google Sheets
    df = conn.read(worksheet="Appointments", ttl=0)
    
    t1, t2 = st.tabs(["Appointments", "Patient Health Records"])
    with t1:
        st.dataframe(df[df['Type'] == "Appointment"])
    with t2:
