import streamlit as st
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; }
    .diet-box { background:#fff5f7; padding:15px; border-radius:10px; border:1px solid #ffc0cb; color:#333; margin-bottom:10px; }
    .badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><p>Dr. Priyanka Gupta - MS (Obs & Gynae)</p>
    <div><span class='badge'>Infertility Specialist</span><span class='badge'>Ultrasound</span><span class='badge'>Laparoscopy</span><span class='badge'>Pharmacy</span></div></div>""", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Access"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Name")
            a = st.number_input("Age", 18, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae", "Lactating Mother"])
            if st.form_submit_button("Enter"):
                if n: st.session_state.update({"logged_in":True,"name":n,"age":a,"stat":s,"role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.text_input("Password", type="password") == "clinicadmin786" and st.form_submit_button("Login"):
                st.session_state.update({"logged_in":True,"role":"D","name":"Dr. Priyanka"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    st.sidebar.markdown(f"### 👤 {st.session_state.name}")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    m = st.sidebar.radio("Nav", ["Tracker", "Diet Plans", "Exercise", "Vitals", "Vaccinations", "Booking"])

    if m == "Tracker":
        if "Pregnant" in st.session_state.stat:
            lmp = st.date_input("LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | Week: {wks}")
        elif "Lactating" in st.session_state.stat:
            st.info("Focus on 8-12 glasses of water daily [cite: 3] and galactagogues like fenugreek and cumin[cite: 4].")
        else:
            lp = st.date_input("Last Period", value=date.today()-timedelta(days=14))
            st.success(f"Next Period: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    elif m == "Diet Plans":
        pref = st.radio("Type", ["Vegetarian", "Non-Vegetarian"])
        if "Lactating" in st.session_state.stat:
            st.info("Goal: +300-500 extra calories daily[cite: 1]. Eat 3 meals and 2-3 snacks[cite: 5].")
            if pref == "Vegetarian":
                st.markdown("<div class='diet-box'><b>Morning:</b> Fenugreek/Cumin water </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Oats porridge / Ragi dosa / Methi paratha </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> Roti, Moong/Masoor Dal, Green Veg, Curd </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Veg Khichdi with ghee / Brown rice with veg curry </div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='diet-box'><b>Morning:</b> Fenugreek water or Milk with almonds </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> 2 Eggs with toast / Oats with seeds </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> Roti/Brown rice + Chicken or Fish + Spinach </div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Fish curry or Lean meat stir-fry </div>", unsafe_allow_html=True)
        elif "PCOS" in st.session_state.stat:
            st.markdown("<div class='diet-box'><b>PCOS Diet:</b> Low GI foods. Missi Roti, Dal, Sprouted Salad. No sugar.</div>", unsafe_allow_html=True)

    elif m == "Exercise":
        if "Pregnant" in st.session_state.stat:
            tri = st.selectbox("Trimester", ["1st", "2nd", "3rd"])
            if "1st" in tri: st.write("✅ Walking, Prenatal Yoga, Kegels")
            elif "2nd" in tri: st.write("✅ Swimming, Wall Squats, Cat-Cow stretch")
            else: st.write("✅ Butterfly stretch, Pelvic tilts, Birthing Ball")
        else:
            st.write("✅ **PCOS:** Strength (Squats/Planks) 3x/week. 45m Brisk Walk daily.")

    elif m == "Vitals":
        h, w = st.number_input("Ht (cm)", 100, 250, 160), st.number_input("Wt (kg)", 30, 200, 60)
        bp, pls = st.text_input("BP (120/80)"), st.number_input("Pulse", 40, 200, 72)
        if st.button("Save"):
            bmi = round(w/((h/100)**2), 1)
            st.success(f"BMI: {bmi} | BP: {bp} | Pulse: {pls}")

    elif m == "Vaccinations":
        if "Pregnant" in st.session_state.stat:
            st.info("Essential: 1. Tetanus (TT), 2. Tdap, 3. Influenza (Flu)")
        else:
            st.info("Essential: HPV Vaccination (3 Doses schedule)")
        with st.form("v"):
            st.selectbox("Type", ["Tetanus", "Tdap", "Flu", "HPV Dose 1", "HPV Dose 2", "HPV Dose 3"])
            st.file_uploader("Upload Card")
            st.form_submit_button("Save")

    elif m == "Booking":
        dt = st.date_input("Date", min_value=date.today())
        if dt.weekday() == 6: st.error("Closed on Sundays")
        else:
            slots = [f"{h}:{m:02d} AM" for h in range(11,14) for m in [0,15,30,45]] + [f"{h-12}:{m:02d} PM" for h in range(18,21) for m in [0,15,30,45]]
            st.selectbox("Slot", slots)
            if st.button("Confirm"): st.success("Requested")
