import streamlit as st
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

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

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

# --- 3. MAIN APPLICATION ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Navigation", ["Health Tracker", "Diet Plans", "Exercise & Yoga", "Health Vitals", "Vaccinations", "Book Appointment"])
    
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. Implantation is occurring.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. Heart is beating.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. Baby starts moving fingers.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. Halfway! You feel kicks.")
            elif wks <= 30: st.info("🥦 Week 30: Size of a cabbage. Eyes open.")
            elif wks <= 40: st.info("🍉 Week 40: Full term! Ready for birth.")
        else:
            st.header("🗓️ Period Tracker")
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Diet Plans":
        pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        
        if "PCOS" in st.session_state.stat:
            st.header("🌸 Detailed PCOS Diet Plan")
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with lemon or cinnamon.")
                st.write("**Breakfast:** Moong Dal Chilla OR Vegetable Dalia OR Sprouted Salad.")
                st.write("**Mid-Morning:** 1 Fruit (Apple/Pear) + Handful of Walnuts.")
                st.write("**Lunch:** 2 Missi Roti + 1 bowl Dal + Green Veggie + Salad.")
                st.write("**Evening:** Roasted Chana OR Buttermilk.")
                st.write("**Dinner:** Soya Chunks Curry OR Tofu Stir-fry with vegetables.")
            else:
                st.write("**Early Morning:** Apple Cider Vinegar in warm water.")
                st.write("**Breakfast:** 2 Egg Whites + Spinach OR Vegetable Oats.")
                st.write("**Mid-Morning:** 1 Fruit + Flax seeds.")
                st.write("**Lunch:** Grilled Chicken/Fish + small bowl Brown Rice + Salad.")
                st.write("**Evening:** Handful of Almonds OR Clear Chicken Soup.")
                st.write("**Dinner:** Baked Salmon OR Chicken Salad (No creamy dressings).")
        
        elif "Lactating" in st.session_state.stat:
            st.header("🤱 Detailed Lactation Diet Plan")
            [cite_start]st.info("A healthy lactation diet requires an additional 300–500 calories per day. [cite: 1]")
            if pref == "Vegetarian":
                [cite_start]st.write("**Early Morning:** Warm water with soaked fenugreek seeds or cumin water. [cite: 8]")
                [cite_start]st.write("**Breakfast:** Oats porridge with almonds/walnuts OR Ragi dosa OR Methi/Palak paratha with curd. [cite: 8]")
                [cite_start]st.write("**Mid-Morning:** 1 seasonal fruit (papaya/pomegranate) + soaked almonds and dates. [cite: 8]")
                [cite_start]st.write("**Lunch:** 2–3 Whole wheat rotis + 1 bowl Dal + Green leafy vegetable + Curd + Salad. [cite: 8]")
                [cite_start]st.write("**Evening:** Roasted Makhana OR Paneer tikka OR 1 Methi/Gond ladoo with milk. [cite: 8]")
                [cite_start]st.write("**Dinner:** Vegetable Khichdi with ghee OR Brown rice with mixed vegetable curry and dal. [cite: 8]")
            else:
                [cite_start]st.write("**Early Morning:** Fenugreek water OR Milk with soaked almonds. [cite: 11]")
                [cite_start]st.write("**Breakfast:** 2 Scrambled/Boiled eggs with whole-wheat toast OR Oats porridge with seeds/fruits. [cite: 11]")
                [cite_start]st.write("**Mid-Morning:** Fruit salad OR 1 bowl of sprouted moong chaat. [cite: 11]")
                [cite_start]st.write("**Lunch:** 2–3 Rotis or brown rice + Grilled/Curried Chicken or Fish + Spinach sabzi + Salad. [cite: 11]")
                [cite_start]st.write("**Evening:** Chicken/Lentil soup OR Handful of walnuts and raisins OR 1 Methi ladoo. [cite: 11]")
                [cite_start]st.write("**Dinner:** 2 Rotis + Fish curry (low mercury) OR Lean meat stir-fry with quinoa. [cite: 11]")
        
        else:
            st.header("🥗 Detailed Pregnancy Diet Chart")
            st.write("**Early Morning:** 5 Soaked Almonds + Warm Water.")
            st.write("**Breakfast:** Veggie Poha / Oats / Stuffed Paratha + 1 Bowl Curd.")
            st.write("**Mid-Morning:** 1 Fruit (Apple/Pomegranate) + Coconut Water.")
            if pref == "Non-Vegetarian":
                st.write("**Lunch:** 2 Roti + Chicken/Fish Curry + Bowl of Salad.")
                st.write("**Dinner:** Grilled Chicken / Egg Curry + 1 Roti + Steamed Veggies.")
            else:
                st.write("**Lunch:** 2 Roti + Dal Tadka + Seasonal Veggie + Salad.")
                st.write("**Dinner:** Paneer Bhurji / Dal + 1 Roti + Warm Milk.")

    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Specific Yoga")
            tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
            if "1st" in tri: st.write("✅ **1st:** Walking (20 mins), Gentle Yoga, Kegels.")
            elif "2nd" in tri: st.write("✅ **2nd:** Swimming, Wall Squats, Side-Lying Leg Lifts, Cat-Cow.")
            else: st.write("✅ **3rd:** Butterfly Stretch, Pelvic Tilts, Birthing Ball.")
        
        elif "Lactating" in st.session_state.stat:
            st.header("🧘 Detailed Postpartum Recovery & Exercise")
            [cite_start]st.info("Exercise is safe and beneficial for mental health and recovery. [cite: 17]")
            
            [cite_start]st.subheader("Phase-Wise Progression [cite: 18]")
            [cite_start]st.write("**Immediate Postpartum (Weeks 0–6):** [cite: 20]")
            [cite_start]st.write("- Walking: Start with 5-minute walks, building to 30 minutes. [cite: 21]")
            [cite_start]st.write("- Pelvic Floor (Kegels): 3 sets of 10 repetitions daily. [cite: 22, 23]")
            [cite_start]st.write("- Diaphragmatic Breathing: 'Belly breathing' to re-engage core. [cite: 24]")
            [cite_start]st.write("- Pelvic Tilts: Strengthens abdomen and relieves back pain. [cite: 25]")
            
            [cite_start]st.write("**Post-Checkup (Weeks 6–12):** [cite: 26]")
            [cite_start]st.write("- Low-Impact Cardio: Swimming (once bleeding stops), cycling, or elliptical. [cite: 27]")
            [cite_start]st.write("- Bodyweight Strength: Modified squats, lunges, and side planks. [cite: 28]")
            [cite_start]st.write("- Yoga & Pilates: 'Happy Baby' pose to relieve pelvic tension. [cite: 29]")
            
            [cite_start]st.write("**After 12 Weeks:** Gradual reintroduction of jogging or light weights once stable. [cite: 30, 31]")
            
            [cite_start]st.subheader("Guidelines for Breastfeeding Mothers [cite: 32]")
            [cite_start]st.write("- **Timing:** Exercise immediately *after* feeding to avoid discomfort from engorgement. [cite: 34]")
            [cite_start]st.write("- **Hydration:** Drink water before, during, and after exercise. [cite: 35]")
            [cite_start]st.write("- **Support:** Wear a professionally fitted, high-impact sports bra. [cite: 36]")
            [cite_start]st.write("- **Intensity:** Avoid maximal effort to prevent lactic acid buildup in milk. [cite: 37]")
            [cite_start]st.write("- **Hygiene:** Rinse breasts before feeding if you have sweated. [cite: 38]")
            
            [cite_start]st.warning("**When to Stop:** Consult a doctor if you feel faint, dizzy, or notice increased red vaginal bleeding. [cite: 39, 40, 41, 43]")

        else:
            st.header("🏋️ PCOS Strength Training")
            st.write("✅ **Strength:** Squats, Lunges, Planks (3x per week).")
            st.write("✅ **Cardio:** 45 mins Brisk walking daily.")

    elif m == "Health Vitals":
        st.header("📈 Health Vitals")
        c1, c2 = st.columns(2)
        with c1:
            h = st.number_input("Height (cm)", 100, 250, 160)
            w = st.number_input("Weight (kg)", 30, 200, 60)
        with c2:
            bp = st.text_input("Blood Pressure (e.g., 120/80)")
            pls = st.number_input("Pulse Rate (BPM)", 40, 200, 72)
        if st.button("Calculate & Save"):
            bmi = round(w/((h/100)**2), 1)
            st.success(f"Vitals Recorded: BMI {bmi}, BP {bp}, Pulse {pls}")

    elif m == "Vaccinations":
        if "Pregnant" in st.session_state.stat:
            st.header("💉 Pregnancy Vaccinations")
            st.info("Essential: 1. Tetanus (TT) | 2. Tdap | 3. Influenza (Flu)")
        else:
            st.header("💉 PCOS / Gynae Vaccination")
            st.info("Essential: HPV Vaccination (Cervical Cancer Prevention) - 3 Doses")
        with st.form("vac_form"):
            v_type = st.selectbox("Vaccine", ["Tetanus", "Tdap", "Influenza", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3", "Other"])
            v_date = st.date_input("Date")
            v_file = st.file_uploader("Upload Record Card", type=['jpg','png','jpeg'])
            if st.form_submit_button("Save"): st.success("Record saved!")

    elif m == "Book Appointment":
        st.header("📅 15-Minute Slots")
        dt = st.date_input("Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Clinic Closed on Sundays")
        else:
            slots = [f"{h:02d}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]] + [f"{h-12:02d}:{m:02d} PM" for h in [18, 19, 20] for m in [0, 15, 30, 45]]
            tm = st.selectbox("Select Time", slots)
            if st.button("Confirm Booking"): st.success(f"Confirmed for {dt} at {tm}")
