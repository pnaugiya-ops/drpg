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
    .diet-box { background: #fff5f7; padding: 20px; border-radius: 12px; border: 1px solid #ffc0cb; line-height: 1.6; }
    .patient-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b6b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

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
                st.session_state.update({"logged_in":True, "name":n, "age":age, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            if st.form_submit_button("Login") and st.text_input("Pass", type="password") == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        search = st.text_input("🔍 Search Patient", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals", "📅 Manage Schedule"])
        
        with t_adm[0]: # Appointments View
            if not df.empty:
                apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().contains(search))]
                for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                    st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)
        
        with t_adm[1]: # Reports View
            reps = df[(df['Type'] == 'REPORT') & (df['Name'].str.lower().contains(search))] if not df.empty else pd.DataFrame()
            for _, row in reps.iterrows():
                with st.expander(f"Report: {row['Name']}"):
                    st.write(f"Note: {row['Details']}")
                    show_img(row['Attachment'])

        with t_adm[2]: # Vitals View
            st.dataframe(df[df['Type'] == 'VITALS'], use_container_width=True)

        with t_adm[3]: # Block Dates
            if st.sidebar.button("Logout", key="d_logout"): st.session_state.logged_in = False; st.rerun()
            block_dt = st.date_input("Block Clinic Date", min_value=date.today())
            if st.button("Block Date"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()

    else: # Patient View
        st.sidebar.markdown(f"### Welcome, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccines & Screening", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "Diet & Yoga":
            st.header("🥗 Nutritional Guidelines")
            if "Pregnant" in st.session_state.stat:
                st.subheader("Pregnancy Daily Diet Chart")
                diet_text = """
                1. **Cereals & Grains:** 60g per serving (6 servings per day)
                2. **Pulses & Beans:** 30g per serving (3 servings per day)
                3. **Milk & Milk Products:** 150ml per serving (2 servings per day)
                4. **Vegetables:** (Green leafy, roots, and others) 100g per serving (4 servings per day)
                5. **Fruits:** 50g per serving (4 servings per day)
                """
                st.markdown(f"<div class='diet-box'>{diet_text}</div>", unsafe_allow_html=True)
                st.download_button("📩 Download Diet Chart as Text", diet_text, file_name="Pregnancy_Diet_BhavyaLabs.txt")
            else:
                st.write("**PCOS Diet:** High protein, low GI foods. Avoid processed sugar.")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160)
                wi = st.number_input("Weight (kg)", 30, 200, 60)
                pu = st.number_input("Pulse", 40, 200, 72)
                bp = st.text_input("BP", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"VITALS","Details":f"BMI: {bmi}, BP: {bp}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"BMI: {bmi}")

        elif m == "Book Appointment":
            sel_dt = st.date_input("Date", min_value=date.today())
            if str(sel_dt) in blocked_dates: st.error("Clinic Closed")
            else:
                with st.form("b_form"):
                    slots = []
                    curr = datetime.strptime("11:00", "%H:%M")
                    while curr <= datetime.strptime("13:45", "%H:%M"):
                        slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    if sel_dt.weekday() != 6:
                        curr = datetime.strptime("18:00", "%H:%M")
                        while curr <= datetime.strptime("19:45", "%H:%M"):
                            slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    tm = st.selectbox("15-Min Slot", slots)
                    if st.form_submit_button("Book"):
                        new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        elif m == "Vaccines & Screening":
            if "PCOS" in st.session_state.stat:
                st.info("HPV Vaccine: 3 doses. Pap Smear: Every 3 years.")
            else:
                st.info("T-Dap, Flu, Tetanus vaccines as per trimester.")

        elif m == "Upload Reports":
            with st.form("u_form"):
                f = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Send"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"REPORT","Details":n,"Attachment":b64,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")

        if st.sidebar.button("Logout", key="p_logout"): st.session_state.logged_in = False; st.rerun()
