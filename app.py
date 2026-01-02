import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GynaeCare Portal")

# 1. Connect using the Secrets we set up
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Patient Portal")

# 2. Simple Inputs
name = st.text_input("Patient Name")
bp = st.text_input("Blood Pressure")

if st.button("Submit Data"):
    if name:
        # 3. Get the existing data from your sheet
        # This is the "Handshake"
        try:
            existing_data = conn.read()
        except:
            # If the sheet is totally empty, create a starting point
            existing_data = pd.DataFrame(columns=["Name", "BP", "Time"])
        
        # 4. Prepare the new row
        new_row = pd.DataFrame([{"Name": name, "BP": bp, "Time": str(datetime.now())}])
        
        # 5. Combine them
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # 6. Push back to Google Sheets
        conn.update(data=updated_df)
        
        st.balloons()
        st.success("Success! The data is now in your Google Sheet.")
    else:
        st.error("Please enter a name.")
