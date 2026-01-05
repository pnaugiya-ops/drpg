import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date, timedelta
import base64, io
from PIL import Image

# --- 1. CONFIG ---
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
        with st.form("p_l"):
            n = st.text_input("Full Name")
            age = st.number_input("Age", min_value=1, max_value=100, value=25)
            s = st.radio("Status", ["Pregnant", "PCOS/Gynae"])
            if st.form_submit_button("Enter"):
                st.session_state.update({"logged_in":True, "name":n, "age":age, "stat":s, "role":"P"})
                st.rerun()
    with t2:
        with st.form("d_l"):
            if st.form_submit_button("Login") and st.text_input("Pass", type="password") == "clinicadmin786":
                st.session_state.update({"logged_in":True, "role":"D"})
                st.rerun()

# --- 3. MAIN ---
else:
    st.sidebar.markdown(f"**Patient:** {st.session_state.get('name', 'Admin')}")
    if st.session_state.get('role') == 'P':
        st.sidebar.markdown(f"**Age:** {st.session_state.get('age')}")
    
    st.sidebar.markdown("### 🕒 Clinic Timings")
    st.sidebar.markdown("<div class='timing-card'><b>Mon-Sat:</b> 11AM-2PM & 6PM-8PM<br><b>Sun:</b> 11AM-2PM</div>", unsafe_allow_html=True)
    
    if st.sidebar.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.rerun()

    df = conn.read(ttl=0)
    blocked_dates = df[df['Type'] == "BLOCK"]['Details'].tolist() if not df.empty else []

    if st.session_state.role == "D":
        st.title("👨‍⚕️ Admin Dashboard")
        t_adm = st.tabs(["Submissions", "Manage Availability"])
        with t_adm[0]:
            if not df.empty:
                for i, row in df.sort_values(by='Timestamp', ascending=False).iterrows():
                    if row['Type'] == "BLOCK": continue
                    with st.expander(f"{row['Name']} - {row['Timestamp']}"):
                        st.write(f"**Type:** {row.get('Type','')} | **Details:** {row.get('Details','')}")
                        if 'Attachment' in row and str(row['Attachment']) != "nan": show_img(row['Attachment'])
        with t_adm[1]:
            st.subheader("📅 Block Dates")
            block_dt = st.date_input("Select Date", min_value=date.today())
            if st.button("Block Date"):
                new = pd.DataFrame([{"Name":"ADMIN","Type":"BLOCK","Details":str(block_dt),"Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                conn.update(data=pd.concat([df, new], ignore_index=True)); st.rerun()

    else:
        m = st.sidebar.radio("Menu", ["Vitals", "Vaccines & Screening", "Diet & Yoga", "Reports", "Booking"])
        
        if m == "Vaccines & Screening":
            st.header("💉 Preventive Care")
            if "PCOS" in st.session_state.stat:
                st.subheader("Gynae Wellness")
                st.write("**1. HPV Vaccination:** Recommended to prevent cervical cancer. Usually 3 doses (0, 1, 6 months).")
                st.write("**2. Pap Smear Test:** Screening for cervical health. Recommended every 3 years for women aged 21-65.")
                
            else:
                st.info("T-Dap: 27-36 weeks | Flu: Anytime | Tetanus: Confirmation")

        elif m == "Diet & Yoga":
            st.header("🥗 Nutrition & Lifestyle")
            if "PCOS" in st.session_state.stat:
                v, nv = st.tabs(["Vegetarian Diet", "Non-Vegetarian Diet"])
                with v:
                    st.write("**Breakfast:** Oats with seeds/nuts or Moong Dal Chilla.")
                    st.write("**Lunch:** Brown rice/Multigrain roti with dal and leafy vegetables.")
                    st.write("**Dinner:** Soya chunks or Paneer stir-fry with broccoli.")
                with nv:
                    st.write("**Breakfast:** Boiled eggs (2) with sautéed spinach.")
                    st.write("**Lunch:** Grilled Chicken/Fish with a large salad and quinoa.")
                    st.write("**Dinner:** Lean meat soup or Grilled fish with asparagus.")
                st.warning("Limit: Sugar, Maida, and Processed snacks.")
                
            else:
                st.write("Balanced Trimester-wise Diet with Folic Acid, Iron, and Calcium.")

        elif m == "Booking":
            st.header("📅 Appointment")
            sel_dt = st.date_input("Date", min_value=date.today())
            if str(sel_dt) in blocked_dates: st.error("Clinic Closed")
            else:
                with st.form("b_f"):
                    # Generate 15-min slots
                    slots = []
                    curr = datetime.strptime("11:00", "%H:%M")
                    while curr <= datetime.strptime("13:45", "%H:%M"):
                        slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    if sel_dt.weekday() != 6: # Evening slots if not Sunday
                        curr = datetime.strptime("18:00", "%H:%M")
                        while curr <= datetime.strptime("19:45", "%H:%M"):
                            slots.append(curr.strftime("%I:%M %p")); curr += timedelta(minutes=15)
                    
                    tm = st.selectbox("15-Min Slot", slots)
                    if st.form_submit_button("Confirm"):
                        new = pd.DataFrame([{"Name":f"{st.session_state.name} (Age: {st.session_state.age})","Type":"APP","Details":f"{sel_dt} {tm}","Timestamp":datetime.now().strftime("%Y-%m-%d %H:%M")}])
                        conn.update(data=pd.concat([df, new], ignore_index=True)); st.success("Booked!")
