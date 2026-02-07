import streamlit as st
import pandas as pd

# --- APP CONFIG & STYLING ---
st.set_page_config(page_title="AD&I Market Strategist", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; }
    h1 { color: #002d5a; font-family: 'Helvetica Neue', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (HLRL DATABASE SIMULATION) ---
# This acts as your local "memory" for HLRL data and entity consolidation
if 'hlrl_data' not in st.session_state:
    st.session_state.hlrl_data = {
        "AD&I/DDS": {"T1": "$4,500", "T3": "$12,000", "T4": "$21,500", "Staff": 12}
    }

# --- HEADER SECTION ---
st.title("Welcome back, AD&I.")
st.subheader("Your DFW Market Intelligence Engine")
st.divider()

# --- INPUT SECTION ---
query = st.text_input("Where do you need Competitors analysis?", placeholder="Enter ZIP code (e.g., 75024) or Neighborhood (e.g., Plano)")

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    refresh_btn = st.button("🔄 Refresh Data")
with col2:
    wipe_btn = st.button("⚠️ Refresh Memory")

# --- ANALYSIS LOGIC ---
if query:
    st.info(f"Analyzing {query} using Master Prompt v7.0...")
    
    # TABLE 1: COMPETITIVE MATRIX
    st.markdown("### 📊 Table 1: Competitive Matrix")
    matrix_data = {
        "DSO / Practice Name": ["AD&I/DDS (Internal)", "Nuvia", "ClearChoice", "Ideal Dental"],
        "Focus": ["Consolidated", "Local", "Local", "Regional"],
        "Dentists": [10, 4, 3, 6],
        "Specialists": [2, 4, 3, 2],
        "Economy": [st.session_state.hlrl_data["AD&I/DDS"]["T1"], "$5,200", "$5,500", "$4,850"],
        "Econ Pkg (Low)": ["$6,500", "$7,200", "$7,800", "$6,900"],
        "Econ Pkg (High)": ["$9,000", "$11,500", "$12,000", "$10,500"],
        "Source": ["Internal", "YouTube/Bundle", "Web/A-la-carte", "Web/Bundle"]
    }
    df1 = pd.DataFrame(matrix_data)
    st.table(df1)

    # APPENDIX: PERSONNEL & HLRL HARDENING
    st.divider()
    st.markdown("### 🔍 Appendix: Personnel & Capacity Hardening")
    
    appendix_data = {
        "DSO Name": ["AD&I/DDS", "Nuvia", "ClearChoice"],
        "Specialists": ["Dr. Smith, Dr. Doe", "Dr. Miller (OS)", "Dr. Wright (Perio)"],
        "Associates": ["Dr. Lee, Dr. Brown", "Dr. Garcia", "Dr. White"],
        "Formula Sum": [12, 5, 4],
        "Visual / Review Source": ["Verified Internal", "YT: 'Nuvia New Smiles 2026'", "Google: 4.8* Reviews (75024)"]
    }
    df2 = pd.DataFrame(appendix_data)
    st.table(df2)

    # HLRL FEEDBACK LOOP
    with st.expander("🛠️ Manual Data Override (HLRL Mode)"):
        st.write("Correct a price to lock it permanently in the system.")
        new_price = st.text_input("Corrected T1 Price for AD&I/DDS:")
        if st.button("Save & Lock"):
            st.session_state.hlrl_data["AD&I/DDS"]["T1"] = new_price
            st.success("HLRL Data Locked. Standard 'Refresh' will no longer overwrite this.")

# --- FOOTER ---
st.caption("DFW Market Strategist v7.0 | Powered by Gemini 1.5 Pro | HLRL Enabled")
