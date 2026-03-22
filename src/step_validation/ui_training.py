import os
import tempfile
import time
from pathlib import Path

import cv2
import streamlit as st

from .process_manager import ProcessManager
from .serialization import deserialize_process, serialize_process

SAMPLE_EVERY_N = 3  # keep 1 in N frames when extracting from uploaded video


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

    phase = st.session_state.get("training_phase", "record")
    if phase == "record":
        _render_record_phase(manager)
    else:
        _render_review_phase(manager)


def _render_record_phase(manager: ProcessManager) -> None:
    st.subheader("Step 1: Record a Segment")
    st.caption("Record video of yourself performing one step, then give it a name. Repeat for each step.")

    tab_camera, tab_upload = st.tabs(["Live Camera", "Upload Video File"])

    with tab_camera:
        _render_camera_recording()

    with tab_upload:
        _render_upload_recording()

    segments = st.session_state.get("recorded_segments", [])
    if segments:
        st.markdown("---")
        n = len(segments)
        if st.button(f"Review {n} segment(s) and finalize →", type="primary"):
            st.session_state.training_phase = "review"
            st.rerun()


def _render_camera_recording() -> None:
    video_placeholder = st.empty()

    recording = st.session_state.get("cam_recording", False)

    col_start, col_stop = st.columns(2)
    start_clicked = col_start.button("Start Recording", key="cam_start",
                                     type="primary", disabled=recording)
    stop_clicked = col_stop.button("Stop Recording", key="cam_stop",
                                   disabled=not recording)

    if start_clicked:
        st.session_state.cam_recording = True
        st.session_state._cam_buffer = []
        st.rerun()

    if stop_clicked:
        st.session_state.cam_recording = False
        st.rerun()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Camera not available.")
        return

    if not st.session_state.get("cam_recording"):
        # Idle: show single preview frame
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame_rgb, caption="Live Feed (Idle)", use_container_width=True)

        # If a buffer exists (just stopped), prompt for label
        frames = st.session_state.get("_cam_buffer", [])
        if frames:
            st.info(f"Captured {len(frames)} frames. Name this step to save it.")
            label = st.text_input("Step name (e.g. 'Attach Left Bracket'):", key="cam_label_input")
            col_save, col_discard = st.columns(2)
            if col_save.button("Save Segment", key="cam_save", type="primary"):
                if not label.strip():
                    st.error("Please enter a step name.")
                else:
                    st.session_state.recorded_segments.append({
                        "label": label.strip(),
                        "frames": frames,
                        "source": "camera",
                    })
                    st.session_state._cam_buffer = []
                    st.success(f"Saved '{label.strip()}' ({len(frames)} frames).")
                    st.rerun()
            if col_discard.button("Discard", key="cam_discard"):
                st.session_state._cam_buffer = []
                st.rerun()
        return

    # Active recording loop
    while st.session_state.get("cam_recording"):
        ret, frame = cap.read()
        if not ret:
            break
        st.session_state._cam_buffer.append(frame.copy())

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        n_frames = len(st.session_state._cam_buffer)
        cv2.putText(frame_rgb, f"REC  {n_frames} frames", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (220, 50, 50), 2, cv2.LINE_AA)
        video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
        time.sleep(0.05)

    cap.release()


def _render_upload_recording() -> None:
    uploaded_files = st.file_uploader(
        "Upload video files (.mp4, .avi, .mov, .mkv)",
        type=["mp4", "avi", "mov", "mkv"],
        key="video_uploader",
        accept_multiple_files=True,
    )
    if not uploaded_files:
        return

    if "pending_uploads" not in st.session_state:
        st.session_state.pending_uploads = []

    # Process new uploads
    for uploaded_file in uploaded_files:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        if file_id not in [p["id"] for p in st.session_state.pending_uploads]:
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            cap = cv2.VideoCapture(tmp_path)
            all_frames: list = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                all_frames.append(frame.copy())
            cap.release()
            os.unlink(tmp_path)

            if all_frames:
                frames = [f for idx, f in enumerate(all_frames) if idx % SAMPLE_EVERY_N == 0]
                st.session_state.pending_uploads.append({
                    "id": file_id,
                    "name": uploaded_file.name,
                    "frames": frames,
                    "total_frames": len(all_frames),
                    "label": "",
                })

    # Display all pending uploads
    for i, upload in enumerate(st.session_state.pending_uploads):
        with st.container(border=True):
            col_preview, col_input = st.columns([1, 2])
            with col_preview:
                preview = cv2.cvtColor(upload["frames"][len(upload["frames"]) // 2], cv2.COLOR_BGR2RGB)
                st.image(preview, caption=upload["name"], use_container_width=True)
            with col_input:
                st.caption(f"{len(upload['frames'])} frames sampled from {upload['total_frames']} total")
                upload["label"] = st.text_input("Step name:", value=upload["label"], key=f"upload_label_{i}")

    if st.session_state.pending_uploads:
        if st.button("Save All Uploaded Segments", key="upload_save_all", type="primary"):
            missing_labels = [u["name"] for u in st.session_state.pending_uploads if not u["label"].strip()]
            if missing_labels:
                st.error(f"Please enter step names for: {', '.join(missing_labels)}")
            else:
                for upload in st.session_state.pending_uploads:
                    st.session_state.recorded_segments.append({
                        "label": upload["label"].strip(),
                        "frames": upload["frames"],
                        "source": "upload",
                    })
                st.session_state.pending_uploads = []
                st.success(f"Saved {len(uploaded_files)} segment(s).")
                st.rerun()


def _render_review_phase(manager: ProcessManager) -> None:
    st.subheader("Step 2: Review & Finalize")

    segments = st.session_state.get("recorded_segments", [])

    if not segments:
        st.info("No segments recorded yet.")
        if st.button("← Back to Recording"):
            st.session_state.training_phase = "record"
            st.rerun()
        return

    for i, seg in enumerate(segments):
        with st.container(border=True):
            col_info, col_preview, col_actions = st.columns([3, 2, 1])

            with col_info:
                new_label = st.text_input(
                    "Step name", value=seg["label"] or "",
                    key=f"seg_label_{i}",
                )
                seg["label"] = new_label
                n_frames = len(seg["frames"])
                source_icon = "Camera" if seg["source"] == "camera" else "Upload"
                st.caption(f"{source_icon}  |  {n_frames} frames")

            with col_preview:
                if seg["frames"]:
                    mid = seg["frames"][len(seg["frames"]) // 2]
                    st.image(cv2.cvtColor(mid, cv2.COLOR_BGR2RGB), use_container_width=True)

            with col_actions:
                if st.button("Delete", key=f"seg_del_{i}", type="secondary"):
                    st.session_state.recorded_segments.pop(i)
                    st.rerun()

    st.markdown("---")
    col_back, col_finalize = st.columns([1, 2])

    with col_back:
        if st.button("← Record Another"):
            st.session_state.training_phase = "record"
            st.rerun()

    with col_finalize:
        all_labeled = all(seg["label"] and seg["label"].strip() for seg in segments)
        if not all_labeled:
            st.warning("All segments must have a name before finalizing.")
        else:
            if st.button("Finalize Training", type="primary"):
                with st.spinner("Computing embeddings... this may take a moment."):
                    manager.finalize_training_from_segments(segments)
                st.success("Training complete! Switch to Operation mode.")
                st.rerun()

    if st.session_state.get("training_finalized"):
        steps = manager.get_steps()
        process_bytes = serialize_process(steps)
        st.download_button("💾 Save Process (.pkl)", data=process_bytes,
                           file_name="process.pkl", mime="application/octet-stream")
