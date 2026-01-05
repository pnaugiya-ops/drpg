import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:10px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 15px; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    .clinic-badge { background: #e8f4f8; color: #003366; padding: 5px 10px; border-radius: 5px; font-weight: bold; display: inline-block; margin: 5px; font-size: 12px; border: 1px solid #003366; }
    </style>
    """, unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Database Connection Error: {e}")

if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

# --- HELPERS ---
def process_img(f):
    if not f: return ""
    try:
        img = Image.open(f)
        img.thumbnail((500, 500))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=40)
        return base64.b64encode(buf.getvalue()).decode()
    except: return ""

def show_img(b):
    if b: st.image(io.BytesIO(base64.b64decode(b)), use_container_width=True)

# --- 2. LOGIN & CLINIC INFO ---
if not st.session_state.logged_in:
    st.markdown("""<div class='dr-header'>
        <h1>BHAVYA LABS & CLINICS</h1>
        <h3>Dr. Priyanka Gupta</h3>
        <p>MS (Obs & Gynae)</p>
        <div style='margin-top:10px;'>
            <span class='clinic-badge'>Infertility Specialist</span>
            <span class='clinic-badge'>Ultrasound</span>
            <span class='clinic-badge'>Laparoscopic Surgery</span>
            <span class='clinic-badge'>Pharmacy</span>
            <span class='clinic-badge'>Thyrocare Blood Test</span>
        </div>
    </div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            n = st.text_input("Full Name")
            age = st.number_input("Age", 1, 100, 25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter Portal"):
                if n:
                    st.session_state.update({"logged_in":True, "name":n, "age":age, "stat":s, "role":"P"})
                    st.rerun()
                else: st.warning("Please enter your name")
    with t2:
        with st.form("d_login"):
            pass_in = st.text_input("Clinic Password", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()
                else: st.error("Access Denied")

# --- 3. MAIN APP ---
else:
    try:
        df = conn.read(ttl=0)
        if df is not None and not df.empty:
            df['Name'] = df['Name'].fillna('').astype(str)
            df['Type'] = df['Type'].fillna('').astype(str)
        else:
            df = pd.DataFrame(columns=["Name", "Type", "Details", "Attachment", "Timestamp"])
    except:
        df = pd.DataFrame(columns=["Name", "Type", "Details", "Attachment", "Timestamp"])
    
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        st.sidebar.info("🕒 **Clinic Timings:**\n- 11:00 AM - 02:00 PM\n- 06:00 PM - 08:00 PM\n*(Closed on Sundays)*")
        
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals", "📢 Broadcast", "📅 Availability"])
        
        with t_adm[0]:
            apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().str.contains(search))]
            for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)
        
        with t_adm[1]:
            reps = df[(df['Type'] == 'REPORT') & (df['Name'].str.lower().str.contains(search))]
            for _, row in reps.iterrows():
                with st.expander(f"Report: {row['Name']}"):
                    st.write(f"Note: {row['Details']}")
                    show_img(row['Attachment'])

        with t_adm[2]:
            st.dataframe(df[df['Type'] == 'VITALS'], use_container_width=True)

        with t_adm[3]:
            with st.form("b_form"):
                bt = st.text_input("Title")
                bl = st.text_input("Link")
                if st.form_submit_button("Post Update"):
                    new = pd.DataFrame([{"Name":"DR","Type":"BROADCAST","Details":f"{bt}|{bl}","Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()

        with t_adm[4]:
            block_dt = st.date_input("Block Date", min_value=date.today())
            if st.button("Confirm Block"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now()}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()
            
        if st.sidebar.button("Logout", key="dr_logout"): 
            st.session_state.logged_in = False
            st.rerun()

    else: # Patient View
        st.sidebar.markdown(f"### Hello, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Diet & Yoga", "Vaccine & Screening Portal", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        if m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness Hub")
                
                tab_diet, tab_exercise = st.tabs(["🥗 Nutrition Plan", "🧘 Trimester Exercises"])
                
                with tab_diet:
                    st.markdown("""<div class='diet-box'>
                    <b>General Safety:</b><br>
                    - 🥛 <b>Milk:</b> 3–4 servings daily[cite: 4].<br>
                    - 💧 <b>Hydration:</b> 2.5–3 Liters of water daily[cite: 19].<br>
                    - ☕ <b>Caffeine:</b> Limit to < 200mg/day[cite: 18].
                    </div>""", unsafe_allow_html=True)
                    
                    tri = st.selectbox("Select Trimester (Nutrition)", ["1st Trimester (Weeks 1-12)", "2nd Trimester (Weeks 13-26)", "3rd Trimester (Weeks 27-40)"])
                    
                    if "1st" in tri:
                        st.success("**Focus:** Folic acid & Vitamin B6[cite: 8].")
                        st.write("**Early Morning:** Warm water + 4–5 soaked almonds[cite: 9].")
                        st.write("**Breakfast:** Veggie Poha/Upma + milk OR Whole grain toast + 2 eggs[cite: 9].")
                    elif "2nd" in tri:
                        st.success("**Focus:** Calcium & Iron[cite: 11].")
                        st.write("**Breakfast:** Veg paratha + curd OR Oats porridge[cite: 12].")
                        st.write("**Lunch:** Brown rice + dal + mixed veggies OR Chicken curry[cite: 12].")
                    elif "3rd" in tri:
                        st.success("**Focus:** High Fiber & Healthy Fats[cite: 14].")
                        st.write("**Breakfast:** Besan chilla + mint chutney OR Oats + 2 eggs[cite: 15].")
                        st.write("**Lunch:** Millet khichdi + dal + salad OR Grilled salmon + rice[cite: 15].")

                with tab_exercise:
                    tri_ex = st.selectbox("Select Trimester (Exercises)", ["1st Trimester: Gentle Adaptation", "2nd Trimester: Building Strength", "3rd Trimester: Mobility & Labor Prep"])
                    
                    if "1st" in tri_ex:
                        st.info("**Focus:** Managing fatigue and morning sickness with low-impact movements[cite: 36].")
                        st.write("- **Walking:** Improves circulation and mood[cite: 37].")
                        st.write("- **Prenatal Yoga:** Stretching and breath awareness[cite: 38].")
                        st.write("- **Kegels:** Strengthens pelvic floor[cite: 39].")
                        st.write("- **Cat-Cow Stretch:** Relieves lower back tension[cite: 40].")
                    elif "2nd" in tri_ex:
                        st.info("**Focus:** Moderate resistance and balance training[cite: 43].")
                        st.write("- **Swimming:** Reduces joint pressure and prevents overheating[cite: 44].")
                        st.write("- **Stationary Cycling:** Safer than outdoor biking to avoid falls[cite: 45].")
                        st.write("- **Side-Lying Leg Lifts:** Strengthens hip stabilizers[cite: 46].")
                        st.write("- **Wall Squats:** Prepares thighs for delivery[cite: 47].")
                        st.warning("**Note:** Avoid lying flat on your back for more than a few minutes.")
                    elif "3rd" in tri_ex:
                        st.info("**Focus:** Flexibility, pelvic opening, and relaxation[cite: 51].")
                        st.write("- **Butterfly Stretch:** Opens hips and inner thighs.")
                        st.write("- **Deep Supported Squats:** Encourages optimal baby positioning[cite: 53].")
                        st.write("- **Birthing Ball Exercises:** Gently rocking to keep hips fluid[cite: 55].")
                        st.write("- **Diaphragmatic Breathing:** Critical tool for labor pain management.")
                    
                    st.markdown("""<div class='diet-box'>
                    <b>⚠️ Exercise Safety (2026):</b><br>
                    - <b>Talk Test:</b> You should be able to hold a conversation while exercising.<br>
                    - <b>Hydration:</b> Drink water before, during, and after every session[cite: 59].<br>
                    - <b>Avoid Risks:</b> No contact sports, jumping, or heavy lifting[cite: 60].<br>
                    - <b>Consultation:</b> Always get medical clearance before starting a new routine[cite: 61].
                    </div>""", unsafe_allow_html=True)
            else:
                st.header("🥗 Core PCOS Dietary Principles")
                st.markdown("""<div class='diet-box'>
                - <b>Protein:</b> 50–60g daily. <b>Fiber:</b> >25g daily.<br>
                - <b>Dairy:</b> 1–2 servings (Limit full-fat).<br>
                - <b>Avoid:</b> Maida, Sugary sodas, Fried/Processed meats.
                </div>""", unsafe_allow_html=True)
                p_type = st.radio("Diet Type", ["Vegetarian", "Non-Vegetarian"])
                if p_type == "Vegetarian":
                    st.info("**Breakfast:** Moong dal chilla. **Lunch:** Jowar rotis + veg + dal.")
                else:
                    st.info("**Breakfast:** 2 Boiled egg whites + toast. **Lunch:** Grilled chicken + brown rice.")

        elif m == "Vaccine & Screening Portal":
            st.header("💉 Preventive Care")
            if "Pregnant" in st.session_state.stat:
                st.info("**Maternal Vaccines:** Tetanus (TT), T-Dap (Weeks 27-36), and Seasonal Flu shots.")
            else:
                st.info("**Gynae Wellness:** HPV Vaccine (3 doses) and Pap Smear screening (Every 3 years).")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160); wi = st.number_input("Weight (kg)", 30, 200, 60)
                bp = st.text_input("BP Reading", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":f"BMI:{bmi}, BP:{bp}","Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"BMI: {bmi}")

        elif m == "Book Appointment":
            st.write("🕒 **Hours:** 11:00 AM - 02:00 PM & 06:00 PM - 08:00 PM")
            sel_dt = st.date_input("Date", min_value=date.today())
            if str(sel_dt) in blocked_dates or sel_dt.weekday() == 6: st.error("Clinic Closed")
            else:
                with st.form("b_form"):
                    morning = [f"{h}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]]
                    evening = [f"{h}:{m:02d} PM" for h in [6, 7] for m in [0, 15, 30, 45]]
                    tm = st.selectbox("Slot", morning + evening)
                    if st.form_submit_button("Book"):
                        new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now()}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Confirmed!")

        elif m == "Upload Reports":
            with st.form("u_form"):
                f = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg']); n = st.text_input("Note")
                if st.form_submit_button("Send"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"REPORT","Details":n,"Attachment":b64,"Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")

        if st.sidebar.button("Logout", key="pt_logout"): 
            st.session_state.logged_in = False
            st.rerun()
