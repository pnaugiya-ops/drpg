import streamlit as st
from datetime import datetime, timedelta

# 1. Setup the Page
st.set_page_config(page_title="GynaeCare Portal", page_icon="🤰")

# 2. App Title and Welcome
st.title("🏥 GynaeCare Patient Portal")
st.write("Welcome, Dr. Naugaiya's Patient. Please fill in your details.")

# 3. Basic Information
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=18, max_value=100, step=1)

# 4. The "Are you Pregnant?" Branch
is_pregnant = st.radio("Are you currently pregnant?", ("Select an option", "Yes", "No"))

if is_pregnant == "Yes":
    st.header("🌟 Pregnancy Tracker")
    lmp_date = st.date_input("Select your Last Menstrual Period (LMP) date")
    
    if lmp_date:
        # Medical calculation: EDD is LMP + 280 days
        edd = lmp_date + timedelta(days=280)
        today = datetime.now().date()
        days_pregnant = (today - lmp_date).days
        weeks = days_pregnant // 7
        
        st.success(f"**Your Estimated Due Date (EDD):** {edd.strftime('%d %B %Y')}")
        st.info(f"**Current Stage:** Week {weeks}")
        
        # We will add Trimester specific diet charts here later!

elif is_pregnant == "No":
    st.header("🌸 Women's Health Tracker")
    st.write("We will track your cycle and general health here.")
    # We will add the Cycle Calculator here later!

# 5. Vitals (Common for both)
if is_pregnant != "Select an option":
    st.divider()
    st.subheader("🌡️ Log Your Vitals")
    col1, col2 = st.columns(2)
    with col1:
        bp = st.text_input("Blood Pressure (e.g., 120/80)")
        weight = st.number_input("Weight (kg)", step=0.1)
    with col2:
        pulse = st.number_input("Pulse Rate", step=1)
        sugar = st.text_input("Blood Sugar (optional)")

    if st.button("Save and Submit"):
        if name:
            st.balloons()
            st.success(f"Thank you {name}. Your data has been recorded for the Doctor.")
        else:
            st.error("Please enter your name before submitting.")
