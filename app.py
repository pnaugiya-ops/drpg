import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GynaeCare Portal")

# THE FIX: Tell the connection to use the Service Account specifically
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Patient Portal")
name = st.text_input("Patient Name")
bp = st.text_input("Blood Pressure")

if st.button("Submit Data"):
    if name and bp:
        try:
            # 1. Read existing data
            # The 'ttl=0' forces it to look at the sheet live every time
            existing_data = conn.read(ttl=0)
            
            # 2. Create new row
            new_row = pd.DataFrame([{
                "Name": name, 
                "BP": bp, 
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            
            # 3. Combine and Update
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            
            st.balloons()
            st.success("Successfully saved to your private clinical sheet!")
        except Exception as e:
            st.error(f"Technical Error: {e}")
    else:
        st.error("Please fill in both Name and BP.")
