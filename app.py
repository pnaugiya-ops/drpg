import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64
import io

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Bhavya Labs & Clinics", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    .dr-header { background-color: #003366; color: white; padding: 25px; border-radius: 15px; text-align: center; margin-bottom: 20px; border-bottom: 5px solid #ff4b6b; }
    .stButton>button { border-radius: 10px; background-color: #ff4b6b; color: white; font-weight: bold; width: 100%; }
    .vax-card { background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .emergency-btn { background-color: #ff4b6b; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 20px; display: block; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)
DR_PASSWORD = "clinicadmin786"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.role = False, "Patient"

# --- HELPERS ---
def img_to_b64(file):
    return base64.b64encode(file.read()).decode() if file else ""

def show_b64_img(b64_str):
    if b64_str:
        st.image(io.BytesIO(base64.b64decode(b64_str)), use_container_width=True)

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><h1>BHAVYA LABS & CLINICS</h1><h3>Dr. Priyanka Gupta</h3><p>MS (Obs & Gynae)</p></div>", unsafe_allow_html=True)
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

# --- 3. MAIN APP ---
else:
    df = conn.read(ttl=0)
    
    if st.session_state.role == "Doctor":
        st.title("👨‍⚕️ Admin: Dr. Priyanka Gupta")
        t_adm = st.tabs(["Patient Records", "Schedule"])
        with t_adm[0]:
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    if row['Name'] == "ADMIN": continue
                    with st.expander(f"📋 {row['Timestamp']} - {row['Name']} ({row['Type']})"):
                        st.write(f"**Details:** {row.get('Details', 'N/A')}")
                        if 'Attachment' in row and str(row['Attachment']) not in ["nan", ""]:
                            show_b64_img(row['Attachment'])
            else: st.info("No records.")
        with t_adm[1]:
            b_dt = st.date_input("Block Date", min_value=datetime.now().date())
            if st.button("Confirm Block"):
                new = pd.DataFrame([{"Name":"ADMIN", "Type":"BLOCK", "Date":str(b_dt), "Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()
            for i, r in df[df['Type'] == 'BLOCK'].iterrows():
                if st.button(f"❌ Unblock {r['Date']}", key=f"un_{i}"):
                    conn.update(data=df.drop(i)); st.rerun()

    else:
        st.sidebar.markdown("<a href='tel:9676712517' class='emergency-btn'>🚨 EMERGENCY CALL</a>", unsafe_allow_html=True)
        menu = st.sidebar.radio("Menu", ["Dashboard", "Vaccines", "Upload Reports", "Vitals", "Booking"])

        if menu == "Dashboard":
            st.title(f"Hello, {st.session_state.patient_name}")
            if st.session_state.status == "Pregnant":
                lmp = st.date_input("LMP Date")
                wks = (datetime.now().date() - lmp).days // 7
                st.metric("Pregnancy Progress", f"{wks} Weeks")
                

[Image of fetal development stages by week]

            else: st.info("Welcome to your dashboard. Log your health data below.")

        elif menu == "Vaccines":
            st.title("💉 Vaccination Guide")
            if st.session_state.status == "Pregnant":
                st.markdown("<div class='vax-card'><b>Tetanus (TT1):</b> At confirmation.<br><b>T-Dap:</b> 27-36 Weeks.<br><b>Influenza:</b> Anytime.</div>", unsafe_allow_html=True)
                
            else:
                st.markdown("<div class='vax-card'><b>HPV Vaccine:</b> 3 doses (0, 1, 6 months). Prevents Cervical Cancer.</div>", unsafe_allow_html=True)
                

        elif menu == "Upload Reports":
            st.title("🧪 Upload Prescriptions")
            with st.form("u"):
                file = st.file_uploader("Image (
