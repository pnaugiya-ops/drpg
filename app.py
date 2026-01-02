import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="GynaeCare Portal")
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Patient Portal")
name = st.text_input("Patient Name")
bp = st.text_input("Blood Pressure")

if st.button("Submit Data"):
    if name and bp:
        try:
            # Only sending what the patient types
            new_row = pd.DataFrame([{"Name": name, "BP": bp}])
            
            # Sending it to Google
            conn.update(data=new_row)
            
            st.balloons()
            st.success("It worked! Check your Google Sheet now.")
        except Exception as e:
            st.error(f"Technical Error: {e}")
    else:
        st.error("Please fill in both Name and BP.")
