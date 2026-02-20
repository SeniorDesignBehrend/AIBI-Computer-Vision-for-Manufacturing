import time

import cv2
import streamlit as st

from .embeddings import get_embedding
from .process_manager import ProcessManager
from .serialization import deserialize_process, serialize_process


def render_training_ui(manager: ProcessManager) -> None:
    st.title("Phase 1: Teach the Process")

    with st.expander("Load Saved Process", expanded=not bool(manager.get_steps())):
        uploaded = st.file_uploader("📂 Load Saved Process (.pkl)", type=["pkl"],
                                    key="train_uploader")
        if uploaded is not None:
            file_id = f"{uploaded.name}_{uploaded.size}"
            if st.session_state.get("_last_uploaded_id") != file_id:
                loaded_steps = deserialize_process(uploaded.read())
                st.session_state.steps = loaded_steps
                st.session_state.training_finalized = True
                st.session_state.current_op_step = 0
                st.session_state._last_uploaded_id = file_id
                st.rerun()

    with st.expander("1. Define Process Steps", expanded=True):
        with st.form("add_step_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            new_step_name = col1.text_input("New Step Name (e.g., 'Jack up Car')")
            submitted = col2.form_submit_button("Add Step")
            if submitted and new_step_name:
                manager.add_step(new_step_name)
                st.success(f"Added: {new_step_name}")
                st.rerun()

        steps = manager.get_steps()
        if steps:
            st.write("**Current Steps:**")
            for i, step in enumerate(steps):
                col_name, col_del = st.columns([4, 1])
                col_name.write(f"{i+1}. {step.name}")
                if col_del.button("🗑️", key=f"del_{i}", type="secondary"):
                    del st.session_state.steps[i]
                    for j, s in enumerate(st.session_state.steps):
                        s.order = j
                    st.session_state.training_finalized = False
                    st.rerun()

    steps = manager.get_steps()
    if not steps:
        return

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

    st.write("**Recorded frames per step:**")
    for s in steps:
        label = "finalized" if s.centroid is not None else f"{len(s.centroids)} frames"
        st.caption(f"- {s.name}: {label}")

    all_have_data = all(len(s.centroids) > 0 for s in steps)
    if all_have_data:
        if st.button("✅ Finalize Training", type="primary"):
            manager.finalize_training()
            st.success("Training finalized! Centroids computed and normalized. Switch to Operation mode.")
    else:
        st.info("Record at least one frame per step before finalizing.")

    if st.session_state.get("training_finalized"):
        st.markdown("---")
        process_bytes = serialize_process(steps)
        st.download_button("💾 Save Process", data=process_bytes,
                           file_name="process.pkl", mime="application/octet-stream")

    cap = cv2.VideoCapture(0)

    while cap.isOpened() and not st.session_state.get("recording"):
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_placeholder.image(frame_rgb, caption="Live Feed (Idle)", use_container_width=True)
        time.sleep(0.03)
        if st.session_state.get("recording"):
            break

    while st.session_state.get("recording"):
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
