import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# --- 1. CONFIG & UI STYLING ---
st.set_page_config(page_title="Bhavya Labs", layout="wide", initial_sidebar_state="expanded")

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
for key in ['logged_in', 'labs', 'vitals', 'apts', 'blocked']:
    if key not in st.session_state: st.session_state[key] = False if key == 'logged_in' else []
if 'social' not in st.session_state: st.session_state.social = {"yt": "", "ig": ""}

# --- 2. LOGIN & BRANDING ---
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

# --- 3. PATIENT PORTAL ---
elif st.session_state.role == "P":
    head_l, head_r = st.columns([3, 1])
    with head_l:
        st.markdown(f"### 📋 Patient: {st.session_state.name} ({st.session_state.age} yrs)")
        st.caption(f"Status: {st.session_state.stat}")
    with head_r:
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

    m = st.segmented_control(
        "SELECT VIEW", 
        options=["Health Tracker", "Diet Plans", "Exercise", "Lab Reports", "Vitals", "Social", "Book Slot"],
        default="Health Tracker"
    )
    st.divider()

    if m == "Health Tracker":
        if st.session_state.stat == "Pregnant":
            st.header("🤰 Pregnancy Milestone Tracker")
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            edd = (lmp + timedelta(days=280)).strftime('%d %b %Y')
            st.success(f"🗓️ Estimated Due Date: {edd} | Current Week: {wks}")
            weeks_info = {4: "🌱 Implantation stage.", 12: "🍋 End of 1st Trimester.", 20: "🍌 Halfway point!", 28: "🍆 3rd Trimester begins.", 40: "🍉 Full term."}
            st.info(weeks_info.get(wks, "🍉 Your baby is growing beautifully every single day!"))
        
        elif st.session_state.stat == "Lactating Mother":
            st.header("📋 Health Progress & Family Planning")
            st.info("### 🛡️ Postpartum Contraception Options")
            st.write("As a lactating mother, spacing your next pregnancy is vital. Discuss these options with Dr. Priyanka Gupta:")
            
            exp1 = st.expander("View Contraceptive Methods")
            with exp1:
                st.markdown("""
                * **OCPs (Oral Contraceptive Pills):** Progestogen-only pills (Mini-pills) are preferred during breastfeeding.
                * **Copper T (IUCD):** Long-term reversible protection, can be inserted post-delivery.
                * **DMPA Injection:** 3-monthly hormonal injection for highly effective prevention.
                * **Family Planning Operation:** Permanent tubal ligation for those who have completed their family.
                * **Barrier Methods:** Condoms are safe and do not affect milk supply.
                """)
            st.warning("Note: Avoid combined estrogen pills in the first 6 months of breastfeeding as they may reduce milk supply.")
        
        else:
            st.header("📋 Health Progress")
            st.info("Log your daily vitals and reports to see your health trends.")

    elif m == "Diet Plans":
        st.header(f"🥗 Clinical Diet Chart: {st.session_state.stat}")
        if st.session_state.stat == "Pregnant":
            t1, t2, t3 = st.tabs(["Trimester 1", "Trimester 2", "Trimester 3"])
            with t1: st.markdown("<div class='diet-card'><b>T1 Focus: Folic Acid.</b><br>• Early Morning: 5 Almonds + 2 Walnuts.<br>• Breakfast: Poha/Oats/Dal Chilla.<br>• Lunch: 2 Roti, Dal, Green Sabzi, Fresh Curd.</div>", unsafe_allow_html=True)
            with t2: st.markdown("<div class='diet-card'><b>T2 Focus: Iron & Calcium.</b><br>• Coconut Water & Fresh Fruits daily.<br>• Include Spinach, Paneer, and Sprouted salads.</div>", unsafe_allow_html=True)
            with t3: st.markdown("<div class='diet-card'><b>T3 Focus: Energy & Digestion.</b><br>• Eat 6 small meals instead of 3 large ones.<br>• Bedtime Milk with 2 Dates. Stay hydrated.</div>", unsafe_allow_html=True)
        
        elif st.session_state.stat == "PCOS/Gynae":
            # --- Menstrual Cycle Calculator ---
            st.subheader("📅 Menstrual Cycle Regulator")
            c1, c2 = st.columns(2)
            with c1:
                last_p = st.date_input("First Day of Last Period", value=date.today()-timedelta(days=28))
            with c2:
                cycle_len = st.number_input("Average Cycle Length (Days)", 21, 45, 28)
            
            next_p = last_p + timedelta(days=cycle_len)
            ovulation = last_p + timedelta(days=cycle_len - 14)
            st.success(f"**Expected Next Period:** {next_p.strftime('%d %b %Y')} | **Estimated Ovulation:** {ovulation.strftime('%d %b %Y')}")
            
            # --- Detailed Diet Chart from Documents ---
            st.markdown("### 🥗 PCOS Clinical Diet Principles (2026) ")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Core Goals:**")
                st.write("• **Protein:** 50–60g daily ")
                st.write("• **Fiber:** At least 25g daily ")
                st.write("• **Dairy:** Limit to 1–2 servings (Low-fat) [cite: 3, 4]")
            with col_b:
                st.write("**Foods to Avoid[cite: 10]:**")
                st.write("• Refined Carbs (White Rice/Maida) [cite: 11]")
                st.write("• Sugary Items & Sodas [cite: 12]")
                st.write("• Starchy Veggies (Potato/Corn) [cite: 14]")

            vt, nvt = st.tabs(["Vegetarian Plan [cite: 6]", "Non-Vegetarian Plan [cite: 8]"])
            with vt:
                st.markdown("""
                | Meal | Food Item | Notes [cite: 7] |
                | :--- | :--- | :--- |
                | **Early Morning** | Warm lemon water + 5 soaked almonds | Or methi water |
                | **Breakfast** | Moong dal chilla OR Veg Upma | High protein & fiber |
                | **Lunch** | 2 Jowar/Bajra rotis + Dal + Salad | Use millets |
                | **Evening** | Roasted makhana OR Walnuts | Avoid biscuits |
                | **Dinner** | Tofu/Paneer stir-fry with veggies | Light digestion |
                """)
            with nvt:
                st.markdown("""
                | Meal | Food Item | Notes [cite: 9] |
                | :--- | :--- | :--- |
                | **Early Morning** | Warm water + soaked chia seeds | Metabolism kickstart |
                | **Breakfast** | 2 Boiled egg whites + grain toast | Protein stabilizes sugar |
                | **Lunch** | Grilled chicken/Fish + Brown rice | Fatty fish 2x weekly |
                | **Dinner** | Grilled fish + Mediterranean veggies | Avoid heavy curries |
                | **Bedtime** | Cinnamon-infused warm water | Improves lipid profile |
                """)
        
        else: # Lactation Diet
            st.markdown("<div class='diet-card'><b>Lactation Boosters:</b><br>• Soaked Methi seeds, Jeera-water.<br>• Garlic, Gond Ladoo, Shatavari granules with milk.<br>• Minimum 4 Liters of fluids daily for milk supply.</div>", unsafe_allow_html=True)

    elif m == "Exercise":
        st.header("🧘 Therapeutic Movement")
        st.write("1. **Baddha Konasana (Butterfly Pose):** Pelvic flexibility.")
        st.write("2. **Marjaryasana (Cat-Cow Stretch):** Relief for back strain.")
        st.write("3. **Walking:** 20-30 mins daily walking.")

    elif m == "Lab Reports":
        st.header("📊 Lab Tracking")
        with st.form("lab_form"):
            hb = st.number_input("Hemoglobin (g/dL)", 5.0, 18.0, 12.0)
            sugar = st.number_input("Blood Sugar (mg/dL)", 50, 400, 90)
            tsh = st.number_input("Thyroid TSH (mIU/L)", 0.0, 50.0, 2.5)
            urine = st.selectbox("Urine Test", ["Normal", "Trace", "+1", "+2"])
            if st.form_submit_button("Save Report"):
                st.session_state.labs.append({"User": st.session_state.name, "Date": date.today(), "Hb": hb, "Sugar": sugar, "TSH": tsh, "Urine": urine})
                st.rerun()
        df = pd.DataFrame([r for r in st.session_state.labs if r['User'] == st.session_state.name])
        if not df.empty:
            st.line_chart(df.set_index('Date')[['Hb', 'Sugar', 'TSH']])

    elif m == "Vitals":
        st.header("📈 Vitals & BMI")
        with st.form("vital_form"):
            p, bp = st.number_input("Pulse Rate", 40, 150, 72), st.text_input("Blood Pressure", "120/80")
            wt, ht = st.number_input("Weight (kg)", 30.0, 150.0, 60.0), st.number_input("Height (cm)", 100.0, 220.0, 160.0)
            if st.form_submit_button("Update Vitals"):
                bmi = round(wt / ((ht/100)**2), 2)
                st.session_state.vitals.append({"User": st.session_state.name, "Date": date.today(), "BMI": bmi, "Pulse": p, "BP": bp})
                st.rerun()

    elif m == "Social":
        st.header("📺 Health Feed")
        if st.session_state.social["yt"]: st.video(st.session_state.social["yt"])
        if st.session_state.social["ig"]: st.info(f"Latest Update: {st.session_state.social['ig']}")

    elif m == "Book Slot":
        st.header("📅 Select Time Slot")
        slots = [f"{h}:{m:02d} AM" for h in [11] for m in [15, 30, 45]] + [f"{h}:{m:02d} PM" for h in [12, 1, 6, 7] for m in [0, 15, 30, 45]]
        d = st.date_input("Date", min_value=date.today())
        t = st.selectbox("Slot", slots)
        if st.button("Request Booking"):
            if d in st.session_state.blocked: st.error("Clinic Closed on this date.")
            else:
                st.session_state.apts.append({"Patient": st.session_state.name, "Date": d, "Time": t})
                st.success("Booking Request Sent!")

