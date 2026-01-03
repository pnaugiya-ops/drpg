import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fffafa; }
    .stButton>button { border-radius: 20px; background-color: #ff4b6b; color: white; border: none; }
    .stExpander { background-color: white; border-radius: 10px; margin-bottom: 10px; }
    .clinic-header { color: #ff4b6b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- 2. LOGIN & WELCOME SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 Welcome to Bhavya Labs & Clinics")
    st.markdown("### *Comprehensive Care under one roof*")
    
    with st.container(border=True):
        st.markdown("""
        **Our Services:**
        ✅ Gynaecology & Obstetric Consultation | ✅ Ultrasound | ✅ Pharmacy  
        ✅ **Full Body Blood Tests (Thyrocare Franchise)** | ✅ Laparoscopy & Infertility
        """)
        c1, c2 = st.columns(2)
        c1.markdown("📞 **Appointment:** +91 9676712517")
        c2.markdown("📧 **Email:** pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Patient Name")
            status = st.selectbox("Purpose of Visit", ["Pregnancy", "PCOS / General Gynae", "Infertility / Laparoscopy"])
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
    st.sidebar.title(f"Bhavya Clinics")
    st.sidebar.write(f"Logged in: {st.session_state.patient_name}")
    
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Admin", ["Appointments", "Patient Database", "Post Video/Updates"])
        # [Doctor logic remains as previously established]

    else:
        menu = st.sidebar.radio("Menu", ["Dashboard", "Detailed Diet Plans", "Medical Library", "Book Appointment", "Records"])
        
        # --- DASHBOARD ---
        if menu == "Dashboard":
            st.title(f"Welcome to Bhavya Labs & Clinics, {st.session_state.patient_name}")
            if st.session_state.status == "Pregnancy":
                st.info("🤰 Pregnancy Tracking Active")
                # [LMP/EDD Logic here]
            elif st.session_state.status == "Infertility / Laparoscopy":
                st.success("🔬 Specialized Fertility & Surgical Module")
                st.write("We offer advanced Laparoscopic solutions and Infertility workups.")

        # --- DETAILED DIETS (All Trimesters & Lactation) ---
        elif menu == "Diet & Nutrition":
            st.title("🥗 Clinical Nutrition Plans")
            diet_pref = st.radio("Preference", ["Vegetarian", "Non-Vegetarian"])
            
            stage = st.selectbox("Select Stage", ["1st Trimester", "2nd Trimester", "3rd Trimester", "Lactation (Breastfeeding)", "PCOS / Weight Loss"])
            
            if "Trimester" in stage:
                if stage == "1st Trimester":
                    st.header("🍎 1st Trimester (1800-2000 kcal)")
                    st.write("**Focus:** Folic Acid. Avoid raw papaya/pineapple.")
                elif stage == "2nd Trimester":
                    st.header("🥩 2nd Trimester (2200-2400 kcal)")
                    st.write("**Focus:** Iron & Calcium. Add 340 extra calories.")
                elif stage == "3rd Trimester":
                    st.header("🥛 3rd Trimester (2400-2600 kcal)")
                    st.write("**Focus:** Energy & Fiber. Avoid heavy spicy meals to prevent heartburn.")
            
            elif stage == "Lactation (Breastfeeding)":
                st.header("🤱 Post-Partum & Lactation (2600-2800 kcal)")
                st.info("You need ~500 extra calories compared to pre-pregnancy.")
                st.write("**Galactagogues (Milk Boosting Foods):**")
                st.markdown("- **Vegetarian:** Fenugreek (Methi) seeds, Fennel (Saunf), Garlic, Oats, Milk, and Gond Ladoo.")
                st.markdown("- **Non-Veg:** Chicken soup and Fish (rich in Omega-3).")
                st.write("**Hydration:** Drink 3-4 Litres of water daily.")

        # --- MEDICAL LIBRARY (New Sections Added) ---
        elif menu == "Medical Library":
            st.title("📚 Bhavya Health Library")
            
            with st.expander("🔬 Infertility & Laparoscopy"):
                st.write("**Infertility:** We provide follicular monitoring, IUI, and hormonal balancing.")
                st.write("**Laparoscopy:** Minimally invasive 'Keyhole' surgery for Ovarian Cysts, Fibroids, and Tubal checks.")

            with st.expander("💊 Contraception (Family Planning)"):
                st.write("Options available at Bhavya Clinics:")
                st.markdown("- **Short term:** OCPs (Pills), Injectables (Antara).")
                st.markdown("- **Long term:** Copper-T (IUD), LNG-IUS.")

            with st.expander("💉 Vaccinations (HPV & Lactation)"):
                st.write("**During Lactation:** It is 100% SAFE to take the HPV vaccine while breastfeeding.")
                st.write("**HPV Vaccine:** Essential for preventing Cervical Cancer. Available for women up to age 45.")

        elif menu == "Book Appointment":
            st.header("📅 Schedule at Bhavya Clinics")
            # [Appointment Logic]

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
