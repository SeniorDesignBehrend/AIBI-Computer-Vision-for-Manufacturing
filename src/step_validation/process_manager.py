import streamlit as st
import numpy as np

from .models import ActionStep


class ProcessManager:
    def __init__(self):
        if "steps" not in st.session_state:
            st.session_state.steps = []
        if "current_op_step" not in st.session_state:
            st.session_state.current_op_step = 0
        if "training_finalized" not in st.session_state:
            st.session_state.training_finalized = False
        if "run_log" not in st.session_state:
            st.session_state.run_log = []

    def add_step(self, name: str) -> None:
        new_order = len(st.session_state.steps)
        st.session_state.steps.append(ActionStep(name=name, order=new_order))
        st.session_state.training_finalized = False

    def get_steps(self):
        return st.session_state.steps

    def clear_steps(self) -> None:
        st.session_state.steps = []
        st.session_state.current_op_step = 0
        st.session_state.training_finalized = False
        st.session_state.run_log = []

    def finalize_training(self) -> None:
        for step in st.session_state.steps:
            if step.centroids:
                mean_emb = np.mean(step.centroids, axis=0)
                norm = np.linalg.norm(mean_emb)
                step.centroid = mean_emb / norm if norm > 0 else mean_emb
        st.session_state.training_finalized = True
