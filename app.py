import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIG & CONNECTION ---
st.set_page_config(page_title="GynaeCare Clinical Portal", page_icon="🤰")
conn = st.connection("gsheets", type=GSheetsConnection)

# Initialize Session (The "App Memory")
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 2. ENTRANCE SCREEN (The Form) ---
if not st.session_state.logged_in:
    st.title("🏥 GynaeCare Patient Portal")
    st.write("Please enter your details to access your clinical dashboard.")
    
    with st.container(border=True):
        name = st.text_input("Patient Full Name")
        lmp_date = st.date_input("Last Menstrual Period (LMP)", value=datetime.now() - timedelta(days=30))
        
        if st.button("Access Dashboard"):
            if name:
                st.session_state.logged_in = True
                st.session_state.patient_name = name
                st.session_state.lmp = lmp_date
                st.rerun()
            else:
                st.error("Name is required.")

# --- 3. THE APP INTERIOR (The Assembly) ---
else:
    # --- Sidebar Setup ---
    st.sidebar.title(f"Dr's Portal: {st.session_state.patient_name}")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Medical Tracker", "Diet & FAQ"])
    
    # Core Pregnancy Calculations (Used across all pages)
    lmp = st.session_state.lmp
    edd = lmp + timedelta(days=280)
    today = datetime.now().date()
    weeks = (today - lmp).days // 7
    days = (today - lmp).days % 7

    # PAGE: DASHBOARD
    if page == "Dashboard":
        st.header("🤰 Your Pregnancy Progress")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Weeks Completed", f"{weeks}w {days}d")
        with col2:
            st.metric("Due Date", edd.strftime("%d %b %Y"))
        
        # Progress visualization
        progress = min(weeks / 40, 1.0)
        st.progress(progress)
        st.caption(f"You are approximately {int(progress*100)}% through your pregnancy.")

    # PAGE: MEDICAL TRACKER
    elif page == "Medical Tracker":
        st.header("🧪 Clinical Milestones")
        
        # Smart Alert Logic
        if 24 <= weeks <= 28:
            st.warning("⚠️ **Sugar Test (OGTT) Window:** Please schedule this week.")
        
        st.markdown("### Upcoming Schedule")
        t_data = {
            "Timeline": ["11-13 Weeks", "18-22 Weeks", "24-28 Weeks", "27-36 Weeks"],
            "Task": ["NT Scan / Double Marker", "Anomaly Scan (TIFFA)", "Diabetes Screening (OGTT)", "Tdap Vaccination"],
            "Status": ["Incomplete" if weeks < 11 else "Pending" for _ in range(4)]
        }
        st.table(pd.DataFrame(t_data))

    # PAGE: DIET & FAQ
    elif page == "Diet & FAQ":
        st.header("🍏 Nutritional Guidance")
        if weeks < 13:
            st.info("**Trimester 1:** Focus on Folic Acid & Protein. Small frequent meals for nausea.")
        elif 13 <= weeks < 27:
            st.info("**Trimester 2:** Iron & Calcium intake is critical now. Hydration is key.")
        else:
            st.info("**Trimester 3:** High energy needs. Monitor fetal kicks and salt intake.")

    # Vitals Logging (Always available at bottom)
    st.markdown("---")
    with st.expander("📝 Log Vitals for Clinic"):
        bp = st.text_input("Blood Pressure")
        wt = st.number_input("Weight (kg)", step=0.1)
        if st.button("Save Entry"):
            try:
                # Read, Append, Update
                df = conn.read(ttl=0)
                new_data = pd.DataFrame([{
                    "Name": st.session_state.patient_name,
                    "Weeks": f"{weeks}w {days}d",
                    "EDD": edd.strftime('%Y-%m-%d'),
                    "BP": bp,
                    "Weight": wt,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Successfully recorded in your medical file!")
            except Exception as e:
                st.error(f"Sync error: {e}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
