import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SETUP & STYLE ---
st.set_page_config(page_title="GynaeCare Hub", page_icon="🏥", layout="wide")

# Fixed the CSS Error here
st.markdown("""
    <style>
    .main { background-color: #fffafa; }
    .stButton>button { border-radius: 20px; background-color: #ff4b6b; color: white; border: none; }
    .stExpander { background-color: white; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

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
        c2.markdown(f"📧 **Email:** pnaugiya@gmail.com")

    t1, t2 = st.tabs(["Patient Access", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Patient Full Name")
            status = st.radio("Are you currently pregnant?", ["Yes", "No (PCOS/General)"])
            if st.form_submit_button("Enter Portal") and name:
                st.session_state.logged_in, st.session_state.patient_name = True, name
                st.session_state.status, st.session_state.role = status, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login as Doctor") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role, st.session_state.patient_name = True, "Doctor", "Dr. Admin"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    st.sidebar.title(f"Logged in: {st.session_state.patient_name}")
    
    if st.session_state.role == "Doctor":
        menu = st.sidebar.radio("Clinic Admin", ["Appointments", "Patient Database", "Post Video/Updates"])
        df = conn.read(ttl=0)
        # [Doctor Logic code here remains the same as before]

    else:
        menu = st.sidebar.radio("Navigation", ["Dashboard", "Diet & Nutrition", "Medical FAQs & Yoga", "Book Appointment", "Records"])
        df = conn.read(ttl=0)

        # --- PREGNANCY DIET ---
        if menu == "Diet & Nutrition":
            st.title("🥗 Detailed Meal Plans")
            diet_type = st.radio("Dietary Preference", ["Vegetarian", "Non-Vegetarian"])
            
            if st.session_state.status == "Yes":
                trim = st.selectbox("Select Your Trimester", ["1st Trimester (0-12 Weeks)", "2nd Trimester (13-26 Weeks)", "3rd Trimester (27-40 Weeks)"])
                
                if trim == "1st Trimester (0-12 Weeks)":
                    st.header("🍎 1st Trimester: Foundation")
                    st.info("Goal: 1800-2000 kcal. Focus on Folic Acid to prevent birth defects.")
                    if diet_type == "Vegetarian":
                        st.write("**Early Morning:** Soaked almonds/walnuts. \n**Breakfast:** Moong Dal Chilla or Poha. \n**Lunch:** 2 Roti, Dal, Green Veggie (Spinach/Methi), Curd. \n**Dinner:** Vegetable Dalia or Paneer.")
                    else:
                        st.write("**Early Morning:** Soaked nuts. \n**Breakfast:** 2 Boiled Eggs or Egg Bhurji. \n**Lunch:** 1 bowl Chicken Curry (less oil), Rice, Salad. \n**Dinner:** Grilled Fish or Egg Curry.")
                
                elif trim == "2nd Trimester (13-26 Weeks)":
                    st.header("🥩 2nd Trimester: Growth")
                    st.info("Goal: 2200-2400 kcal. Focus on Iron (blood) and Calcium (bones).")
                    st.write("**Key Foods:** Jaggery (Gur), Pomegranate, Milk, Paneer/Lean Meat.")

                elif trim == "3rd Trimester (27-40 Weeks)":
                    st.header("🥛 3rd Trimester: Energy")
                    st.info("Goal: 2400-2600 kcal. Focus on Fiber (to avoid constipation) and Omega-3.")

            else:
                st.header("🩸 PCOS Management Plan")
                st.info("Goal: 1500-1800 kcal. Low Glycemic Index to balance Insulin.")
                if diet_type == "Vegetarian":
                    st.write("**Diet:** Replace White Rice with Brown Rice/Ragi. Increase Protein with Sprouts and Tofu.")
                else:
                    st.write("**Diet:** Include Fish and Grilled Chicken. Strictly avoid Fried Meats/Sugary drinks.")

        # --- MEDICAL FAQs & YOGA ---
        elif menu == "Medical FAQs & Yoga":
            st.title("📚 Education & Wellness")
            
            with st.expander("🤮 Nausea & Vomiting (Morning Sickness)"):
                st.write("**Dos:** Eat dry crackers before getting up. Use Ginger/Lemon water. Eat small, frequent meals.")
                st.write("**Don'ts:** Avoid spicy/oily food. Don't stay on an empty stomach for long.")
            
            with st.expander("⚠️ Understanding Abdominal Pain"):
                st.write("**Normal:** Mild pulling sensation on the sides (Round Ligament Pain).")
                st.error("**WARNING:** If pain is accompanied by bleeding, blurred vision, or severe cramping, call Dr. immediately.")

            with st.expander("🧘 Safe Yoga & Exercise"):
                st.write("1. **Butterfly Pose (Baddha Konasana):** Great for pelvic health.")
                st.write("2. **Cat-Cow Stretch:** Relieves back pain.")
                st.write("3. **Pranayama:** Helps manage stress and oxygen flow.")
                

        # --- BOOKING & RECORDS (Included for completeness) ---
        elif menu == "Book Appointment":
            st.header("📅 Book Appointment")
            # [Add previous booking logic here]

        elif menu == "Records":
            st.header("📝 Log Vitals")
            # [Add previous record logging logic here]

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
