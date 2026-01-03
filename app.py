import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. INITIAL SETUP ---
st.set_page_config(page_title="GynaeCare Clinical Portal", page_icon="🏥", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Initialize Session States
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 2. LOGIN / ENTRANCE SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 GynaeCare Patient Portal")
    st.subheader("Your Digital Clinical Companion")
    
    with st.form("login_form"):
        name = st.text_input("Full Name")
        status = st.radio("Current Status", ["Pregnant", "Non-Pregnant / PCOS / General Gynae"])
        submit = st.form_submit_button("Enter Portal")
        
        if submit:
            if name:
                st.session_state.logged_in = True
                st.session_state.patient_name = name
                st.session_state.status = status
                st.rerun()
            else:
                st.error("Please enter your name to proceed.")

# --- 3. THE MAIN APP INTERIOR ---
else:
    # Sidebar Navigation
    st.sidebar.title(f"Hello, {st.session_state.patient_name}")
    st.sidebar.info(f"Mode: {st.session_state.status}")
    
    menu = st.sidebar.radio("Menu", [
        "Dashboard", 
        "Book Appointment", 
        "Diet & Nutrition", 
        "Medical Library (FAQs)", 
        "Report Vault & Vitals"
    ])
    
    # --- PAGE: DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Your Health Dashboard")
        
        if st.session_state.status == "Pregnant":
            lmp = st.date_input("Select LMP Date", value=datetime.now() - timedelta(days=30))
            edd = lmp + timedelta(days=280)
            weeks = (datetime.now().date() - lmp).days // 7
            
            col1, col2 = st.columns(2)
            col1.metric("Gestation", f"{weeks} Weeks")
            col2.metric("Due Date (EDD)", edd.strftime("%d %b %Y"))
            
            st.subheader("💉 Vaccination Schedule")
            st.write("✅ **TT (Tetanus):** 2 doses (Initial and +4 weeks)")
            st.warning("⏳ **Tdap:** Schedule between 27-36 weeks")
            st.write("✅ **Influenza:** Safe at any trimester")
            
        else:
            st.subheader("📅 Menstrual & Ovulation Tracker")
            last_p = st.date_input("Start of Last Period")
            cycle = st.slider("Average Cycle Length", 21, 45, 28)
            next_p = last_p + timedelta(days=cycle)
            ovulation = last_p + timedelta(days=cycle - 14)
            
            col1, col2 = st.columns(2)
            col1.success(f"Next Period: {next_p.strftime('%d %b')}")
            col2.info(f"Ovulation Window: {ovulation.strftime('%d %b')}")

    # --- PAGE: APPOINTMENT ---
    elif menu == "Book Appointment":
        st.title("📅 Appointment Scheduler")
        appt_date = st.date_input("Choose Date", min_value=datetime.now().date())
        is_sunday = appt_date.weekday() == 6 # 6 is Sunday
        
        if is_sunday:
            slots = ["11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM"]
            st.info("Sunday Hours: 11:00 AM - 02:00 PM")
        else:
            slots = ["11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", 
                     "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM"]
            st.info("Mon-Sat Hours: 11:00 AM-02:00 PM & 06:00 PM-08:00 PM")
            
        selected_time = st.selectbox("Select Time Slot", slots)
        if st.button("Confirm Booking"):
            st.success(f"Appointment requested for {selected_time} on {appt_date}")

    # --- PAGE: DIET ---
    elif menu == "Diet & Nutrition":
        st.title("🥗 Personalized Nutrition")
        diet_pref = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if st.session_state.status == "Pregnant":
            st.write("### Pregnancy Meal Plan")
            st.markdown("- **Breakfast:** Oats with milk/nuts or Egg omelet.")
            st.markdown("- **Lunch:** Dal/Chicken with brown rice & curd.")
            st.markdown("- **Evening:** Fruit bowl or handful of almonds.")
        else:
            st.write("### PCOS/Hormone Balance Diet")
            st.markdown("Focus: Low GI foods to control Insulin.")
            st.markdown("- **Morning:** Methi water (fenugreek) + Walnuts.")
            st.markdown("- **Lunch:** Ragi/Jowar Roti with green vegetables.")
            st.markdown("- **Avoid:** White sugar, maida, and processed snacks.")

    # --- PAGE: FAQs ---
    elif menu == "Medical Library (FAQs)":
        st.title("❓ Knowledge Center")
        with st.expander("💉 HPV Vaccination"):
            st.write("Prevents Cervical Cancer. Recommended for all women aged 9-45.")
        with st.expander("⚪ White Discharge / Itching"):
            st.write("Normal if clear. Seek help if curd-like, yellow, or foul-smelling.")
        with st.expander("🩸 Painful Periods (Dysmenorrhea)"):
            st.write("Use heat packs. If pain is severe enough to miss work, consult the Dr.")

    # --- PAGE: REPORTS & VITALS ---
    elif menu == "Report Vault & Vitals":
        st.title("📂 Clinical Records")
        bp = st.text_input("Blood Pressure")
        wt = st.number_input("Weight (kg)", 0.0)
        file = st.file_uploader("Upload Lab Report (PDF/Image)")
        
        if st.button("Save to Clinic"):
            try:
                # READ EXISTING DATA
                df = conn.read(ttl=0)
                # CREATE NEW ROW
                new_row = pd.DataFrame([{
                    "Name": st.session_state.patient_name,
                    "Status": st.session_state.status,
                    "BP": bp, "Weight": wt,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                # UPDATE
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Data synced with clinical records!")
            except:
                st.error("Connection error. Try again.")

    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
