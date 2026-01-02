import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GynaeCare Portal")

# Connect
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Patient Portal Test")

name = st.text_input("Patient Name")
bp = st.text_input("Blood Pressure")

if st.button("Submit Data"):
    if name:
        # Create a tiny table with the new info
        new_row = pd.DataFrame([{"Name": name, "BP": bp, "Time": str(datetime.now())}])
        
        # This line forces the app to WRITE to the sheet
        conn.create(data=new_row)
        
        st.success(f"Sent to Google Sheet! Check your sheet now, Dr.")
    else:
        st.error("Enter a name first.")
