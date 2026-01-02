import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="GynaeCare Clinical Portal", page_icon="🤰")

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 GynaeCare Patient Portal")
st.markdown("---")

# 1. Basic Information
name = st.text_input("Patient Name")
is_pregnant = st.radio("Are you currently pregnant?", ("No", "Yes"))

if is_pregnant == "Yes":
    lmp_date = st.date_input("Last Menstrual Period (LMP)", value=datetime.now())
    
    # CALCULATIONS
    edd = lmp_date + timedelta(days=280)
    today = datetime.now().date()
    diff = today - lmp_date
    weeks = diff.days // 7
    days = diff.days % 7
    
    st.subheader(f"Progress: {weeks} Weeks, {days} Days")
    st.info(f"📅 **Estimated Due Date:** {edd.strftime('%d %B %Y')}")

    # 2. SMART TRACKING LOGIC
    st.markdown("### 📋 Clinical Guidance for your Stage")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**💉 Upcoming Vaccinations**")
        if weeks < 27:
            st.write("- Routine Flu Shot (Anytime)")
        elif 27 <= weeks <= 36:
            st.warning("- **Tdap Vaccine Due Now** (Best between 27-36 weeks)")
        else:
            st.write("- Check if Tdap was completed")

    with col2:
        st.write("**🧪 Required Blood Tests**")
        if weeks < 13:
            st.write("- First Trimester Screening (NT Scan)")
            st.write("- CBC, Blood Group, HIV/VDRL")
        elif 13 <= weeks < 24:
            st.write("- Anatomy Scan (TIFFA)")
        elif 24 <= weeks < 28:
            st.error("- **OGTT Due** (Sugar Test)")
        else:
            st.write("- Repeat Hemoglobin & Growth Scan")

    # 3. DIET & FAQ
    with st.expander("🍏 Your Diet Chart"):
        if weeks < 13:
            st.write("**1st Trimester:** Focus on Folic Acid (Spinach, Beans). Small frequent meals to manage nausea.")
        else:
            st.write("**2nd & 3rd Trimester:** Increase Protein (Eggs, Dal) and Iron. 300 extra calories daily.")

    with st.expander("❓ Common FAQs"):
        st.write("**Q: Is spotting normal?**")
        st.write("A: Mild spotting can happen, but always inform the doctor immediately.")
        st.write("**Q: Which side should I sleep on?**")
        st.write("A: Sleeping on your left side is best for blood flow to the baby.")

# 4. Save to Google Sheets
st.markdown("---")
bp = st.text_input("Blood Pressure (e.g., 120/80)")
weight = st.number_input("Current Weight (kg)", min_value=0.0)

if st.button("Submit to Clinic"):
    if name:
        try:
            existing_data = conn.read(ttl=0)
            new_row = pd.DataFrame([{
                "Name": name,
                "Weeks": weeks if is_pregnant == "Yes" else "N/A",
                "EDD": edd.strftime('%Y-%m-%d') if is_pregnant == "Yes" else "N/A",
                "BP": bp,
                "Weight": weight,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons()
            st.success("Record saved. See you at your next appointment!")
        except Exception as e:
            st.error(f"Save Error: {e}")