# --- 4. ADMIN PORTAL ---
elif st.session_state.role == "D":
    adm_l, adm_r = st.columns([3, 1])
    with adm_l:
        st.title("👩‍⚕️ Admin Master")
    with adm_r:
        if st.button("Log Out", key="admin_logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()

    t1, t2, t3, t4 = st.tabs(["Appointments", "Patient Records", "Clinic Availability", "Social Media"])
    
    with t1:
        if st.session_state.apts:
            st.table(pd.DataFrame(st.session_state.apts))
        else:
            st.info("No Bookings available.")

    with t2:
        if st.session_state.labs:
            st.subheader("Lab Data")
            st.dataframe(pd.DataFrame(st.session_state.labs))
        if st.session_state.vitals:
            st.subheader("Vitals Data")
            st.dataframe(pd.DataFrame(st.session_state.vitals))
        if not st.session_state.labs and not st.session_state.vitals:
            st.info("No records found.")

    with t3:
        bd = st.date_input("Block a date")
        if st.button("Mark Clinic Closed"):
            st.session_state.blocked.append(bd)
            st.success(f"{bd} Blocked")
        st.write("Current Blocked Dates:", st.session_state.blocked)

    with t4:
        with st.form("social_form"):
            yt_link = st.text_input("YouTube URL", value=st.session_state.social["yt"])
            ig_link = st.text_input("Instagram URL", value=st.session_state.social["ig"])
            if st.form_submit_button("Save Feed Updates"):
                st.session_state.social.update({"yt": yt_link, "ig": ig_link})
                st.success("Social Feed Updated!")
