import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date
import base64, io
from PIL import Image

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("""
    <style>
    .dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; }
    .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; }
    .vax-card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; }
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
    # CLINIC TIMINGS IN SIDEBAR
    st.sidebar.markdown("### 🕒 Clinic Timings")
    st.sidebar.markdown("""
    <div class='timing-card'>
    <b>Mon - Sat:</b><br>11:00 AM - 2:00 PM<br>6:00 PM - 8:00 PM<br><br>
    <b>Sunday:</b><br>11:00 AM - 2:00 PM
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    
    # Get Blocked Dates
    blocked_dates = []
    if not df.empty:
        blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist()

    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        t_adm = st.tabs(["Patient Submissions", "Manage Availability"])
        
        with t_adm[0]:
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    if row['Type'] == "BLOCK": continue
                    with st.expander(f"{row['Name']} - {row['Timestamp']}"):
                        st.write(f"**Type:** {row.get('Type','')} | **Details:** {row.get('Details','')}")
                        if 'Attachment' in row and str(row['Attachment']) != "nan": show_img(row['Attachment'])
        
        with t_adm[1]:
            st.subheader("📅 Block/Unblock Dates")
            col1, col2 = st.columns(2)
            with col1:
                block_dt = st.date_input("Select Date to Block", min_value=date.today())
                if st.button("Block Date"):
                    new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Date {block_dt} blocked!")
                    st.rerun()
            with col2:
                if blocked_dates:
                    to_unblock = st.selectbox("Blocked Dates", blocked_dates)
                    if st.button("Unblock Date"):
                        df_new = df[~((df['Type'] == "BLOCK") & (df['Details'] == to_unblock))]
                        conn.update(data=df_new)
                        st.success("Date unblocked!")
                        st.rerun()
                else:
                    st.write("No dates currently blocked.")

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
                    det = f"BMI:{bmi}, BP:{bp}, P:{p}"
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"VITALS","Details":det,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success(f"Saved! BMI: {bmi}")

        elif m == "Reports":
            with st.form("u"):
                f = st.file_uploader("Image", type=['jpg', 'png', 'jpeg'])
                n = st.text_input("Note")
                if st.form_submit_button("Upload"):
                    b64 = process_img(f)
                    new = pd.DataFrame([{"Name":st.session_state.name,"Type":"UPLOAD","Details":n,"Attachment":b64,"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.success("Sent!")

        elif m == "Booking":
            st.subheader("📅 Book Appointment")
            sel_dt = st.date_input("Select Date", min_value=date.today())
            if str(sel_dt) in blocked_dates:
                st.error("The clinic is closed on this date. Please select another day.")
            else:
                with st.form("b_f"):
                    tm = st.selectbox("Slot", ["11:00 AM", "12:00 PM", "01:00 PM", "06:00 PM", "07:00 PM"])
                    if st.form_submit_button("Confirm Booking"):
                        new = pd.DataFrame([{"Name":st.session_state.name,"Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                        conn.update(data=pd.concat([df, new], ignore_index=True))
                        st.success(f"Booked for {sel_dt} at {tm}")
