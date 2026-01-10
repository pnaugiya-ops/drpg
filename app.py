import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIG & GLOBAL CONNECTION ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

# Central connection to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

def save_to_clinic_sheets(p_name, category, detail_text):
    """Saves any data (Appointments/Vitals/Labs) to the cloud sheet"""
    try:
        existing_df = conn.read(worksheet="Appointments", ttl=0)
        new_row = pd.DataFrame([{
            "Name": p_name,
            "Type": category,
            "Details": detail_text,
            "Attachment": "N/A",
            "Timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }])
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        conn.update(worksheet="Appointments", data=updated_df)
        return True
    except:
        return False

# --- 2. UI STYLING ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .dr-header { background:#003366; color:white; padding:25px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .clinic-badge { background:#ff4b6b; color:white; padding:6px 18px; border-radius:20px; font-weight:bold; display:inline-block; margin:5px; font-size:14px; border: 1px solid white; }
    .diet-card { background:#ffffff; padding:20px; border-radius:12px; border:1px solid #e0e0e0; border-left:6px solid #ff4b6b; margin-bottom:15px; line-height: 1.6; color: #333; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width: 100%; height: 3em; }
    section[data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 2px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'blocked' not in st.session_state: st.session_state.blocked = []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 3. LOGIN & BRANDING ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h2 style='margin:0;'>Dr. Priyanka Gupta</h2>
        <p style='font-size:1.2em;'>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Franchise Lab</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
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
    st.markdown(f"### 📋 Patient: {st.session_state.name} ({st.session_state.age} yrs)")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    m = st.segmented_control("SELECT VIEW", options=["Health Tracker", "Cyle Tracker","Diet Plans", "Exercise", "Lab Reports", "Vitals", "Social", "Book Slot"], default="Health Tracker")
    st.divider()

    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
        elif st.session_state.stat == "Lactating Mother":
            st.header("📋 Postpartum Health")
            st.write("Contraception: OCPs, Copper T, Barrier Methods.")
        else:
            st.header("📋 PCOS Health Progress")
elif m == "Cycle Tracker":
        st.header("📅 Menstrual Cycle & PCOS Tracker")
        
        col1, col2 = st.columns(2)
        with col1:
            last_period = st.date_input("When did your last period start?", value=date.today() - timedelta(days=28))
            prev_period = st.date_input("When did the period before THAT start?", value=date.today() - timedelta(days=56))
        
        # Calculate Cycle Length
        cycle_length = (last_period - prev_period).days
        
        with col2:
            st.metric("Your Cycle Length", f"{cycle_length} Days")
            if cycle_length > 35:
                st.warning("PCOS Alert: Your cycle is longer than the typical 28-35 day range.")
            elif cycle_length < 21:
                st.warning("Alert: Your cycle is shorter than 21 days.")
            else:
                st.success("Your cycle length is within the typical range.")

        # Prediction Logic
        # For PCOS, we use the user's actual cycle length for prediction if it's within 21-45 days.
        # Otherwise, we default to 28 for "Normal" comparison.
        prediction_days = cycle_length if 21 <= cycle_length <= 45 else 28
        next_period = last_period + timedelta(days=prediction_days)
        
        st.divider()
        st.subheader(f"Next Expected Period: {next_period.strftime('%d %b %Y')}")
        
        # PCOS Specific Educational Content
        with st.expander("Why do PCOS cycles vary?"):
            st.write("""
            In PCOS, hormonal imbalances (higher androgens) can prevent regular ovulation. 
            This leads to:
            * **Oligomenorrhea:** Fewer than 9 periods a year.
            * **Anovulation:** The body doesn't release an egg, causing the cycle to stretch.
            * **Tip:** Tracking 'Basal Body Temperature' or 'Cervical Mucus' can be more accurate than calendar dates for PCOS.
            """)
            
        if st.button("Log Cycle Data"):
            details = f"Cycle Length: {cycle_length} days, Last Period: {last_period}"
            save_to_clinic_sheets(st.session_state.name, "Cycle Log", details)
            st.success("Cycle data saved for your doctor to review!")

    elif m == "Diet Plans":
        st.header(f"🥗 Clinical Diet Chart: {st.session_state.stat}")
        
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1:
                st.markdown("""<div class='diet-card'>
                <b>Focus: Folic Acid & Vitamin B6 (Weeks 1-12)</b><br>
                • <b>Early Morning:</b> 4-5 soaked almonds + warm water.<br>
                • <b>Breakfast:</b> Veggie Poha/Upma or Whole grain toast + 2 boiled eggs + milk.<br>
                • <b>Lunch:</b> 2 Rotis + Spinach Dal + Sautéed Veggies + Curd.<br>
                • <b>Evening:</b> Roasted Makhana or Sprout salad.<br>
                • <b>Dinner:</b> Veg Khichdi + Curd or Grilled Fish/Chicken + Greens.
                </div>""", unsafe_allow_html=True)
            with t2:
                st.markdown("""<div class='diet-card'>
                <b>Focus: Calcium & Iron (Weeks 13-26)</b><br>
                • <b>Early Morning:</b> Soaked walnuts/almonds + water.<br>
                • <b>Breakfast:</b> Vegetable Paratha with curd or Oats porridge.<br>
                • <b>Lunch:</b> Brown rice + Dal + Mixed Veggies + Salad.<br>
                • <b>Evening:</b> Banana smoothie with flaxseeds or Buttermilk.<br>
                • <b>Dinner:</b> Whole wheat chapati + Paneer or Chicken curry.
                </div>""", unsafe_allow_html=True)
            with t3:
                st.markdown("""<div class='diet-card'>
                <b>Focus: High Fiber & Healthy Fats (Weeks 27-40)</b><br>
                • <b>Early Morning:</b> Warm water + soaked fenugreek seeds.<br>
                • <b>Breakfast:</b> Besan Chilla or Oats porridge with nuts + 2 eggs.<br>
                • <b>Lunch:</b> Millet khichdi with veggies + Dal + Salad.<br>
                • <b>Evening:</b> Yogurt with flaxseeds or Sprout chaat.<br>
                • <b>Dinner:</b> Chapati + Rajma/Chole + Vegetable sabzi + Curd.
                </div>""", unsafe_allow_html=True)

        elif st.session_state.stat == "PCOS/Gynae":
            vt, nvt = st.tabs(["Vegetarian Plan", "Non-Vegetarian Plan"])
            with vt:
                st.markdown("""
                | Time | Item | Note |
                | :--- | :--- | :--- |
                | **Early Morning** | Lemon water + 5 soaked almonds | Improves metabolism |
                | **Breakfast** | Moong dal chilla + Mint chutney | High protein & fiber |
                | **Lunch** | 2 Jowar/Bajra rotis + Mixed veg + Dal | Prevents sugar spikes |
                | **Snack** | Roasted makhana + Green tea | Avoid sugary tea |
                | **Dinner** | Tofu/Paneer stir-fry with veggies | Keep it light |
                """, unsafe_allow_html=True)
            with nvt:
                st.markdown("""
                | Time | Item | Note |
                | :--- | :--- | :--- |
                | **Early Morning** | Lemon water + Soaked chia seeds | Stabilizes blood sugar |
                | **Breakfast** | 2 Boiled egg whites + Whole grain toast | Protein stability |
                | **Lunch** | Grilled chicken/Fish + Brown rice + Salad | Rich in Omega-3 |
                | **Snack** | 1 Boiled egg or Roasted chana | Reduces cravings |
                | **Dinner** | Grilled fish/chicken + Sautéed veggies | Avoid heavy curries |
                """, unsafe_allow_html=True)
        elif st.session_state.stat == "Lactating Mother":
            st.info("Additional 300–500 calories required per day.")
            st.markdown("""<div class='diet-card'>
            <b>Lactation Support Plan (Galactagogues)</b><br>
            • <b>Morning:</b> Warm water with soaked fenugreek (Methi) or Cumin (Jeera) water.<br>
            • <b>Diet Focus:</b> Oats, Ragi, Papaya, and Methi/Gond Ladoos.<br>
            • <b>Hydration:</b> Drink 8-12 glasses of water. Have a glass during every nursing session.
            </div>""", unsafe_allow_html=True)

    elif m == "Exercise":
        st.header("🧘 Therapeutic Movement")
        
        if st.session_state.stat == "Pregnant":
            exp = st.expander("Trimester-Wise Guide", expanded=True)
            exp.markdown("""
            - **T1:** Walking, Prenatal Yoga, Kegels, Cat-Cow Stretch.
            - **T2:** Swimming, Stationary Cycling, Wall Squats, Side-Lying Leg Lifts.
            - **T3:** Butterfly Stretch, Deep Supported Squats, Pelvic Tilts, Birthing Ball.
            """)
            st.warning("Talk Test: You should be able to hold a conversation while exercising.")

        elif st.session_state.stat == "PCOS/Gynae":
            st.write("### PCOS Strength & Insulin Sensitivity")
            st.write("- **Strength Training:** 3-4x/week (Squats, Lunges, Push-ups).")
            st.write("- **LISS Cardio:** 30-45 mins of Brisk Walking.")
            st.write("- **Habit Stack:** Walk for 10-15 minutes after every meal to lower blood sugar.")
            st.info("Limit HIIT to 2 sessions per week to avoid overstressing cortisol.")

        elif st.session_state.stat == "Lactating Mother":
            st.write("### Postpartum Recovery")
            st.write("- **Weeks 0-6:** Walking, Kegels, and Diaphragmatic 'Belly' Breathing.")
            st.write("- **Weeks 6-12:** Low-impact cardio (Swimming, Elliptical) + Bodyweight Squats.")
            st.write("- **After Week 12:** Gradually reintroduce jogging or light weights.")
            st.success("Tip: Exercise immediately AFTER breastfeeding to ensure comfort.")
    elif m == "Lab Reports":
        st.header("📊 Lab Tracking")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 90)
            tsh = st.number_input("Thyroid TSH", 0.0, 50.0, 2.5)
            urine = st.selectbox("Urine Test", ["Normal", "Trace", "+1", "+2"])
            if st.form_submit_button("Save Report"):
                details = f"Hb: {hb}, Sugar: {sugar}, TSH: {tsh}, Urine: {urine}"
                save_to_clinic_sheets(st.session_state.name, "Lab Report", details)
                st.success("Sent to Doctor!")

    elif m == "Vitals":
        st.header("📈 Vitals Tracker")
        with st.form("vital_form"):
            p, bp = st.number_input("Pulse Rate", 40, 150, 72), st.text_input("Blood Pressure", "120/80")
            wt, ht = st.number_input("Weight (kg)", 30.0, 150.0, 60.0), st.number_input("Height (cm)", 100.0, 220.0, 160.0)
            if st.form_submit_button("Update Vitals"):
                bmi = round(wt / ((ht/100)**2), 2)
                details = f"Pulse: {p}, BP: {bp}, Wt: {wt}, BMI: {bmi}"
                save_to_clinic_sheets(st.session_state.name, "Vitals", details)
                st.success("Vitals Updated!")

    elif m == "Book Slot":
        st.header("📅 Select Time Slot")
        slots = [f"{h}:{m:02d} AM" for h in [11] for m in [15, 30, 45]] + [f"{h}:{m:02d} PM" for h in [12, 1, 6, 7] for m in [0, 15, 30, 45]]
        d = st.date_input("Date", min_value=date.today())
        t = st.selectbox("Slot", slots)
        if st.button("Request Booking"):
            # Check if doctor blocked this date
            if str(d) in [str(bd) for bd in st.session_state.blocked]:
                st.error("Clinic is closed on this date.")
            else:
                save_to_clinic_sheets(st.session_state.name, "Appointment", f"Date: {d}, Time: {t}")
                st.success("Booking Request Sent!")

# --- 5. ADMIN PORTAL ---
elif st.session_state.role == "D":
    st.title("👩‍⚕️ Admin Master")
    if st.button("🔄 Refresh Data from Cloud"): 
        st.rerun()

    t1, t2, t3, t4 = st.tabs(["Appointments", "Patient Records", "Clinic Availability", "Social Media"])
    
    # FETCH GLOBAL DATA
    df_global = conn.read(worksheet="Appointments", ttl=0)

    with t1:
        st.subheader("Live Appointment Bookings")
        if not df_global.empty:
            apts = df_global[df_global['Type'] == "Appointment"]
            st.dataframe(apts, use_container_width=True)
        else:
            st.info("No bookings available yet.")

    with t2:
        st.subheader("Patient Health Data")
        if not df_global.empty:
            records = df_global[df_global['Type'].isin(["Lab Report", "Vitals"])]
            st.dataframe(records, use_container_width=True)

    with t3:
        st.subheader("Manage Clinic Schedule")
        bd = st.date_input("Select date to CLOSE clinic")
        if st.button("Mark Clinic Closed"):
            st.session_state.blocked.append(bd)
            st.warning(f"Clinic marked as CLOSED for {bd}")
        st.write("Current Blocked Dates (This Session):", st.session_state.blocked)

    with t4:
        with st.form("social_form"):
            yt = st.text_input("YouTube Link", value=st.session_state.social["yt"])
            ig = st.text_input("Instagram Link", value=st.session_state.social["ig"])
            if st.form_submit_button("Update Feed"):
                st.session_state.social.update({"yt": yt, "ig": ig})
                st.success("Social Media Updated!")
