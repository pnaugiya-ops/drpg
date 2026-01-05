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
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .timing-card { background:#f0f7ff; padding:10px; border-radius:10px; border-left:4px solid #003366; font-size:0.9em; }
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
    st.sidebar.markdown(f"**User:** {st.session_state.name}")
    st.sidebar.markdown("### 🕒 Clinic Timings")
    st.sidebar.markdown("<div class='timing-card'><b>Mon-Sat:</b> 11AM-2PM & 6PM-8PM<br><b>Sun:</b> 11AM-2PM</div>", unsafe_allow_html=True)
    
    if st.sidebar.button("Logout", key="logout_final"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        t_adm = st.tabs(["Submissions & Reports", "Manage Availability"])
        with t_adm[0]:
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    if row['Type'] == "BLOCK": continue
                    with st.expander(f"{row['Name']} - {row['Timestamp']}"):
                        st.write(f"**Type:** {row.get('Type','')} | **Details:** {row.get('Details','')}")
                        if 'Attachment' in row and str(row['Attachment']) != "nan": show_img(row['Attachment'])
        with t_adm[1]:
            st.subheader("📅 Block Appointment Dates")
            block_dt = st.date_input("Select Date", min_value=date.today())
            if st.button("Block Date"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True))
                st.success(f"{block_dt} Blocked!"); st.rerun()

    else:
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccines & Screening", "Diet & Yoga", "Upload Reports", "Book Appointment"])
        
        if m == "Vitals & BMI":
            st.header("📊 Health Tracker")
            with st.form("v_form"):
                c1, c2, c3 = st.columns(3)
                hi = c1.number_input("Height (cm)", 100, 250, 160)
                wi = c2.number_input("Weight (kg)", 30, 200, 60)
                pu = c3.number_input("Pulse (bpm)", 40, 200, 72)
                bp = st.text_input("Blood Pressure", "120/80")
                if st.form_submit_button("Save Vitals"):
                    bmi = round(wi / ((hi/100)**2), 1)
                    if bmi < 18.5: status = "Underweight"
                    elif 18.5 <= bmi < 25: status = "Normal"
                    else: status = "Overweight"
                    det = f"BMI: {bmi} ({status}), BP: {bp}, Pulse: {pu}"
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"VITALS","Details":det,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Recorded! BMI: {bmi} ({status})")

        elif m == "Vaccines & Screening":
            st.header("💉 Preventive Care")
            if "PCOS" in st.session_state.stat:
                st.subheader("Gynae Wellness")
                st.write("**HPV Vaccination:** 3 doses (0, 1, 6 months) for cervical cancer prevention.")
                st.write("**Pap Smear:** Routine screening every 3 years recommended for women.")
                
            else:
                st.info("Maternal Vaccines: T-Dap (27-36 weeks), Flu (Anytime), Tetanus (Confirmation).")

        elif m == "Diet & Yoga":
            st.header("🥗 Nutrition & Lifestyle")
            if "PCOS" in st.session_state.stat:
                vt, nvt = st.tabs(["Vegetarian PCOS Diet", "Non-Vegetarian PCOS Diet"])
                with vt:
                    st.write("**Breakfast:** Moong dal chilla/Oats. **Lunch:** Brown rice, dal & greens. **Dinner:** Paneer stir-fry.")
                with nvt:
                    st.write("**Breakfast:** 2 Boiled eggs & spinach. **Lunch:** Grilled Fish/Chicken & salad. **Dinner:** Chicken soup.")
                
            else:
                st.write("**Pregnancy Diet:** High Folic Acid, Iron, and Calcium intake.")

        elif m == "Upload Reports":
            st.header("🧪 Send Reports")
            with st.form("u_form"):
                f = st.file_uploader("Select Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Upload"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"REPORT","Details":n,"Attachment":b64,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success("Sent!")

        elif m == "Book Appointment":
            st.header("📅 15-Min Slots")
            sel_dt = st.date_input("Date", min_value=date.today())
            if str(sel_dt) in blocked_dates: st.error("Clinic Closed")
            else:
                with st.form("b_form"):
                    slots = []
                    # Morning Slots
                    curr = datetime.strptime("11:00", "%H:%M")
                    while curr <= datetime.strptime("13:45", "%H:%M"):
                        slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    # Evening Slots (except Sun)
                    if sel_dt.weekday() != 6:
                        curr = datetime.strptime("18:00", "%H:%M")
                        while curr <= datetime.strptime("19:45", "%H:%M"):
                            slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    tm = st.selectbox("Slot", slots)
                    if st.form_submit_button("Book Now"):
                        new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age:{st.session_state.age})","Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                        conn.update(data=pd.concat([df, new], ignore_index=True))
                        st.success("Booked!")
