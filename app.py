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
        m = st.sidebar.radio("Menu", ["Baby Tracker & Calculator", "Diet & Yoga", "Vaccine & Screening Portal", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        # --- RESTORED PREGNANCY CALCULATOR & NEW BABY TRACKER ---
        if m == "Baby Tracker & Calculator":
            if "Pregnant" in st.session_state.stat:
                st.header("👶 Pregnancy Tracker & Calculator")
                lmp = st.date_input("Select Last Menstrual Period (LMP)", value=date.today() - timedelta(days=30))
                if lmp:
                    edd = lmp + timedelta(days=280)
                    today = date.today()
                    diff = today - lmp
                    weeks = diff.days // 7
                    days = diff.days % 7
                    st.success(f"🗓️ **Estimated Delivery Date (EDD):** {edd.strftime('%d %B %Y')}")
                    st.info(f"⏳ **Current Pregnancy Stage:** {weeks} Weeks and {days} Days")
                    
                    st.divider()
                    st.subheader("📖 Week-by-Week Baby Development")
                    # Week-by-Week Data Integration
                    if weeks <= 4: st.write("🌱 **Week 1–4 (The Seed):** The baby is a tiny ball of cells the size of a **poppy seed**.")
                    elif weeks <= 5: st.write("💓 **Week 5 (The Heartbeat):** Size of a **sesame seed**. The brain, spine, and heart start forming.")
                    elif weeks <= 6: st.write("🎋 **Week 6 (Little Buds):** Size of a **lentil**. Tiny buds appear that will become arms and legs.")
                    elif weeks <= 7: st.write("🫐 **Week 7 (Face Forming):** Size of a **blueberry**. The face, eyes, and nostrils start to take shape.")
                    elif weeks <= 8: st.write("🍇 **Week 8 (Moving Around):** Size of a **raspberry**. Fingers and toes are sprouting.")
                    elif weeks <= 12: st.write("🍋 **Week 11–12 (Reflexes):** Size of a **lime**. Baby can open/close fists and make sucking motions.")
                    elif weeks <= 15: st.write("🍎 **Week 13–15 (Active Flipping):** Size of an **apple**. Baby is active, flipping and rolling in fluid.")
                    elif weeks <= 18: st.write("🫑 **Week 16–18 (Hearing Sounds):** Size of a **bell pepper**. Baby can hear your voice.")
                    elif weeks <= 20: st.write("🍌 **Week 19–20 (The Halfway Mark):** Size of a **banana**. You may feel first flutters.")
                    elif weeks <= 23: st.write("🍊 **Week 21–23 (Developing Senses):** Size of a **grapefruit**. Baby can taste amniotic fluid.")
                    elif weeks <= 27: st.write("🥦 **Week 24–27 (Opening Eyes):** Size of **cauliflower**. Baby begins regular sleep/wake schedule.")
                    elif weeks <= 31: st.write("🥥 **Week 28–31 (Getting Smart):** Size of a **coconut**. Brain is growing fast.")
                    elif weeks <= 34: st.write("🍈 **Week 32–34 (Filling Out):** Size of a **cantaloupe**. Baby is putting on fat.")
                    elif weeks <= 40: st.write("🍉 **Week 38–40 (Full Term):** Size of a **watermelon**. Baby is ready for the world.")

            else:
                # --- RESTORED MENSTRUAL CYCLE CALCULATOR ---
                st.header("🗓️ Period & Cycle Tracker")
                last_p = st.date_input("Last Period Start Date", value=date.today() - timedelta(days=28))
                cycle_len = st.slider("Average Cycle Length (Days)", 21, 45, 28)
                if last_p:
                    next_p = last_p + timedelta(days=cycle_len)
                    ovulation = last_p + timedelta(days=cycle_len - 14)
                    st.success(f"🩸 **Next Expected Period:** {next_p.strftime('%d %B %Y')}")
                    st.warning(f"🥚 **Estimated Ovulation Window:** Around {ovulation.strftime('%d %B %Y')}")

        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                st.header("🤰 Pregnancy Wellness Hub")
                tab_diet, tab_exercise = st.tabs(["🥗 Nutrition Plan", "🧘 Trimester Exercises"])
                with tab_diet:
                    st.markdown("""<div class='diet-box'>
                    - 🥛 <b>Milk:</b> 3–4 servings daily.<br>
                    - 💧 <b>Hydration:</b> 2.5–3 Liters water daily.<br>
                    - ☕ <b>Caffeine:</b> Limit to < 200mg/day.
                    </div>""", unsafe_allow_html=True)
                    tri = st.selectbox("Select Trimester (Nutrition)", ["1st Trimester (Weeks 1-12)", "2nd Trimester (Weeks 13-26)", "3rd Trimester (Weeks 27-40)"])
                    if "1st" in tri:
                        st.write("**Breakfast:** Veggie Poha/Upma + milk OR Whole grain toast + 2 eggs.")
                    elif "2nd" in tri:
                        st.write("**Lunch:** Brown rice + dal + mixed veggies OR Chicken curry.")
                    elif "3rd" in tri:
                        st.write("**Lunch:** Millet khichdi + dal + salad OR Grilled salmon + rice.")
                with tab_exercise:
                    tri_ex = st.selectbox("Select Trimester (Exercises)", ["1st Trimester: Gentle Adaptation", "2nd Trimester: Building Strength", "3rd Trimester: Mobility & Labor Prep"])
                    if "1st" in tri_ex: st.write("- Walking\n- Prenatal Yoga
