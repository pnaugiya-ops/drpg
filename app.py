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
        st.sidebar.info("🕒 **Clinic Timings:**\n- 11:00 AM - 02:00 PM\n- 06:00 PM - 08:00 PM")
        
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals", "📢 Broadcast", "📅 Availability"])
        
        with t_adm[0]:
            apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().str.contains(search))]
            for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)
        
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
        m = st.sidebar.radio("Menu", ["Tracker & Calculator", "Diet & Yoga", "Vaccine Portal", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        if m == "Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("👶 Pregnancy Tracker & Baby Growth")
                lmp = st.date_input("Last Menstrual Period (LMP)", value=date.today() - timedelta(days=30))
                edd = lmp + timedelta(days=280)
                diff = date.today() - lmp
                weeks, days = diff.days // 7, diff.days % 7
                st.success(f"🗓️ **Expected Delivery Date (EDD):** {edd.strftime('%d %B %Y')}")
                st.info(f"⏳ **Current Stage:** {weeks} Weeks and {days} Days")
                
                st.divider()
                st.subheader("📖 Week-by-Week Development")
                if weeks <= 4: st.write("🌱 **Week 4 (Poppy Seed):** The baby is a tiny ball of cells snuggling into the womb.")
                elif weeks <= 5: st.write("💓 **Week 5 (Sesame Seed):** The heart tube begins to pulse.")
                elif weeks <= 8: st.write("🍇 **Week 8 (Raspberry):** Fingers and toes are starting to sprout.")
                elif weeks <= 12: st.write("🍋 **Week 12 (Lime):** The baby can open/close fists and make sucking motions.")
                elif weeks <= 20: st.write("🍌 **Week 20 (Banana):** You will likely feel the first 'flutters' now.")
                elif weeks <= 27: st.write("🥦 **Week 27 (Cauliflower):** Baby begins to develop a regular sleep/wake schedule.")
                elif weeks <= 40: st.write("🍉 **Week 40 (Watermelon):** Full term! Ready for the world.")
                

            else:
                st.header("🗓️ Menstrual Cycle Tracker")
                last_p = st.date_input("Last Period Start Date", value=date.today() - timedelta(days=28))
                cycle_len = st.slider("Average Cycle Length (Days)", 21, 45, 28)
                next_p = last_p + timedelta(days=cycle_len)
                ovulation = last_p + timedelta(days=cycle_len - 14)
                st.success(f"🩸 **Next Expected Period:** {next_p.strftime('%d %B %Y')}")
                st.warning(f"🥚 **Estimated Ovulation Window:** Around {ovulation.strftime('%d %B %Y')}")
                

        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness")
                t1, t2 = st.tabs(["🥗 Nutrition", "🧘 Exercises"])
                with t1:
                    tri = st.selectbox("Select Trimester", ["1st Trimester", "2nd Trimester", "3rd Trimester"])
                    if "1st" in tri: st.write("**Focus:** Folic acid & B6. **Breakfast:** Veggie Poha + Milk.")
                    elif "2nd" in tri: st.write("**Focus:** Calcium & Iron. **Lunch:** Brown rice + Dal + Chicken/Veg.")
                    else: st.write("**Focus:** Fiber & Fats. **Dinner:** Chapati + Rajma/Fish + Curd.")
                with t2:
                    st.write("**Recommended:** Walking, Prenatal Yoga, and Kegels. Avoid lying flat on your back after the 1st trimester.")
                    
            else:
                st.header("🌸 PCOS Wellness Hub")
                t1, t2 = st.tabs(["🥗 PCOS Nutrition", "🏋️ PCOS Exercise"])
                with t1:
                    st.markdown("<div class='diet-box'><b>Focus:</b> High Protein (50-60g) & Low-GI Fiber.</div>", unsafe_allow_html=True)
                    st.write("**Breakfast:** Moong dal chilla or 2 Egg whites + toast.")
                with t2:
                    st.write("**Routine:** Strength training 3-4x/week. Brisk walking (30-45m) daily.")

        elif m == "Vaccine Portal":
            st.header("💉 Preventive Care")
            if "Pregnant" in st.session_state.stat:
                st.info("Essential Maternal Vaccines: Tetanus (TT), T-Dap, and Flu shots.")
            else:
                st.info("Essential Gynae Wellness: HPV Vaccine (3 doses) and Pap Smear screening.")

        elif m == "Book Appointment":
            st.write("🕒 **Hours:** 11:00 AM - 02:00 PM & 06:00 PM - 08:00 PM")
            sel_dt = st.date_input("Select Date", min_value=date.today())
            if sel_dt.weekday() == 6: st.error("Clinic Closed on Sundays")
            else:
                with st.form("book_form"):
                    morning = [f"{h}:{m:02d} AM" for h in range(11, 14) for m in [0, 15, 30, 45]]
                    evening = [f"{h}:{m:02d} PM" for h in [6, 7] for m in [0, 15, 30, 45]]
                    tm = st.selectbox("Choose a Slot", morning + evening)
                    if st.form_submit_button("Confirm"):
                        new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now()}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Appointment Booked!")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160); wi = st.
