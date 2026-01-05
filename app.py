import streamlit as st
from datetime import datetime, date, timedelta

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; margin-bottom:20px; }
    .diet-box { background:#fff5f7; padding:15px; border-radius:10px; border:1px solid #ffc0cb; color:#333; margin-bottom:10px; }
    .clinic-badge { background:#e8f4f8; color:#003366; padding:5px 10px; border-radius:5px; font-weight:bold; display:inline-block; margin:2px; font-size:11px; border:1px solid #003366; }
    .stButton>button { background:#ff4b6b; color:white; border-radius:10px; font-weight:bold; width:100%; }
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
    
    # 3.1 TRACKER (RESTORED WEEK-BY-WEEK)
    if m == "Health Tracker":
        if "Pregnant" in st.session_state.stat:
            st.header("🤰 Pregnancy Week-by-Week Development")
            lmp = st.date_input("Select LMP Date", value=date.today()-timedelta(days=70))
            wks = (date.today()-lmp).days // 7
            st.success(f"🗓️ EDD: {(lmp+timedelta(days=280)).strftime('%d %b %Y')} | ⏳ Current Week: {wks}")
            
            if wks <= 4: st.info("🌱 Week 4: Size of a poppy seed. Implantation happens.")
            elif wks <= 8: st.info("🍇 Week 8: Size of a raspberry. All major organs starting to form.")
            elif wks <= 12: st.info("🍋 Week 12: Size of a lime. Baby starts moving fingers and toes.")
            elif wks <= 16: st.info("🥑 Week 16: Size of an avocado. Baby can make a fist.")
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. Halfway! You feel the first kicks.")
            elif wks <= 24: st.info("🌽 Week 24: Size of corn. Lungs are developing.")
            elif wks <= 30: st.info("🥦 Week 30: Size of a cabbage. Baby can open eyes.")
            elif wks <= 36: st.info("🥬 Week 36: Size of a romaine lettuce. Preparing for birth.")
            else: st.info("🍉 Week 40: Full term. Ready to meet the world!")
        else:
            st.header("🗓️ Period Tracker")
            lp = st.date_input("Last Period Start", value=date.today()-timedelta(days=14))
            st.success(f"🩸 Next Expected: {(lp+timedelta(days=28)).strftime('%d %b %Y')}")

    # 3.2 DETAILED DIET PLANS
    elif m == "Diet Plans":
        pref = st.radio("Diet Preference", ["Vegetarian", "Non-Vegetarian"])
        if "Lactating" in st.session_state.stat:
            st.header("🤱 Lactation Diet Plan (+500 Calories)")
            if pref == "Vegetarian":
                st.markdown("<div class='diet-box'><b>Early Morning:</b> Soaked fenugreek seeds or cumin water.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> Ragi dosa OR Oats porridge with nuts.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2-3 Rotis, Dal, Green leafy veggies, Curd, Salad.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Evening:</b> Roasted Makhana OR Methi/Gond ladoo with milk.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Veg Khichdi with ghee OR Brown rice with veg curry.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='diet-box'><b>Early Morning:</b> Fenugreek water OR Milk with almonds.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Breakfast:</b> 2 Scrambled/Boiled eggs with toast.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Lunch:</b> Grilled Chicken/Fish (Salmon) + brown rice + Spinach.</div>", unsafe_allow_html=True)
                st.markdown("<div class='diet-box'><b>Dinner:</b> Fish curry OR Lean meat stir-fry with quinoa.</div>", unsafe_allow_html=True)
        
        elif "Pregnant" in st.session_state.stat:
            st.header("🥗 Pregnancy Full Diet Chart")
            st.markdown("<div class='diet-box'><b>Morning:</b> 5 Soaked Almonds + Warm Water.</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Breakfast:</b> Veggie Poha / Oats / Stuffed Paratha + 1 Bowl Curd.</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Mid-Morning:</b> 1 Fruit + Coconut Water.</div>", unsafe_allow_html=True)
            if pref == "Non-Vegetarian":
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Chicken/Fish Curry + Salad.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Roti + Dal Tadka + Seasonal Veggie + Curd.</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Dinner:</b> 1 Roti + Paneer Curry / Dal / Egg + Milk.</div>", unsafe_allow_html=True)
        
        else:
            st.header("🌸 Detailed PCOS Nutrition")
            st.markdown("<div class='diet-box'><b>Breakfast:</b> Sprouted Salad / Veg Dalia / Vegetable Oats (No sugar).</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Lunch:</b> 2 Missi Roti + 1 Bowl Dal + Green Veggie + Salad.</div>", unsafe_allow_html=True)
            st.markdown("<div class='diet-box'><b>Dinner:</b> Clear Soup + Tofu / Grilled Veggies. Walk 15 mins after.</div>", unsafe_allow_html=True)

    # 3.3 EXERCISE (ALL TRIMESTERS RESTORED)
    elif m == "Exercise & Yoga":
        if "Pregnant" in st.session_state.stat:
            st.header("🧘 Trimester-Specific Yoga")
            tri = st.selectbox
