import sys
from pathlib import Path

import streamlit as st

# Ensure package imports work when run via `streamlit run` directly
ROOT = Path(__file__).resolve().parent
if str(ROOT.parent) not in sys.path:
    sys.path.append(str(ROOT.parent))

from step_validation.embeddings import load_dinov2_model
from step_validation.process_manager import ProcessManager
from step_validation.ui_operation import render_operation_ui
from step_validation.ui_training import render_training_ui


st.set_page_config(layout="wide", page_title="Action Sequence Trainer")

st.markdown("""
<style>
    .element-container {
        transition: none !important;
    }
    [data-testid="stMarkdownContainer"] {
        transition: none !important;
    }
</style>
""", unsafe_allow_html=True)

manager = ProcessManager()

with st.spinner("Loading DINOv2 model..."):
    load_dinov2_model()

st.sidebar.title("System Mode")
mode = st.sidebar.radio("Select Phase:", ["Training (Teach)", "Operation (Monitor)"])

if mode == "Training (Teach)":
    render_training_ui(manager)
else:
    render_operation_ui(manager)
