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
        try:
            # 3. Read what's already there
            existing_data = conn.read()
            
            # 4. Create the new row
            new_row = pd.DataFrame([{"Name": name, "BP": bp, "Time": str(datetime.now())}])
            
            # 5. Add the new row to the old data
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            
            # 6. Save it back to Google
            conn.update(data=updated_df)
            
            st.balloons()
            st.success("Success! The data is now in your Google Sheet.")
        
        except Exception as e:
            st.error("Connection Error. Please ensure your Google Sheet has 'Anyone with link can Edit' permission.")
    else:
        st.error("Please enter a name.")
