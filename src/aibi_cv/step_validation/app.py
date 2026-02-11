import pickle
import streamlit as st
import cv2
import numpy as np
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional

import torch
import torchvision.transforms as T
from PIL import Image


# --- 1. Verification State Machine ---

class VerificationState(Enum):
    IDLE         = auto()  # No confident match for any step
    CORRECT_STEP = auto()  # Current step detected, building window votes
    CONFIRMED    = auto()  # Window vote threshold met — step complete
    WRONG_ORDER  = auto()  # A past step re-detected
    SKIPPED      = auto()  # A future step detected before current is confirmed
    COMPLETE     = auto()  # All steps finished


# --- 2. Data Model ---

@dataclass
class ActionStep:
    name: str
    order: int
    centroids: List[np.ndarray] = field(default_factory=list)  # raw training embeddings
    centroid: Optional[np.ndarray] = None                       # finalized normalized centroid


class ProcessManager:
    def __init__(self):
        if 'steps' not in st.session_state:
            st.session_state.steps = []
        if 'current_op_step' not in st.session_state:
            st.session_state.current_op_step = 0
        if 'training_finalized' not in st.session_state:
            st.session_state.training_finalized = False
        if 'run_log' not in st.session_state:
            st.session_state.run_log = []

    def add_step(self, name):
        new_order = len(st.session_state.steps)
        st.session_state.steps.append(ActionStep(name=name, order=new_order))
        st.session_state.training_finalized = False

    def get_steps(self):
        return st.session_state.steps

    def clear_steps(self):
        st.session_state.steps = []
        st.session_state.current_op_step = 0
        st.session_state.training_finalized = False
        st.session_state.run_log = []

    def finalize_training(self):
        """Average all captured embeddings per step and L2-normalize into one centroid."""
        for step in st.session_state.steps:
            if step.centroids:
                mean_emb = np.mean(step.centroids, axis=0)
                norm = np.linalg.norm(mean_emb)
                step.centroid = mean_emb / norm if norm > 0 else mean_emb
        st.session_state.training_finalized = True


def serialize_process(steps) -> bytes:
    return pickle.dumps(steps)


def deserialize_process(data: bytes) -> list:
    return pickle.loads(data)


# --- 3. Embedding Extraction ---

@st.cache_resource
def load_dinov2_model():
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14')
    model.eval()
    return model

transform = T.Compose([
    T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
])

def get_embedding(frame):
    """Extract DINOv2 embedding and L2-normalize it (makes dot product == cosine sim)."""
    model = load_dinov2_model()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    with torch.no_grad():
        img_tensor = transform(pil_image).unsqueeze(0)
        embedding = model(img_tensor).squeeze().cpu().numpy()
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding


# --- 4. Similarity & State Logic ---

def calculate_similarity(embedding, steps, threshold):
    """
    Compare embedding to finalized step centroids using dot product (== cosine sim
    since both are L2-normalized).

    Returns (best_match_idx, best_similarity).
    Returns (-1, score) when best score is below threshold — treated as IDLE.
    """
    best_match_idx = -1
    best_similarity = -1.0

    for i, step in enumerate(steps):
        if step.centroid is None:
            continue
        similarity = float(np.dot(embedding, step.centroid))
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_idx = i

    if best_similarity < threshold:
        return -1, best_similarity
    return best_match_idx, best_similarity


def get_verification_state(detected_idx, current_idx, num_steps, window, required_votes):
    """
    Derive the current VerificationState from the sliding window.

      - COMPLETE     if all steps already confirmed
      - IDLE         if detected_idx == -1 (below similarity threshold)
      - SKIPPED      if detected step is ahead of expected
      - WRONG_ORDER  if detected step is behind expected
      - CONFIRMED    if window has enough votes for current_idx
      - CORRECT_STEP otherwise (still accumulating votes)
    """
    if current_idx >= num_steps:
        return VerificationState.COMPLETE

    if detected_idx == -1:
        return VerificationState.IDLE

    if detected_idx > current_idx:
        return VerificationState.SKIPPED

    if detected_idx < current_idx:
        return VerificationState.WRONG_ORDER

    # detected_idx == current_idx
    votes = sum(1 for v in window if v == current_idx)
    if votes >= required_votes:
        return VerificationState.CONFIRMED
    return VerificationState.CORRECT_STEP


# --- 5. UI ---

st.set_page_config(layout="wide", page_title="Action Sequence Trainer")
manager = ProcessManager()

st.sidebar.title("System Mode")
mode = st.sidebar.radio("Select Phase:", ["Training (Teach)", "Operation (Monitor)"])


