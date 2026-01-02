import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GynaeCare Portal")

# 1. Connect using the URL in your Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Patient Portal")

name = st.text_input("Patient Name")
bp = st.text_input("Blood Pressure")

if st.button("Submit Data"):
    if name:
        try:
            # 2. Read what's currently in the sheet
            existing_data = conn.read()
            
            # 3. Create the new row
            new_row = pd.DataFrame([{
                "Name": name, 
                "BP": bp, 
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # 4. Add the new row to the bottom of the list
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            
            # 5. Push the whole list back to the Google Sheet
            conn.update(data=updated_df)
            
            st.balloons()
            st.success("Success! The data is now in your Google Sheet.")
        
        except Exception as e:
            st.error("Connection Error. Check if your Google Sheet is set to 'Anyone with link can EDIT'.")
    else:
        st.error("Please enter a name.")
