import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- 1. SECURE API CONFIGURATION ---
# In Streamlit Cloud, go to Settings -> Secrets and add: GOOGLE_API_KEY = "your_key"
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")

# --- 2. THE MASTER PROMPT ENGINE (v7.0) ---
SYSTEM_INSTRUCTION = """
You are the Lead Market Research Scientist for the DFW Dental Market. 
Entity: AD&I/DDS (combined internal entity).
Logic: Search for bundled pricing (Sedation, CBCT, Grafting). 
Output: Generate two tables: 
1. Table 1: Competitive Matrix (Economy, Econ Low, Econ High).
2. Appendix: Personnel & Capacity (Specialist Names, Formula Sum, Visual Source).
HLRL Rules: Respect user-provided permanent price overrides.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- 3. UI/UX INTERFACE ---
st.set_page_config(page_title="AD&I Market Strategist", layout="wide")

st.title("Welcome back, AD&I.")
st.subheader("DFW Competitor Intelligence Engine")

# HLRL Persistent State
if 'hlrl_locks' not in st.session_state:
    st.session_state.hlrl_locks = {}

query = st.text_input("Where do you need Competitors analysis?", placeholder="Enter ZIP code or DFW Neighborhood")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("🔄 Run Analysis"):
        if query:
            # Combine current query with any HLRL locked data
            prompt = f"Analyze competitors in {query}. Use these HLRL overrides: {st.session_state.hlrl_locks}"
            response = model.generate_content(prompt)
            st.markdown(response.text)
        else:
            st.warning("Please enter a location.")

# --- 4. HLRL OVERRIDE PANEL ---
with st.sidebar:
    st.header("🛠️ HLRL Data Lock")
    st.write("Manually override and lock a price point.")
    comp_name = st.text_input("Competitor Name")
    target_tier = st.selectbox("Tier", ["Economy", "Econ Low", "Econ High"])
    fixed_price = st.text_input("Verified Price")
    
    if st.button("Lock Price Permanently"):
        st.session_state.hlrl_locks[f"{comp_name}_{target_tier}"] = fixed_price
        st.success(f"Locked {comp_name} {target_tier} at {fixed_price}")
