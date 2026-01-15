import streamlit as st
from utils import config

st.set_page_config(page_title="TSAS Control Panel", layout="centered")

st.title("🧠🛡️ TSAS Control Panel")

st.markdown("Control live parameters for the TSAS 3D simulation.")

st.divider()

# Simulation Control
config.SIMULATION_RUNNING = st.toggle(
    "Simulation Running",
    value=config.SIMULATION_RUNNING
)

# Threat Parameters
st.subheader("Threat Parameters")

config.INTENT = st.slider(
    "Hostile Intent Probability",
    0.0, 1.0, config.INTENT
)

config.SIGNAL = st.slider(
    "Signal Strength",
    0.0, 1.0, config.SIGNAL
)

config.SPEED_SCALE = st.slider(
    "Speed Scaling",
    0.1, 2.0, config.SPEED_SCALE
)

st.divider()

st.success("Changes apply instantly to the 3D TSAS simulation")
