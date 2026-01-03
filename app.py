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
    .chat-bubble-ai { padding: 12px; border-radius: 15px 15px 15px 0px; background-color: #e6f0ff; border: 1px solid #b3d1ff; color: #003366; margin-bottom: 10px; }
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
        try:
            img_data = base64.b64decode(base64_str)
            st.image(io.BytesIO(img_data), use_container_width=True)
        except:
            st.error("Could not display image.")

# --- 2. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<div class='dr-header'><div class='clinic-name'>BHAVYA LABS & CLINICS</div><div class='dr-name'>Dr. Priyanka Gupta</div><div style='font-size:20px; color:#ff4b6b;'>MS (Obs & Gynae)</div></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["Patient Portal", "Doctor Login"])
    with t1:
        with st.form("p_login"):
            name = st.text_input("Full Name")
            st_val = st.radio("Status", ["Pregnant", "Non-Pregnant"])
            if st.form_submit_button("Enter Portal"):
                st.session_state.logged_in, st.session_state.patient_name, st.session_state.status, st.session_state.role = True, name, st_val, "Patient"
                st.rerun()
    with t2:
        with st.form("d_login"):
            pw = st.text_input("Clinic Password", type="password")
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
                    if row['Name'] == "ADMIN": continue
                    with st.expander(f"📋 {row['Timestamp']} - {row['Name']} ({row['Type']})"):
                        st.write(f"**Details:** {row.get('Details', 'N/A')}")
                        if 'Attachment' in row and str(row['Attachment']) != "nan" and row['Attachment'] != "":
                            st.write("**Attached Image:**")
                            display_base64_img(row['Attachment'])
            else:
                st.info("No records found.")

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
                for i, r in blocked_dates.iterrows():
                    if st.button(f"❌ Unblock {r['Date']}", key=f"un_{i}"):
                        conn.update(data=df.drop(i))
                        st.rerun()

    else:
        st.sidebar.title("Bhavya Clinics")
        menu = st.sidebar.radio("Menu", ["Dashboard", "AI Assistant", "Vaccines", "Labs & Uploads", "Vitals", "Booking"])

        if menu == "Dashboard":
            st.title(f"Hello, {st.session_state.patient_name}")
            st.markdown(f"<div class='status-box'><b>Current Profile:</b> {st.session_state.status}</div>", unsafe_allow_html=True)
            if st.session_state.status == "Pregnant":
                lmp = st.date_input("Select LMP Date")
                wks = (datetime.now().date() - lmp).days // 7
                st.metric("Pregnancy Progress", f"{wks} Weeks")
            else:
                st.info("Welcome to your health dashboard. Use the sidebar to track your progress.")

        elif menu == "AI Assistant":
            st.title("🤖 Interactive Assistant")
            query = st.text_input("Ask a question (e.g., 'Is bleeding normal?' or 'HPV dose')")
            if query:
                st.markdown("<div class='chat-bubble-ai'>I am here to help! For specific medical advice, please book a 15-minute consultation so Dr. Priyanka can review your history. Generally, spotting can be normal after a Pap smear, but heavy bleeding requires immediate attention.</div>", unsafe_allow_html=True)

        elif menu == "Vaccines":
            st.title("💉 Vaccination Schedule")
            if st.session_state.status == "Pregnant":
                st.markdown("<div class='vax-card'><b>Tetanus (TT1):</b> At confirmation.<br><b>T-Dap:</b> 27-36 Weeks.<br><b>Influenza:</b> Seasonal / Anytime.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='vax-card'><b>HPV Vaccine:</b> 3 doses (0, 1, 6 months) for Cervical Cancer prevention. Recommended up to age 45.</div>", unsafe_allow_html=True)

        elif menu == "Labs & Uploads":
            st.title("🧪 Report Uploads")
            with st.form("l_upload"):
                hb = st.number_input("Hb%", 5.0, 18.0, 11.0)
                file = st.file_uploader("Upload Report/Prescription Image", type=['jpg', 'jpeg',
