import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False
if 'lab_records' not in st.session_state:
    st.session_state.lab_records = []
if 'appointments' not in st.session_state:
    st.session_state.appointments = []
if 'blocked_dates' not in st.session_state:
    st.session_state.blocked_dates = []
if 'broadcasts' not in st.session_state:
    st.session_state.broadcasts = []

# --- 2. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta - MS (Obs & Gynae)</h3>
        <div>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True,"name":n,"age":a,"stat":s,"role":"P"})
                    st.rerun()
    with t2:
        with st.form("d_login"):
            p = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if p == "clinicadmin786":
                    st.session_state.update({"logged_in":True,"role":"D","name":"Dr. Priyanka"})
                    st.rerun()

# --- 3. DOCTOR DASHBOARD ---
elif st.session_state.role == "D":
    st.sidebar.markdown(f"### 👩‍⚕️ Welcome, {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    
    dm = st.sidebar.radio("Doctor Panel", ["Manage Appointments", "Review Patient Reports", "Block Clinic Dates", "Broadcast Media"])

    if dm == "Manage Appointments":
        st.header("📅 Patient Appointments")
        if st.session_state.appointments:
            st.table(pd.DataFrame(st.session_state.appointments))
        else:
            st.info("No appointments currently booked.")

    elif dm == "Review Patient Reports":
        st.header("📋 Patient Lab Records")
        if st.session_state.lab_records:
            st.dataframe(pd.DataFrame(st.session_state.lab_records))
        else:
            st.info("No lab records found.")

    elif dm == "Block Clinic Dates":
        st.header("🚫 Date Management")
        b_date = st.date_input("Select Date to Block")
        if st.button("Block Date for All Bookings"):
            st.session_state.blocked_dates.append(b_date)
            st.success(f"Clinic bookings disabled for {b_date}")

    elif dm == "Broadcast Media":
        st.header("📢 Video Broadcast")
        v_url = st.text_input("Enter YouTube Video Link")
        v_desc = st.text_area("Video Title/Description")
        if st.button("Broadcast to Dashboard"):
            st.session_state.broadcasts.append({"url": v_url, "desc": v_desc})
            st.success("Video successfully broadcasted.")

# --- 4. PATIENT DASHBOARD ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment", "Doctor's Updates"])
    
    # --- DIET PLANS (RESTORING FULL DETAIL) ---
    if m == "Diet Plans":
        pref = st.radio("Select Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "Pregnant" in st.session_state.stat:
            st.header(f"🤰 Detailed {pref} Pregnancy Diet")
            tri = st.selectbox("Select Trimester", ["1st Trimester (0-12wks)", "2nd Trimester (13-26wks)", "3rd Trimester (27-40wks)"])
            if pref == "Vegetarian":
                st.write("**Early Morning:** 5 Soaked Almonds + 1 glass Warm Milk.")
                st.write("**Breakfast:** Veggie Poha OR Moong Dal Chilla OR Paneer/Aloo Paratha with Curd.")
                st.write("**Mid-Morning:** 1 Seasonal Fruit (Pomegranate/Apple/Guava) + Coconut Water.")
                st.write("**Lunch:** 2-3 Whole Wheat Roti + 1 Bowl Dal + 1 Bowl Green Vegetable + 1 Cup Curd + Fresh Salad.")
                st.write("**Evening Snack:** Roasted Makhana OR Sprouted Moong Salad OR Handful of Roasted Chana.")
                st.write("**Dinner:** 2 Roti + Paneer Bhurji OR Mixed Vegetable Curry + 1 glass Warm Milk before bed.")
            else:
                st.write("**Early Morning:** 1 Boiled Egg + 5 Soaked Almonds.")
                st.write("**Breakfast:** 2 Egg Omelet with Spinach OR Chicken Keema Paratha + 1 Bowl Curd.")
                st.write("**Mid-Morning:** 1 Seasonal Fruit (Apple/Banana) + Handful of Walnuts.")
                st.write("**Lunch:** 2 Roti + Grilled Chicken or Fish Curry + Spinach Sabzi + Cucumber & Tomato Salad.")
                st.write("**Evening Snack:** Chicken Soup OR 2 Boiled Egg Whites OR Handful of Almonds.")
                st.write("**Dinner:** Grilled Fish OR Egg Curry with 1 Roti + Steamed Vegetables (Broccoli/Carrots).")

        elif "PCOS" in st.session_state.stat:
            st.header(f"🌸 Detailed {pref} PCOS Diet Chart")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with Cinnamon (Dalchini) OR 1 tsp Apple Cider Vinegar in warm water.")
                st.write("**Breakfast:** Besan Chilla with added grated vegetables OR Vegetable Oats with Flax seeds.")
                st.write("**Mid-Morning:** 1 Apple or Pear + 2-3 Walnuts.")
                st.write("**Lunch:** 2 Missi Roti (Besan-Wheat mix) + 1 bowl Dal + 1 Cup Curd + Large Seasonal Salad.")
                st.write("**Evening Snack:** Green Tea + Roasted Chana OR Buttermilk (Chaas).")
                st.write("**Dinner:** Soya Chunks Curry OR Tofu Stir-fry with Broccoli, Capsicum, and Mushrooms.")
            else:
                st.write("**Early Morning:** Lemon water OR Fenugreek (Methi) water.")
                st.write("**Breakfast:** 2 Egg White Omelet with Spinach, Mushrooms, and Onions.")
                st.write("**Mid-Morning:** 1 bowl Papaya OR Handful of Flax seeds and Pumpkin seeds.")
                st.write("**Lunch:** Grilled Chicken + 1 small portion Brown Rice + Huge Mixed Green Salad.")
                st.write("**Evening Snack:** Clear Chicken Soup OR 10 Almonds.")
                st.write("**Dinner:** Baked Fish (Salmon/Mackerel/Trout) OR Chicken Salad with Olive Oil dressing.")

        elif "L
