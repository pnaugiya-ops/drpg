import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP & STYLE ---
st.set_page_config(page_title="GynaeCare Hub", page_icon="🏥", layout="wide")

# Custom CSS for a better look
st.markdown("""
    <style>
    .main { background-color: #fff5f7; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b6b; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_index=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- 2. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.title("🏥 GynaeCare Digital Clinic")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.markdown("📞 **Emergency:** +91 9676712517")
        c2.markdown("📧 **Email:** pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Name")
            status = st.radio("Are you pregnant?", ["Yes", "No (PCOS/Gynae)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name = True, name
                st.session_state.status, st.session_state.role = status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title(f"Welcome, {st.session_state.patient_name}")
    
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Clinic Admin", ["Appointments", "Patient Logs", "Post Updates"])
        df = conn.read(ttl=0)
        # [Doctor Logic remains same as previous version]

    else:
        menu = st.sidebar.radio("Navigation", ["My Health Dashboard", "Diet & Nutrition", "Medical FAQs & Yoga", "Book Appointment", "Records"])
        df = conn.read(ttl=0)

        # --- PREGNANCY DIET LOGIC ---
        if menu == "Diet & Nutrition":
            st.title("🥗 Personalized Nutrition Plan")
            diet_type = st.radio("Select Preference", ["Vegetarian", "Non-Vegetarian"])
            
            if st.session_state.status == "Yes":
                trim = st.selectbox("Select Trimester", ["1st Trimester (0-12w)", "2nd Trimester (13-26w)", "3rd Trimester (27-40w)"])
                
                if trim == "1st Trimester (0-12w)":
                    st.header("🍎 1st Trimester: Foundation (1800-2000 kcal)")
                    st.write("**Focus:** Folic acid & managing nausea.")
                    if diet_type == "Vegetarian":
                        st.markdown("- **Breakfast:** Sprouted moong or Poha with nuts.\n- **Lunch:** Brown rice, Dal, Spinach (Palak).\n- **Dinner:** Paneer sautéed with veggies.")
                    else:
                        st.markdown("- **Breakfast:** Boiled eggs or Egg bhurji.\n- **Lunch:** Chicken soup or Fish curry with rice.\n- **Dinner:** Grilled chicken salad.")
                
                elif trim == "2nd Trimester (13-26w)":
                    st.header("🥩 2nd Trimester: Growth (2200-2400 kcal)")
                    st.write("**Focus:** Iron and Calcium for bone development.")
                    st.info("Add an extra 340 calories/day.")
                
                elif trim == "3rd Trimester (27-40w)":
                    st.header("🥛 3rd Trimester: Energy (2400-2600 kcal)")
                    st.write("**Focus:** Omega-3 (DHA) for brain & Energy.")

            else:
                st.header("🩸 PCOS Management Diet (1500-1800 kcal)")
                st.write("**Focus:** Low Glycemic Index & High Protein.")
                if diet_type == "Vegetarian":
                    st.markdown("- **Tips:** Use Ragi/Jowar instead of wheat. High fiber salads.")
                else:
                    st.markdown("- **Tips:** Include lean meat. Avoid fried chicken or heavy oils.")

        # --- MEDICAL FAQs & YOGA ---
        elif menu == "Medical FAQs & Yoga":
            st.title("📚 Knowledge & Wellness")
            
            with st.expander("🤮 Managing Nausea & Vomiting (Morning Sickness)"):
                st.write("**Remedies:** Ginger tea, small frequent meals, dry toast/crackers before getting out of bed.")
            
            with st.expander("⚠️ Is my Abdominal Pain serious?"):
                st.write("**Normal:** Mild stretching (Round ligament pain).")
                st.error("**Serious:** Sharp, persistent pain with bleeding or fever. Contact Dr. immediately.")

            with st.expander("🧘 Safe Yoga & Exercise"):
                st.markdown("1. **Marjariasana (Cat-Cow):** Relieves back tension.")
                st.markdown("2. **Baddha Konasana (Butterfly):** Improves hip flexibility.")
                st.warning("Avoid lying flat on your back after the 1st trimester.")

        # [Include Dashboard, Booking, and Records code from previous version here]

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
