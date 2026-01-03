import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. SETTINGS ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; width:100%; } .vax-card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; } .emergency-btn { background:#ff4b6b; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:bold; display:block; text-decoration:none; }</style>", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def img_to_b64(file): return base64.b64encode(file.read()).decode() if file else ""
def show_img(b64): 
    if b64: st.image(io.BytesIO(base64.b64decode(b64)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient", "Doctor"])
    with t1:
        with st.form("p"):
            name = st.text_input("Name")
            stat = st.radio("Status", ["Pregnant", "Non-Pregnant"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":name, "stat":stat, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d"):
            if st.form_submit_button("Doctor Login") and st.text_input("Password", type="password") == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
            if row['Name'] == "ADMIN": continue
            with st.expander(f"📋 {row['Timestamp']} - {row['Name']}"):
                st.write(f"**Type:** {row['Type']} | **Details:** {row.get('Details', '')}")
                if 'Attachment' in row and str(row['Attachment']) not in ["nan", ""]: show_img(row['Attachment'])
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()
    else:
        st.sidebar.markdown("<a href='tel:9676712517' class='emergency-btn'>🚨 EMERGENCY CALL</a>", unsafe_allow_html=True)
        m = st.sidebar.radio("Menu", ["Dashboard", "Vaccines", "Upload", "Booking"])
        
        if m == "Dashboard":
            st.title(f"Hello, {st.session_state.name}")
            if st.session_state.stat == "Pregnant":
                lmp = st.date_input("LMP")
                st.metric("Pregnancy", f"{(datetime.now().date()-lmp).days//7} Weeks")
                

[Image of fetal development stages by week]

        
        elif m == "Vaccines":
            st.title("💉 Vaccines")
            if st.session_state.stat == "Pregnant":
                st.markdown("<div class='vax-card'><b>Tetanus:</b> Confirmation<br><b>T-Dap:</b> 27-36 Wks<br><b>Flu:</b> Anytime</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("<div class='vax-card'><b>HPV:</b> 3 doses (0, 1, 6 months)</div>", unsafe_allow_html=True)
                
        
        elif m == "Upload":
            with st.form("u"):
                f = st.file_uploader("Image", type=['jpg', 'png'])
                note = st.text_input("Note")
                if st.form_submit_button("Upload"):
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"FILE", "Details":note, "Attachment":img_to_b64(f), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")
        
        elif m == "Booking":
            dt = st.date_input("Date")
            if st.button("Confirm"):
                new = pd.DataFrame([{"Name":st.session_state.name, "Type":"APP", "Date":str(dt), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
