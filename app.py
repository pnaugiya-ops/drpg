import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import re
import base64
import io

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8faff; }
    .dr-header { 
        background-color: #003366; color: white; padding: 30px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
        border-bottom: 5px solid #ff4b6b;
    }
    .clinic-name { font-size: 36px; font-weight: bold; }
    .dr-name { font-size: 28px; font-weight: bold; }
    .stButton>button { border-radius: 12px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #e6f0ff; border-left: 6px solid #003366; margin-bottom: 20px; color: #003366; }
    .vax-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786" 

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPER: FILE PROCESSING ---
def img_to_base64(uploaded_file):
    if uploaded_file is not None:
        return base64.b64encode(uploaded_file.read()).decode()
    return ""

def display_base64_img(base64_str):
    if base64_str:
        img_data = base64.b64decode(base64_str)
        st.image(io.BytesIO(img_data), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><div class='clinic-name'>BHAVYA LABS & CLINICS</div><div class='dr-name'>Dr. Priyanka Gupta</div><div style='font-size:20px; color:#ff4b6b;'>MS (Obs & Gynae)</div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            st_val = st.radio("Status", ["Pregnant", "Non-Pregnant"])
            if st.form_submit_button("Enter"):
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, st_val, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login") and pw == DR_PASSWORD:
                st.session_state.logged_in, st.session_state.role = True, "Doctor"
                st.rerun()

# --- 3. MAIN INTERFACE ---
else:
    df = conn.read(ttl=0)
    
    if st.session_state.role == "Doctor":
        st.title("👨‍⚕️ Admin: Dr. Priyanka Gupta")
        t_adm = st.tabs(["Patient Records & Uploads", "Schedule Management"])
        
        with t_adm[0]:
            st.subheader("All Patient Submissions")
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    # Skip blocking/admin rows in the record list
                    if row['Name'] == "ADMIN": continue
                    
                    with st.expander(f"📋 {row['Timestamp']} - {row['Name']} ({row['Type']})"):
                        st.write(f"**Details:** {row.get('Details', 'N/A')}")
                        if 'Attachment' in row and str(row['Attachment']) != "nan" and row['Attachment'] != "":
                            st.write("**Attached File:**")
                            display_base64_img(row['Attachment'])
                        else:
                            st.info("No file attached to this entry.")
            else:
                st.info("No patient records found.")

        with t_adm[1]:
            c1, c2 = st.columns(2)
            with c1:
                st.write("### Block a Date")
                b_dt = st.date_input("Select Date", min_value=datetime.now().date())
                if st.button("Confirm Block"):
                    new = pd.DataFrame([{"Name":"ADMIN", "Type":"BLOCK", "Date":str(b_dt), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                    conn.update(data=pd.concat([df, new], ignore_index=True))
                    st.rerun()
            with c2:
                st.write("### Currently Blocked")
                blocked_dates = df[df['Type'] == 'BLOCK']
                if not blocked_dates.empty:
                    for i, r in blocked_dates.iterrows():
                        if st.button(f"❌ Unblock {r['Date']}", key=f"un_{i}")
