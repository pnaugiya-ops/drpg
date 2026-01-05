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
            elif wks <= 20: st.info("🍌 Week 20: Size of a banana. You feel kicks.")
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
            if pref == "Vegetarian":
                st.write("**Early Morning:** Warm water with soaked fenugreek seeds.")
                st.write("**Breakfast:** Oats porridge with nuts OR Ragi dosa with chutney.")
                st.write("**Mid-Morning:** 1 seasonal fruit + handful of soaked almonds.")
                st.write("**Lunch:** 2-3 Rotis, 1 bowl Dal, Green leafy vegetables, Curd, Salad.")
                st.write("**Evening:** Roasted Makhana OR Methi/Gond ladoo with milk.")
                st.write("**Dinner:** Vegetable Khichdi with ghee OR Brown rice with mixed veg curry.")
            else:
                st.write("**Early Morning:** Fenugreek water OR Milk with soaked almonds.")
                st.write("**Breakfast:** 2 Scrambled/Boiled eggs with whole-wheat toast.")
                st.write("**Mid-Morning:** Fruit salad OR 1 bowl of sprouted moong.")
                st.write("**Lunch:** Grilled/Curried Chicken or Fish + Brown Rice + Spinach.")
                st.write("**Evening:** Chicken/Lentil soup OR 1 Methi ladoo.")
                st.write("**Dinner:** Fish curry (low mercury) OR Lean meat stir-fry with quinoa.")
        
        else:
            st.header("🥗 Detailed Pregnancy Diet Chart")
            st.write("**Early Morning:** 5 Soaked Almonds + Warm Water.")
            st.write("**Breakfast:** Veggie Poha / Oats / Stuffed Paratha + 1 Bowl Curd.")
            st.write("**Mid-Morning:** 1 Fruit (Apple/Pomegranate) + Coconut Water.")
            if pref == "Non-Vegetarian":
                st.write("**Lunch:** 2 Roti + Chicken/Fish Curry + Bowl of Salad.")
                st.write("**Dinner:** Grilled Chicken / Egg Curry + 1 Roti + Steamed Veggies.")
            else:
                st.write("**