# ══════════════════════════════════════════════════════════
# PHASE 1: TRAINING
# ══════════════════════════════════════════════════════════
if mode == "Training (Teach)":
    st.title("Phase 1: Teach the Process")

    with st.expander("1. Define Process Steps", expanded=True):
        col1, col2 = st.columns([3, 1])
        new_step_name = col1.text_input("New Step Name (e.g., 'Jack up Car')")
        if col2.button("Add Step"):
            if new_step_name:
                manager.add_step(new_step_name)
                st.success(f"Added: {new_step_name}")

    steps = manager.get_steps()
    if steps:
        st.write("### 2. Record Actions")

        video_placeholder = st.empty()

        selected_step_name = st.selectbox("Select Step to Train:", [s.name for s in steps])
        selected_step_idx = next(i for i, s in enumerate(steps) if s.name == selected_step_name)

        col_start, col_stop, col_clear = st.columns(3)
        if col_start.button("🔴 Start Recording"):
            st.session_state.recording = True
            st.session_state.training_finalized = False

        if col_stop.button("⬛ Stop Recording"):
            st.session_state.recording = False
            count = len(steps[selected_step_idx].centroids)
            st.success(f"Saved {count} frames for '{selected_step_name}'")

        if col_clear.button("🗑 Clear Recording"):
            steps[selected_step_idx].centroids = []
            steps[selected_step_idx].centroid = None
            st.session_state.training_finalized = False
            st.success(f"Cleared recording for '{selected_step_name}'")

        # Per-step frame count
        st.write("**Recorded frames per step:**")
        for s in steps:
            if s.centroid is not None:
                label = "finalized"
            else:
                label = f"{len(s.centroids)} frames"
            st.caption(f"- {s.name}: {label}")

        # Finalize button — only show when every step has at least one frame
        all_have_data = all(len(s.centroids) > 0 for s in steps)
        if all_have_data:
            if st.button("✅ Finalize Training", type="primary"):
                manager.finalize_training()
                st.success("Training finalized! Centroids computed and normalized. Switch to Operation mode.")
        else:
            st.info("Record at least one frame per step before finalizing.")

        # Save / Load process
        st.markdown("---")
        col_save, col_load = st.columns(2)
        with col_save:
            if st.session_state.get('training_finalized'):
                process_bytes = serialize_process(steps)
                st.download_button("💾 Save Process", data=process_bytes,
                                   file_name="process.pkl", mime="application/octet-stream")
            else:
                st.caption("Finalize training to enable save.")
        with col_load:
            uploaded = st.file_uploader("📂 Load Saved Process", type=["pkl"],
                                        label_visibility="collapsed")
            if uploaded is not None:
                loaded_steps = deserialize_process(uploaded.read())
                st.session_state.steps = loaded_steps
                st.session_state.training_finalized = True
                st.session_state.current_op_step = 0
                st.rerun()

        # Camera feed
        cap = cv2.VideoCapture(0)

        while cap.isOpened() and not st.session_state.get('recording'):
            ret, frame = cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame_rgb, caption="Live Feed (Idle)", use_container_width=True)
            time.sleep(0.03)
            if st.session_state.get('recording'):
                break

        while st.session_state.get('recording'):
            ret, frame = cap.read()
            if not ret:
                break

            emb = get_embedding(frame)
            steps[selected_step_idx].centroids.append(emb)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.putText(frame_rgb, f"RECORDING: {selected_step_name}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 50, 50), 2)
            video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            time.sleep(0.1)

        cap.release()


# ══════════════════════════════════════════════════════════
# PHASE 2: OPERATION
# ══════════════════════════════════════════════════════════
elif mode == "Operation (Monitor)":
    st.title("Phase 2: Sequence Verification")

    # Sidebar verification parameters
    st.sidebar.markdown("---")
    st.sidebar.subheader("Verification Parameters")
    SIMILARITY_THRESHOLD = st.sidebar.slider(
        "Similarity Threshold", 0.50, 1.0, 0.75, 0.01,
        help="Minimum cosine similarity to count a frame as a match. Below this = IDLE."
    )
    WINDOW_SIZE = st.sidebar.slider(
        "Window Size (frames)", 5, 30, 10, 1,
        help="Number of recent frames kept for sliding-window voting."
    )
    REQUIRED_VOTES = st.sidebar.slider(
        "Required Votes", 1, WINDOW_SIZE, max(1, int(WINDOW_SIZE * 0.7)), 1,
        help="Votes needed within the window to confirm a step."
    )

    steps = manager.get_steps()

    if not steps:
        st.warning("No process defined. Please go to Training mode first.")
    elif not st.session_state.get('training_finalized'):
        st.warning("Training not finalized. Go to Training mode and click **Finalize Training**.")
    else:
        col_restart, _ = st.columns([1, 4])
        if col_restart.button("↺ Restart Observation"):
            st.session_state.current_op_step = 0
            st.rerun()

        current_idx = st.session_state.current_op_step

        # Progress bar
        progress = current_idx / len(steps)
        st.progress(progress)

        expected_label = steps[current_idx].name if current_idx < len(steps) else "COMPLETE"
        st.subheader(f"Expecting: Step {current_idx + 1} — {expected_label}")

        # Step checklist
        for i, s in enumerate(steps):
            if i < current_idx:
                st.markdown(f"✅ ~~Step {i+1}: {s.name}~~")
            elif i == current_idx:
                st.markdown(f"**▶ Step {i+1}: {s.name}** ← current")
            else:
                st.markdown(f"⬜ Step {i+1}: {s.name}")

        video_loc = st.empty()
        status_loc = st.empty()

        # State → overlay color (BGR for OpenCV)
        STATE_COLORS = {
            VerificationState.IDLE:         (180, 180, 180),
            VerificationState.CORRECT_STEP: (100, 200,   0),
            VerificationState.CONFIRMED:    (  0, 255,   0),
            VerificationState.WRONG_ORDER:  (  0, 165, 255),
            VerificationState.SKIPPED:      (  0,   0, 255),
            VerificationState.COMPLETE:     (  0, 255,   0),
        }

        if st.button("Start Monitoring"):
            cap = cv2.VideoCapture(0)
            window = deque(maxlen=WINDOW_SIZE)
            run_record = {
                'run': len(st.session_state.run_log) + 1,
                'started': datetime.now().strftime("%H:%M:%S"),
                'completed': False,
                'steps': [],
            }
            current_step_warnings = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Embed → match → vote
                emb = get_embedding(frame)
                detected_idx, conf = calculate_similarity(emb, steps, SIMILARITY_THRESHOLD)
                window.append(detected_idx)

                state = get_verification_state(
                    detected_idx, current_idx, len(steps), window, REQUIRED_VOTES
                )

                # State-specific message and side-effects
                if state == VerificationState.IDLE:
                    status_text = "Waiting for action..."

                elif state == VerificationState.CORRECT_STEP:
                    votes = sum(1 for v in window if v == current_idx)
                    status_text = (
                        f"Detecting '{steps[current_idx].name}'... "
                        f"({votes}/{REQUIRED_VOTES})"
                    )

                elif state == VerificationState.CONFIRMED:
                    status_text = f"Step {current_idx + 1} confirmed! Advancing..."
                    run_record['steps'].append({
                        'step': steps[current_idx].name,
                        'result': '✅',
                        'warnings': '; '.join(current_step_warnings) or '—',
                    })
                    current_step_warnings = []
                    st.session_state.current_op_step += 1
                    current_idx += 1
                    window.clear()

                elif state == VerificationState.WRONG_ORDER:
                    past_name = steps[detected_idx].name if detected_idx >= 0 else "unknown"
                    status_text = (
                        f"Warning: '{past_name}' re-detected "
                        f"(expected step {current_idx + 1})"
                    )
                    current_step_warnings.append(f"Re-detected '{past_name}'")

                elif state == VerificationState.SKIPPED:
                    future_name = steps[detected_idx].name
                    status_text = (
                        f"WARNING: Skipped to '{future_name}'! "
                        f"(Expected '{steps[current_idx].name}')"
                    )
                    current_step_warnings.append(f"Skipped to '{future_name}'")

                elif state == VerificationState.COMPLETE:
                    status_text = "Process Complete!"

                # Overlay on frame
                color = STATE_COLORS[state]
                conf_pct = int(conf * 100)
                cv2.putText(frame, status_text, (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
                cv2.putText(frame,
                            f"Conf: {conf_pct}%  Threshold: {int(SIMILARITY_THRESHOLD * 100)}%",
                            (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_loc.image(frame_rgb, use_container_width=True)
                status_loc.markdown(
                    f"**State:** `{state.name}` &nbsp;|&nbsp; **Confidence:** {conf_pct}%"
                )

                if state == VerificationState.COMPLETE:
                    st.success("Process Completed Successfully!")
                    break

            run_record['completed'] = (st.session_state.current_op_step >= len(steps))
            st.session_state.run_log.append(run_record)
            cap.release()

            if st.session_state.current_op_step >= len(steps):
                if st.button("↺ Run Again"):
                    st.session_state.current_op_step = 0
                    st.rerun()

        if st.session_state.get('run_log'):
            with st.expander(f"Run History ({len(st.session_state.run_log)} runs)"):
                for r in reversed(st.session_state.run_log):
                    status = "Complete" if r['completed'] else "Incomplete"
                    st.markdown(f"**Run {r['run']}** — {r['started']} — {status}")
                    if r['steps']:
                        st.dataframe(r['steps'], use_container_width=True)
