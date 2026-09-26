import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="EcoOrbit Dashboard", layout="wide")

st.title("⚡ EcoOrbit: Orbital Data Sustainability Hub")
st.caption("NASA Space Apps Challenge Submission — Earth vs. Space Compute Simulator")

# 2. Sidebar Interactive Sliders
st.sidebar.header("🎛️ Simulation Parameters")
ground_load = st.sidebar.slider(
    "Terrestrial Data Center Load (%)", 
    min_value=0, 
    max_value=100, 
    value=40, 
    help="Adjust percentage of compute running on Earth vs. Low Earth Orbit."
)

space_share = 100 - ground_load

# 3. Dynamic Sustainability Calculations
co2_saved = space_share * 0.85
energy_saved = space_share * 0.62
collision_risk = "LOW" if space_share < 70 else "MODERATE"

# 4. Display Core Metrics Top-Center
col1, col2, col3 = st.columns(3)
col1.metric(label="Estimated CO₂ Reduction", value=f"{co2_saved:.1f}%")
col2.metric(label="Terrestrial Energy Savings", value=f"{energy_saved:.1f}%")
col3.metric(label="Orbital Debris Risk Index", value=collision_risk)

st.markdown("---")

# 5. Visual Interactive Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Compute Load Distribution")
    df_distribution = pd.DataFrame({
        "Location": ["Terrestrial Data Centers", "Orbital Satellites"],
        "Share (%)": [ground_load, space_share]
    })
    fig_pie = px.pie(
        df_distribution, 
        values="Share (%)", 
        names="Location", 
        color_discrete_sequence=["#1C2541", "#00F5D4"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.subheader("Resource Impact Analysis")
    df_impact = pd.DataFrame({
        "Metric": ["CO₂ Reduction (%)", "Energy Savings (%)"],
        "Value": [co2_saved, energy_saved]
    })
    fig_bar = px.bar(
        df_impact, 
        x="Metric", 
        y="Value", 
        color="Metric", 
        color_discrete_sequence=["#00BBF9", "#00F5D4"]
    )
    st.plotly_chart(fig_bar, use_container_width=True)
