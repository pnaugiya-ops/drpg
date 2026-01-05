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
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; margin-bottom:20px; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; color: #333; font-size: 16px; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Establishing Connection with Error Catching
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Connection Error: {e}")

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

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
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
            pass_in = st.text_input("Pass", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()
                else: st.error("Wrong Password")

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
                if st.form_submit_button("Broadcast"):
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
        m = st.sidebar.radio("Menu", ["Diet & Yoga", "Vitals & BMI", "Upload Reports", "Book Appointment"])
        
        if m == "Diet & Yoga":
            st.header("🥗 Your Personalized Diet Plan")
            if "Pregnant" in st.session_state.stat:
                st.info("Maintaining a balanced diet is essential for fetal development and maternal health across all three trimesters[cite: 1].")
                
                diet_summary = """
                **General Safety & Guidelines:** [cite: 16]
                - **Milk Intake:** Aim for 3–4 servings of pasteurized/low-fat milk per day[cite: 4, 6].
                - **Hydration:** Drink 2.5–3 liters of water daily[cite: 19].
                - **Avoid:** Raw meat/eggs, unpasteurized dairy, and high-mercury fish[cite: 17].
                - **Limit:** Caffeine to under 200mg per day[cite: 18].
                """
                st.markdown(f"<div class='diet-box'>{diet_summary}</div>", unsafe_allow_html=True)
                
                tri = st.selectbox("Select Your Trimester", ["First Trimester (Weeks 1–12)", "Second Trimester (Weeks 13–26)", "Third Trimester (Weeks 27–40)"])
                
                if "First" in tri:
                    st.success("**Focus:** Folic acid for neural tube development and Vitamin B6 for nausea[cite: 8].")
                    st.write("**Early Morning:** Warm water + 4–5 soaked almonds [cite: 9]")
                    st.write("**Breakfast:** Veggie Poha or Whole grain toast + boiled eggs [cite: 9]")
                elif "Second" in tri:
                    st.success("**Focus:** Calcium and iron for bone growth and blood volume[cite: 11].")
                    st.write("**Lunch:** Brown rice + dal + veggies OR chicken curry [cite: 12]")
                    st.write("**Evening Snack:** Handful of nuts or chicken sandwich [cite: 12]")
                elif "Third" in tri:
                    st.success("**Focus:** High fiber for digestion and healthy fats for baby weight[cite: 14].")
                    st.write("**Lunch:** Millet khichdi with veggies OR chicken stew [cite: 15]")
                    st.write("**Dinner:** Chapati + rajma/chole OR fish curry [cite: 15]")
            else:
                st.subheader("PCOS Diet & Lifestyle")
                st.write("Focus on High Fiber, Low GI foods. Daily activity like Yoga is highly recommended.")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160)
                wi = st.number_input("Weight (kg)", 30, 200, 60)
                bp = st.text_input("BP", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":f"BMI:{bmi}, BP:{bp}","Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"BMI: {bmi}")

        elif m == "Book Appointment":
            sel_dt = st.date_input("Date", min_value=date.today())
            if str(sel_dt) in blocked_dates: st.error("Clinic Closed")
            else:
                with st.form("b_form"):
                    slots = [f"{h:02d}:00" for h in range(11, 14)] + [f"{h:02d}:00" for h in range(18, 20)]
                    tm = st.selectbox("Select Slot", slots)
                    if st.form_submit_button("Confirm"):
                        new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now()}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        elif m == "Upload Reports":
            with st.form("u_form"):
                f = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Send"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"REPORT","Details":n,"Attachment":b64,"Timestamp":datetime.now()}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")

        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
