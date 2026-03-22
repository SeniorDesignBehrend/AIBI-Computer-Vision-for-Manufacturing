from collections import defaultdict

import numpy as np
import streamlit as st

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
        if "recorded_segments" not in st.session_state:
            st.session_state.recorded_segments = []
        if "training_phase" not in st.session_state:
            st.session_state.training_phase = "record"

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

    def clear_training_state(self) -> None:
        st.session_state.recorded_segments = []
        st.session_state.training_phase = "record"
        st.session_state.training_finalized = False

    def finalize_training(self) -> None:
        for step in st.session_state.steps:
            if step.centroids:
                mean_emb = np.mean(step.centroids, axis=0)
                norm = np.linalg.norm(mean_emb)
                step.centroid = mean_emb / norm if norm > 0 else mean_emb
        st.session_state.training_finalized = True

    def finalize_training_from_segments(self, segments: list) -> None:
        from .embeddings import get_embedding

        label_to_frames: dict[str, list] = defaultdict(list)
        label_order: list[str] = []
        for seg in segments:
            if seg["label"] and seg["frames"]:
                if seg["label"] not in label_order:
                    label_order.append(seg["label"])
                label_to_frames[seg["label"]].extend(seg["frames"])

        steps = []
        for idx, label in enumerate(label_order):
            embeddings = [get_embedding(f) for f in label_to_frames[label]]
            mean_emb = np.mean(embeddings, axis=0)
            norm = np.linalg.norm(mean_emb)
            step = ActionStep(name=label, order=idx)
            step.centroid = mean_emb / norm if norm > 0 else mean_emb
            steps.append(step)

        st.session_state.steps = steps
        st.session_state.training_finalized = True
        st.session_state.recorded_segments = []
        st.session_state.training_phase = "record"
