from collections import deque
from datetime import datetime

import cv2
import streamlit as st

from .embeddings import get_embedding
from .process_manager import ProcessManager
from .state import VerificationState
from .verification import calculate_similarity, get_verification_state


def render_operation_ui(manager: ProcessManager) -> None:
    st.title("Phase 2: Sequence Verification")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Verification Parameters")
    similarity_threshold = st.sidebar.slider(
        "Similarity Threshold", 0.50, 1.0, 0.75, 0.01,
        help="Minimum cosine similarity to count a frame as a match. Below this = IDLE."
    )
    window_size = st.sidebar.slider(
        "Window Size (frames)", 5, 30, 10, 1,
        help="Number of recent frames kept for sliding-window voting."
    )
    required_votes = st.sidebar.slider(
        "Required Votes", 1, window_size, max(1, int(window_size * 0.7)), 1,
        help="Votes needed within the window to confirm a step."
    )

    steps = manager.get_steps()

    if not steps:
        st.warning("No process defined. Please go to Training mode first.")
        return
    if not st.session_state.get("training_finalized"):
        st.warning("Training not finalized. Go to Training mode and click **Finalize Training**.")
        return

    col_restart, _ = st.columns([1, 4])
    if col_restart.button("↺ Restart Observation"):
        st.session_state.current_op_step = 0
        st.rerun()

    current_idx = st.session_state.current_op_step

    progress_loc = st.empty()
    heading_loc = st.empty()
    checklist_loc = st.empty()

    def render_step_ui(idx: int) -> None:
        progress_loc.progress(idx / len(steps))
        expected_label = steps[idx].name if idx < len(steps) else "COMPLETE"
        heading_loc.subheader(f"Expecting: Step {idx + 1} — {expected_label}")
        checklist_md = ""
        for i, s in enumerate(steps):
            if i < idx:
                checklist_md += f"✅ ~~Step {i+1}: {s.name}~~\n\n"
            elif i == idx:
                checklist_md += f"**▶ Step {i+1}: {s.name}** ← current\n\n"
            else:
                checklist_md += f"⬜ Step {i+1}: {s.name}\n\n"
        checklist_loc.markdown(checklist_md)

    render_step_ui(current_idx)

    video_loc = st.empty()
    status_loc = st.empty()

    state_colors = {
        VerificationState.IDLE: (180, 180, 180),
        VerificationState.CORRECT_STEP: (100, 200, 0),
        VerificationState.CONFIRMED: (0, 255, 0),
        VerificationState.WRONG_ORDER: (0, 165, 255),
        VerificationState.SKIPPED: (0, 0, 255),
        VerificationState.COMPLETE: (0, 255, 0),
    }

    if st.button("Start Monitoring"):
        with st.spinner("Opening camera..."):
            cap = cv2.VideoCapture(0)
        window = deque(maxlen=window_size)
        run_record = {
            "run": len(st.session_state.run_log) + 1,
            "started": datetime.now().strftime("%H:%M:%S"),
            "completed": False,
            "steps": [],
        }
        current_step_warnings: list[str] = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            emb = get_embedding(frame)
            detected_idx, conf = calculate_similarity(emb, steps, similarity_threshold)
            window.append(detected_idx)

            state = get_verification_state(
                detected_idx, current_idx, len(steps), window, required_votes
            )

            if state == VerificationState.IDLE:
                status_text = "Waiting for action..."

            elif state == VerificationState.CORRECT_STEP:
                votes = sum(1 for v in window if v == current_idx)
                status_text = (
                    f"Detecting '{steps[current_idx].name}'... "
                    f"({votes}/{required_votes})"
                )

            elif state == VerificationState.CONFIRMED:
                status_text = f"Step {current_idx + 1} confirmed! Advancing..."
                run_record["steps"].append({
                    "step": steps[current_idx].name,
                    "result": "✅",
                    "warnings": "; ".join(current_step_warnings) or "—",
                })
                current_step_warnings = []
                st.session_state.current_op_step += 1
                current_idx += 1
                window.clear()
                render_step_ui(current_idx)

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
                render_step_ui(current_idx)

            color = state_colors[state]
            conf_pct = int(conf * 100)
            cv2.putText(frame, status_text, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
            cv2.putText(frame,
                        f"Conf: {conf_pct}%  Threshold: {int(similarity_threshold * 100)}%",
                        (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_loc.image(frame_rgb, use_container_width=True)
            status_loc.markdown(
                f"**State:** `{state.name}` &nbsp;|&nbsp; **Confidence:** {conf_pct}%"
            )

            if state == VerificationState.COMPLETE:
                st.success("Process Completed Successfully!")
                break

        run_record["completed"] = (st.session_state.current_op_step >= len(steps))
        st.session_state.run_log.append(run_record)
        cap.release()

        if st.session_state.current_op_step >= len(steps):
            if st.button("↺ Run Again"):
                st.session_state.current_op_step = 0
                st.rerun()

    if st.session_state.get("run_log"):
        with st.expander(f"Run History ({len(st.session_state.run_log)} runs)"):
            for r in reversed(st.session_state.run_log):
                status = "Complete" if r["completed"] else "Incomplete"
                st.markdown(f"**Run {r['run']}** — {r['started']} — {status}")
                if r["steps"]:
                    st.dataframe(r["steps"], use_container_width=True)
