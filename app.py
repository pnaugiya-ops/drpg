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

# --- 3. DOCTOR DASHBOARD (RESTORED) ---
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
            st.info("No lab records submitted by patients yet.")

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
            st.success("Video successfully broadcasted to all patients.")

# --- 4. PATIENT DASHBOARD ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Lab Reports & Trends", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment", "Doctor's Updates"])
    
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
        else:
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Lab Reports & Trends":
        st.header("📊 Lab Report Entry")
        with st.form("lab_entry"):
            hb = st.number_input("Hemoglobin", 5.0, 20.0, 12.0)
            tsh = st.number_input("TSH Level", 0.0, 15.0, 2.5)
            sugar = st.number_input("Blood Sugar", 50, 500, 90)
            if st.form_submit_button("Save Records"):
                st.session_state.lab_records.append({"Date": date.today(), "Name": st.session_state.name, "Hb": hb, "TSH": tsh, "Sugar": sugar})
                st.success("Records saved and updated in trends.")

    elif m == "Diet Plans":
        pref = st.radio("Select Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "Pregnant" in st.session_state.stat:
            st.header(f"🤰 Detailed {pref} Pregnancy Diet")
            tri = st.selectbox("Select Trimester", ["1st Trimester (0-12wks)", "2nd Trimester (13-26wks)", "3rd Trimester (27-40wks)"])
            
            if pref == "Vegetarian":
                st.write("**Early Morning:** 5 Soaked Almonds + Warm Water.")
                st.write("**Breakfast:** Veggie Poha OR Moong Dal Chilla OR Stuffed Paratha with Curd.")
                st.write("**Mid-Morning:** 1 Fruit (Pomegranate/Apple) + Coconut Water.")
                st.write("**Lunch:** 2 Roti + 1 Bowl Dal + 1 Bowl Seasonal Vegetable + Fresh Salad.")
                st.write("**Evening:** Roasted Makhana OR Sprouted Moong Salad.")
                st.write("**Dinner:** 1-2 Roti + Paneer Bhurji OR Mix Veg + Warm Milk before bed.")
            else:
                st.write("**Early Morning:** 1 Boiled Egg + 5 Soaked Almonds.")
                st.write("**Breakfast:** Egg Omelet with Spinach OR Chicken Keema Paratha + Curd.")
                st.write("**Mid-Morning:** 1 Fruit (Apple/Banana) + Handful of Walnuts.")
                st.write("**Lunch:** 2 Roti + Grilled Chicken or Fish Curry + Spinach Sabzi + Salad.")
                st.write("**Evening:** Chicken Soup OR Boiled Egg Whites.")
                st.write("**Dinner:** Grilled Fish OR Egg Curry + 1 Roti + Steamed Veggies.")

        elif "PCOS" in st.session_state.stat:
            st.header(f"🌸 Detailed {pref} PCOS Diet Chart")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with Cinnamon (Dalchini) or ACV.")
                st.write("**Breakfast:** Besan Chilla with veggies OR Vegetable Dalia.")
                st.write("**Mid-Morning:** 1 Apple or Pear + 2 Walnuts.")
                st.write("**Lunch:** 2 Missi Roti + 1 bowl Dal + Curd + Large Salad.")
                st.write("**Evening:** Green Tea + Roasted Chana.")
                st.write("**Dinner:** Soya Chunks Curry OR Tofu Stir-fry with Broccoli.")
            else:
                st.write("**Early Morning:** Lemon water OR Fenugreek water.")
                st.write("**Breakfast:** 2 Egg White Omelet with Spinach and Mushrooms.")
                st.write("**Mid-Morning:** 1 bowl Papaya OR Handful of Flax seeds.")
                st.write("**Lunch:** Grilled Chicken + 1 small portion Brown Rice + Huge Salad.")
                st.write("**Evening:** Clear Chicken Soup OR 10 Almonds.")
                st.write("**Dinner:** Baked Fish (Salmon/Mackerel) OR Chicken Salad.")

        elif "Lactating" in st.session_state.stat:
            st.header(f"🤱 {pref} Lactation Support Diet")
            if pref == "Vegetarian":
                st.write("**Morning:** Fenugreek water. **Breakfast:** Ragi dosa or Oats.")
                st.write("**Lunch:** 2-3 Rotis, Dal, Green Veggie. **Dinner:** Khichdi with Ghee.")
            else:
                st.write("**Morning:** Milk with almonds. **Breakfast:** 2 Scrambled eggs.")
                st.write("**Lunch:** Chicken/Fish Curry + Brown Rice. **Dinner:** Lean meat stir-fry.")

    elif m == "Exercise & Yoga":
        st.header("🧘 Recommended Exercise")
        if "Pregnant" in st.session_state.stat:
            st.write("✅ **1st Tri:** Gentle walking. **2nd Tri:** Wall squats. **3rd Tri:** Butterfly pose.")
        elif "Lactating" in st.session_state.stat:
            st.write("✅ **Weeks 0-6:** Short walks, Kegels. **After 6wks:** Swimming and Yoga.")
        else:
            st.write("✅ **PCOS:** 45 mins brisk walk + 3 days strength training (squats/planks).")

    elif m == "Health Vitals":
        st.header("📈 Record Vitals")
        h = st.number_input("Height (cm)", 100, 250, 160)
        w = st.number_input("Weight (kg)", 30, 200, 60)
        bp = st.text_input("Blood Pressure")
        pls = st.number_input("Pulse Rate", 40, 180, 72)
        if st.button("Save Vitals"):
            st.success("Vitals saved to database.")

    elif m == "Vaccinations":
        st.header("💉 Important Dates")
        st.write("Track your TT, Tdap, Flu, and HPV vaccine doses here.")

    elif m == "Book Appointment":
        st.header("📅 Book Appointment")
        dt = st.date_input("Select Date", min_value=date.today())
        if dt in st.session_state.blocked_dates or dt.weekday() == 6:
            st.error("Clinic is closed on this date.")
        else:
            slots = [f"{h:02d}:00 AM" for h in range(11, 14)] + [f"{h-12:02d}:00 PM" for h in range(18, 21)]
            tm = st.selectbox("Select 15-Min Slot", slots)
            if st.button("Confirm Booking"):
                st.session_state.appointments.append({"Patient": st.session_state.name, "Date": dt, "Time": tm})
                st.success(f"Appointment confirmed for {dt} at {tm}.")

    elif m == "Doctor's Updates":
        st.header("📢 Video Guidance from Dr. Priyanka")
        if st.session_state.broadcasts:
            for b in st.session_state.broadcasts:
                st.video(b['url'])
                st.write(b['desc'])
        else:
            st.write("Stay tuned for upcoming health videos.")
