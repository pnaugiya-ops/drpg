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
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #ff4b6b; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- 2. LOGIN SCREEN (2 OPTIONS ONLY) ---
if not st.session_state.logged_in:
    st.title("🏥 Welcome to Bhavya Labs & Clinics")
    st.subheader("Your Partner in Obstetric & Gynaecological Health")
    
    with st.container(border=True):
        st.markdown("""
        **Our Comprehensive Services:**
        🩺 **Consultation:** Obs & Gynae | 🔬 **Fertility:** IUI, Follicular Study | 🔪 **Surgery:** Laparoscopy  
        🩸 **Thyrocare Franchise:** All Blood Tests | 🔊 **Ultrasound** | 💊 **Pharmacy**
        """)
        c1, c2 = st.columns(2)
        c1.markdown("📞 **Call:** +91 9676712517")
        c2.markdown("📧 **Email:** pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Patient Name")
            status = st.radio("Current Status", ["Pregnant", "Non-Pregnant (PCOS/Fertility/General)"])
            if st.form_submit_button("Enter My Portal") and name:
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
    st.sidebar.title(f"Bhavya Clinics")
    st.sidebar.info(f"User: {st.session_state.patient_name}")
    
    if st.session_state.role == "Doctor":
        # [Doctor Admin logic remains established]
        st.sidebar.success("Admin Mode Active")
        menu = st.sidebar.radio("Clinic Admin", ["Appointments", "Patient Database", "Post Updates"])
        # ... (Include previous Doctor code here)

    else:
        menu = st.sidebar.radio("Navigation", ["Home Dashboard", "Detailed Diet Plans", "Medical Library", "Book Appointment", "My Records"])
        
        # --- DASHBOARD ---
        if menu == "Home Dashboard":
            st.title(f"Welcome, {st.session_state.patient_name}")
            if st.session_state.status == "Pregnant":
                st.markdown("### 🤰 Your Pregnancy Journey")
                # LMP Calculation logic...
                st.info("💡 Tip: Don't forget to check the Medical Library for your Vaccination schedule!")
            else:
                st.markdown("### 🌸 Gynaecology & Wellness Hub")
                st.write("Access expert advice on PCOS, Fertility, and Preventative Screenings below.")

        # --- DIET PLANS ---
        elif menu == "Detailed Diet Plans":
            st.title("🥗 Clinical Nutrition Guide")
            diet_pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
            
            if st.session_state.status == "Pregnant":
                stage = st.selectbox("Select Stage", ["1st Trimester", "2nd Trimester", "3rd Trimester", "Lactation (Post-Delivery)"])
                if stage == "1st Trimester":
                    st.subheader("🍎 1st Trimester (1800-2000 kcal)")
                    st.write("Focus on Folic Acid. Managing Nausea with small meals.")
                elif stage == "2nd Trimester":
                    st.subheader("🥩 2nd Trimester (2200-2400 kcal)")
                    st.write("Focus on Iron & Calcium for fetal bone growth.")
                elif stage == "3rd Trimester":
                    st.subheader("🥛 3rd Trimester (2400-2600 kcal)")
                    st.write("Focus on Fiber & Omega-3. Prevent acidity & constipation.")
                elif stage == "Lactation (Post-Delivery)":
                    st.subheader("🤱 Lactation Diet (2600-2800 kcal)")
                    st.write("**Galactagogues:** Fenugreek (Methi), Fennel, Oats, Garlic, and plenty of fluids.")
            else:
                st.subheader("🩸 PCOS & Weight Management")
                st.write("Focus: Low Glycemic Index (GI) and High Fiber to control insulin spikes.")

        # --- MEDICAL LIBRARY (The Core Knowledge Base) ---
        elif menu == "Medical Library":
            st.title("📚 Bhavya Health Library")
            
            if st.session_state.status == "Pregnant":
                with st.expander("💉 Pregnancy Vaccinations"):
                    st.write("**Tetanus (TT/Td):** 2 doses are mandatory to protect you and your baby.")
                    st.write("**Influenza:** Recommended in any trimester.")
                with st.expander("💉 Post-Delivery / Lactation"):
                    st.write("**HPV Vaccine:** It is perfectly safe to take the HPV vaccine while breastfeeding.")
            
            else:
                with st.expander("🔬 Infertility & Procedures"):
                    st.write("**Follicular Monitoring:** Serial ultrasounds to track egg growth.")
                    st.write("**IUI (Intrauterine Insemination):** Processing sperm and placing it in the uterus.")
                    st.write("**IVF Guidance:** Step-by-step support for advanced conception.")
                
                with st.expander("🏥 Laparoscopy (Keyhole Surgery)"):
                    st.write("Minimally invasive surgery for Ovarian Cysts, Endometriosis, and Fibroids. Faster recovery and minimal scarring.")
                
                with st.expander("🛡️ Preventive Screening (Pap Smear & HPV)"):
                    st.write("**Pap Smear:** A simple test to check for early cervical cell changes.")
                    st.write("**HPV Vaccination:** Prevents 90% of cervical cancers. Recommended for all women.")

        # --- APPOINTMENTS ---
        elif menu == "Book Appointment":
            st.header("📅 Book at Bhavya Clinics")
            st.checkbox("💉 Include Thyrocare Blood Test (Thyroid, CBC, HbA1c, etc.)")
            # [Appointment slots logic here]

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
