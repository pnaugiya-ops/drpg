import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="GynaeCare Portal", page_icon="🤰")

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 GynaeCare Patient Portal")

# Patient Info
name = st.text_input("Patient Name")
is_pregnant = st.radio("Are you currently pregnant?", ("No", "Yes"))

# Pregnancy Logic
edd_str = ""
gestation_str = ""

if is_pregnant == "Yes":
    lmp_date = st.date_input("Select your LMP (Last Menstrual Period)", value=datetime.now())
    
    # 1. Calculate EDD (Naegele's Rule: LMP + 280 days)
    edd = lmp_date + timedelta(days=280)
    edd_str = edd.strftime("%d %B %Y")
    
    # 2. Calculate Gestational Age
    today = datetime.now().date()
    diff = today - lmp_date
    weeks = diff.days // 7
    days = diff.days % 7
    gestation_str = f"{weeks} Weeks, {days} Days"
    
    # Display results to patient
    st.success(f"🗓️ **Estimated Due Date:** {edd_str}")
    st.info(f"🤰 **Current Gestational Age:** {gestation_str}")

# Other Vitals
bp = st.text_input("Blood Pressure (e.g. 120/80)")

if st.button("Submit Data"):
    if name:
        try:
            existing_data = conn.read(ttl=0)
            new_row = pd.DataFrame([{
                "Name": name,
                "Pregnant": is_pregnant,
                "EDD": edd_str,
                "Gestation": gestation_str,
                "BP": bp,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons()
            st.write("Data saved successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
