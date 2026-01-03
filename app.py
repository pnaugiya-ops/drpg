import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. SETTINGS & STYLES ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; width:100%; } .vax-card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; } .emergency-btn { background:#ff4b6b; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; display:block; text-decoration:none; }</style>", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def img_to_b64(file): 
    return base64.b64encode(file.read()).decode() if file else ""
def show_img(b64): 
    if b64: st.image(io.BytesIO(base64.b64decode(b64)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Name")
            stat = st.radio("Status", ["Pregnant", "Non-Pregnant"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":name, "stat":stat, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        if not df.empty:
            for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                if row['Name'] == "ADMIN": continue
                with st.expander(f"📋 {row['Timestamp']} - {row['Name']}"):
                    st.write(f"**Type:** {row.get('Type','')} | **Details:** {row.get('Details', '')}")
                    if 'Attachment' in row and str(row['Attachment']) not in ["nan", ""]: show_img(row['Attachment'])
        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
    else:
        st.sidebar.markdown("<a href='tel:9676712517' class='emergency-btn'>🚨 EMERGENCY CALL</a>", unsafe_allow_html=True)
        m = st.sidebar.radio("Menu", ["Dashboard", "Vaccines", "Upload Reports", "Booking"])
        
        if m == "Dashboard":
            st.title(f"Hello, {st.session_state.name}")
            if st.session_state.stat == "Pregnant":
                lmp = st.date_input("LMP Date")
                wks = (datetime.now().date()-lmp).days//7
                st.metric("Pregnancy Progress", f"{wks} Weeks")
                st.write("---")
                st.write("### Fetal Development Reference")
                # Visual guide for development stages
            else: st.info("Welcome back! Use the menu to track your health.")
        
        elif m == "Vaccines":
            st.title("💉 Vaccination Guide")
            if st.session_state.stat == "Pregnant":
                st.markdown("<div class='vax-card'><b>Tetanus (TT1):</b> On Confirmation<br><b>T-Dap:</b> 27-36 Weeks<br><b>Influenza:</b> Anytime</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='vax-card'><b>HPV Vaccine:</b> 3 doses (0, 1, 6 months) for Cervical Cancer prevention.</div>", unsafe_allow_html=True)
        
        elif m == "Upload Reports":
            st.title("🧪 Upload Reports")
            with st.form("u_form"):
                f = st.file_uploader("Select Image", type=['jpg', 'png', 'jpeg'])
                note = st.text_input("Note (e.g. Blood Report)")
                if st.form_submit_button("Submit"):
                    b64 = img_to_b64(f)
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"UPLOAD", "Details":note, "Attachment":b64, "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Uploaded!")
        
        elif m == "Booking":
            dt = st.date_input("Select Date", min_value=datetime.now().date())
            if st.button("Confirm Booking"):
                new = pd.DataFrame([{"Name":st.session_state.name, "Type":"APP", "Details":str(dt), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
