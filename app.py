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
    .emergency-btn { background-color: #ff0000 !important; color: white !important; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
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
    except Exception: return ""

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
            pass_in = st.text_input("Pass", type="password")
            if st.form_submit_button("Login"):
                if pass_in == "clinicadmin786":
                    st.session_state.update({"logged_in":True, "role":"D", "name":"Dr. Priyanka"})
                    st.rerun()
                else: st.error("Wrong Password")

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []
    st.sidebar.markdown(f"### Hello, {st.session_state.name}")
    st.sidebar.markdown('<a href="tel:+919999999999" class="emergency-btn">📞 EMERGENCY CALL</a>', unsafe_allow_html=True)

    if st.session_state.role == "D":
        st.markdown("<div class='dr-header'><h1>👨‍⚕️ Doctor Dashboard</h1></div>", unsafe_allow_html=True)
        search = st.text_input("🔍 Search Patient Name", "").lower()
        t_adm = st.tabs(["📋 Appointments", "🧪 Reports", "📈 Vitals", "📅 Availability"])
        
        with t_adm[0]:
            if not df.empty:
                apps = df[(df['Type'] == 'APP') & (df['Name'].str.lower().contains(search))]
                for _, row in apps.sort_values(by='Timestamp', ascending=False).iterrows():
                    st.markdown(f"<div class='patient-card'><b>👤 {row['Name']}</b><br>📅 Slot: {row['Details']}</div>", unsafe_allow_html=True)
        
        with t_adm[1]:
            reps = df[(df['Type'] == 'REPORT') & (df['Name'].str.lower().contains(search))] if not df.empty else pd.DataFrame()
            for _, row in reps.iterrows():
                with st.expander(f"Report: {row['Name']}"):
                    st.write(f"Note: {row['Details']}")
                    show_img(row['Attachment'])

        with t_adm[2]:
            st.dataframe(df[df['Type'] == 'VITALS'], use_container_width=True)

        with t_adm[3]:
            block_dt = st.date_input("Block Clinic Date", min_value=date.today())
            if st.button("Confirm Block"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()
            
        if st.sidebar.button("Logout", key="d_logout"): st.session_state.logged_in = False; st.rerun()

    else: # Patient View
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccines", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "Diet & Yoga":
            st.header("🥗 Nutritional Guidelines")
            if "Pregnant" in st.session_state.stat:
                st.subheader("Pregnancy Daily Diet Chart")
                st.markdown("""<div class='diet-box'>
                1. <b>Cereals & Grains:</b> 60g per serving (6 servings/day)<br>
                2. <b>Pulses & Beans:</b> 30g per serving (3 servings/day)<br>
                3. <b>Milk & Milk Products:</b> 150ml per serving (2 servings/day)<br>
                4. <b>Vegetables:</b> 100g per serving (4 servings/day)<br>
                5. <b>Fruits:</b> 50g per serving (4 servings/day)</div>""", unsafe_allow_html=True)
                

[Image of the food pyramid for pregnant women]

            else:
                st.subheader("PCOS Diet Chart")
                st.write("Focus on High Fiber, Low GI foods, and Lean Proteins.")

        elif m == "Vitals & BMI":
            with st.form("v_form"):
                hi = st.number_input("Height (cm)", 100, 250, 160)
                wi = st.number_input("Weight (kg)", 30, 200, 60)
                pu = st.number_input("Pulse", 40, 200, 72)
                bp = st.text_input("BP", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"VITALS","Details":f"BMI:{bmi}, BP:{bp}, Pulse:{pu}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
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
                    tm = st.selectbox("Slot", slots)
                    if st.form_submit_button("Confirm Booking"):
                        new = pd.DataFrame([{"Name":f"{st.session_state.name}","Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        elif m == "Vaccines":
            if "PCOS" in st.session_state.stat:
                st.info("HPV Vaccine (3 doses) and regular Pap Smear screening are key for Gynae wellness.")
                
            else:
                st.info("Maternal Vaccination: T-Dap, Flu, and Tetanus Toxoid as advised by the doctor.")

        elif m == "Upload Reports":
            with st.form("u_form"):
                f = st.file_uploader("Select Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Send to Doctor"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name}","Type":"REPORT","Details":n,"Attachment":b64,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Report Sent!")

        if st.sidebar.button("Logout", key="p_logout"): st.session_state.logged_in = False; st.rerun()
