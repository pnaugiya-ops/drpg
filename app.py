import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io
from PIL import Image

# --- 1. CONFIG ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }</style>", unsafe_allow_html=True)

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
        with st.form("p_l"):
            n = st.text_input("Full Name")
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":n, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_l"):
            if st.form_submit_button("Login") and st.text_input("Pass", type="password") == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN ---
else:
    if st.sidebar.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        if not df.empty:
            for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                if row['Name'] == "ADMIN": continue
                with st.expander(f"{row['Name']} - {row['Timestamp']}"):
                    st.write(f"Type: {row.get('Type','')} | Details: {row.get('Details','')}")
                    if 'Attachment' in row and str(row['Attachment']) != "nan": show_img(row['Attachment'])
    else:
        st.sidebar.title(f"Hi, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Vitals", "Vaccines", "Diet & Yoga", "Reports", "Booking"])
        
        if m == "Vitals":
            with st.form("v"):
                h = st.number_input("Ht (cm)", 100, 250, 160)
                w = st.number_input("Wt (kg)", 30, 200, 60)
                p = st.number_input("Pulse", 40, 200, 72)
                bp = st.text_input("BP", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(w/((h/100)**2), 1)
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    det = f"BMI:{bmi}, BP:{bp}, P:{p}"
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":det,"Timestamp":ts}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Saved! BMI: {bmi}")

        elif m == "Vaccines":
            if "Pregnant" in st.session_state.stat:
                st.info("T-Dap: 27-36 weeks | Flu: Anytime | Tetanus: Confirmation")
            else:
                st.info("HPV Vaccine: 3 doses (0, 1, 6 months) for prevention.")

        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                d1, d2, d3 = st.tabs(["1st Tri", "2nd Tri", "3rd Tri"])
                with d1: st.write("Diet: Folic Acid. Yoga: Butterfly.")
                with d2: st.write("Diet: Iron/Calcium. Yoga: Palm Tree.")
                with d3: st.write("Diet: High Fiber. Yoga: Squats.")
            else:
                st.write("PCOS: Low GI, No sugar. Yoga: Surya Namaskar.")

        elif m == "Reports":
            with st.form("u"):
                f = st.file_uploader("Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Upload"):
                    b64 = process_img(f)
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"UPLOAD","Details":n,"Attachment":b64,"Timestamp":ts}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success("Sent!")

        elif m == "Booking":
            with st.form("b"):
                dt = st.date_input("Date")
                tm = st.selectbox("Slot", ["10AM", "12PM", "5PM", "7PM"])
                if st.form_submit_button("Book"):
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{dt} {tm}","Timestamp":ts}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Booked for {dt}")
