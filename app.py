import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64, io

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Bhavya Labs", layout="wide")
st.markdown("<style>.dr-header { background:#003366; color:white; padding:20px; border-radius:15px; text-align:center; border-bottom:5px solid #ff4b6b; } .stButton>button { border-radius:10px; background:#ff4b6b; color:white; font-weight:bold; width:100%; } .vax-card { background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px; }</style>", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- HELPERS ---
def img_to_b64(f): return base64.b64encode(f.read()).decode() if f else ""
def show_img(b): 
    if b: st.image(io.BytesIO(base64.b64decode(b)), use_container_width=True)

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
            if st.form_submit_button("Login") and st.text_input("Pass", type="password") == "clinicadmin786":
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
                st.write(f"Type: {row.get('Type','')} | Details: {row.get('Details', '')}")
                if 'Attachment' in row and str(row['Attachment']) not in ["nan", ""]: show_img(row['Attachment'])
        if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
    else:
        st.sidebar.title(f"Hello, {st.session_state.name}")
        m = st.sidebar.radio("Menu", ["Vitals & BMI", "Vaccines", "Diet & Yoga", "Reports", "Booking"])
        
        if m == "Vitals & BMI":
            with st.form("v"):
                h, w, p = st.columns(3)
                hi = h.number_input("Ht(cm)", 100, 250, 160)
                wi = w.number_input("Wt(kg)", 30, 200, 60)
                pu = p.number_input("Pulse", 40, 200, 72)
                bp = st.text_input("BP", "120/80")
                if st.form_submit_button("Save"):
                    bmi = round(wi/((hi/100)**2), 1)
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"VIT", "Details":f"BMI:{bmi}, BP:{bp}, Pulse:{pu}", "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success(f"BMI: {bmi}")

        elif m == "Vaccines":
            if "Pregnant" in st.session_state.stat:
                st.write("Tetanus (TT1): Confirmation | T-Dap: 27-36 weeks | Flu: Anytime")
                
            else:
                st.write("HPV: 3 doses (0, 1, 6 months) for Cervical Cancer prevention.")
                

        elif m == "Diet & Yoga":
            if "Pregnant" in st.session_state.stat:
                d1, d2, d3 = st.tabs(["1st Tri", "2nd Tri", "3rd Tri"])
                with d1: 
                    st.write("Diet: Folic Acid. Yoga: Butterfly pose.")
                    

[Image of first trimester pregnancy diet chart]

                with d2: 
                    st.write("Diet: Iron/Calcium. Yoga: Palm Tree pose.")
                    

[Image of second trimester pregnancy diet chart]

                with d3: 
                    st.write("Diet: High Fiber. Yoga: Supported Squats.")
                    

[Image of third trimester pregnancy diet chart]

            else:
                st.write("PCOS Diet: Low GI, No Sugar. Yoga: Surya Namaskar.")
                

        elif m == "Reports":
            with st.form("u"):
                f = st.file_uploader("Upload Image", type=['jpg', 'png'])
                n = st.text_input("Note")
                if st.form_submit_button("Send"):
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"REP", "Details":n, "Attachment":img_to_b64(f), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Sent!")

        elif m == "Booking":
            with st.form("b"):
                dt = st.date_input("Date")
                tm = st.selectbox("Slot", ["10AM", "11AM", "12PM", "5PM", "6PM", "7PM"])
                if st.form_submit_button("Confirm"):
                    new = pd.DataFrame([{"Name":st.session_state.name, "Type":"APP", "Details":f"{dt} {tm}", "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")

    if st.sidebar.button("Logout"): st.session_state.logged_in = False; st.rerun()
