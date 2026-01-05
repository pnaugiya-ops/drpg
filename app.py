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
        # --- RESTORED CLINIC TIMINGS IN DASHBOARD ---
        st.sidebar.info("""🕒 **Clinic Timings:**
        - Morning: 11:00 AM - 02:00 PM
        - Evening: 06:00 PM - 08:00 PM
        *(Closed on Sundays)*""")
        
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals", "📢 Broadcast Content", "📅 Availability"])
        
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
                bl = st.text_input("YouTube/Instagram Link")
                if st.form_submit_button("Post Update"):
                    new = pd.DataFrame([{"Name":"DR","Type":"BROADCAST","Details":f"{bt}|{bl}","Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()

        with t_adm[4]:
            block_dt = st.date_input("Block Date", min_value=date.today())
            if st.button("Confirm Block"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now()}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()
            
        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()

    else: # Patient View
        st.sidebar.markdown(f"### Hello, {st.session_state.name}")
        # --- RESTORED ALL SECTIONS: VACCINE PORTAL INCLUDED ---
        m = st.sidebar.radio("Menu", ["Diet & Yoga", "Vaccine & Screening Portal", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        if m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🥗 Pregnancy Nutritional Plan")
                diet_sum = "Avoid raw meat/eggs, unpasteurized dairy. Hydration: 2.5–3L water. Caffeine: <200mg/day."
                st.markdown(f"<div class='diet-box'>{diet_sum}</div>", unsafe_allow_html=True)
                tri = st.selectbox("Select Trimester", ["First (Weeks 1–12)", "Second (Weeks 13–26)", "Third (Weeks 27–40)"])
                if "First" in tri: st.write("**Focus:** Folic acid & B6. **Breakfast:** Veggie Poha + milk.")
                elif "Second" in tri: st.write("**Focus:** Calcium & Iron. **Lunch:** Dal + Brown rice + Sabzi.")
                elif "Third" in tri: st.write("**Focus:** Fiber & Healthy Fats. **Dinner:** Chapati + Rajma.")
            else:
                # --- NEW PCOS DIET INTEGRATION ---
                st.header("🥗 Core PCOS Dietary Principles (2026)")
                st.markdown("""<div class='diet-box'>
                - <b>Protein:</b> Aim for 50–60g daily.<br>
                - <b>Dairy:</b> Limit to 1–2 servings (Full-fat may worsen acne).<br>
                - <b>Fiber:</b> At least 25g daily from whole grains & non-starchy veg.<br>
                - <b>Avoid:</b> Refined carbs (Maida), Sugary sodas, and Fried foods.
                </div>""", unsafe_allow_html=True)
                
                diet_type = st.radio("Choose Diet Chart", ["Vegetarian", "Non-Vegetarian"])
                if diet_type == "Vegetarian":
                    st.info("**Breakfast:** Moong dal chilla with mint chutney.")
                    st.info("**Lunch:** 2 Jowar/Bajra rotis + mixed veg curry + dal + salad.")
                    st.info("**Dinner:** Tofu/Paneer stir-fry or Veg khichdi (Lighter).")
                else:
                    st.info("**Breakfast:** 2 Boiled egg whites + whole grain toast.")
                    st.info("**Lunch:** Grilled chicken/Fish + brown rice + green sabzi.")
                    st.info("**Dinner:** Grilled fish or chicken + sautéed Mediterranean veggies.")

        elif m == "Vaccine & Screening Portal":
            st.header("💉 Preventive Care & Vaccines")
            if "Pregnant" in st.session_state.stat:
                st.subheader("Maternal Vaccines")
                st.info("- **Tetanus Toxoid (TT):** On confirmation.\n- **T-Dap:** Between 27-36 weeks.\n- **Flu Vaccine:** Recommended during season.")
            else:
                st.subheader("Gynae Screening & Vaccines")
                st.info("- **HPV Vaccine:** For cervical cancer prevention (3 doses).\n- **Pap Smear:** Every 3 years as per guidelines.")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160)
                wi = st.number_input("Weight (kg)", 30, 200, 60)
                bp = st.text_input("BP Reading", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":f"BMI:{bmi}, BP:{bp}","Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"Saved! BMI: {bmi}")

        elif m == "Book Appointment":
            # --- RESTORED 15-MIN SLOTS & TIMINGS ---
            st.write("🕒 **Clinic Hours:** 11:00 AM - 02:00 PM & 06:00 PM - 08:00 PM")
            sel_dt = st.date_input("Select Date", min_value=date.today())
            if str(sel_dt) in blocked_dates or sel_dt.weekday() == 6: st.error("Clinic Closed")
            else:
                with st.form("b_form"):
                    morning = [f"{h}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]]
                    evening = [f"{h}:{m:02d} PM" for h in [6, 7] for m in [0, 15, 30, 45]]
                    tm = st.selectbox("Select Slot", morning + evening)
                    if st.form_submit_button("Book Appointment"):
                        new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now()}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Confirmed!")

        elif m == "Upload Reports":
            with st.form("u_form"):
                f = st.file_uploader("Upload Lab/Scan Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note for Doctor")
                if st.form_submit_button("Send to Dr. Priyanka"):
                    b64 = process_img(f)
