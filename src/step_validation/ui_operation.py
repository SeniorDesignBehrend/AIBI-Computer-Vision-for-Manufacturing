import time
from datetime import datetime

import cv2
import numpy as np
import streamlit as st

from .embeddings import get_embedding
from .process_manager import ProcessManager
from .state import VerificationState
from .verification import calculate_similarity, get_verification_state


def _draw_checklist_overlay(
    frame_rgb: np.ndarray,
    steps: list,
    current_idx: int,
    state: VerificationState,
    state_colors: dict,
) -> np.ndarray:
    frame = frame_rgb.copy()
    h, w = frame.shape[:2]

    panel_x, panel_y, panel_w, line_h = 10, 10, 320, 28
    panel_h = min(len(steps) * line_h + 20, h - 20)

    overlay = frame.copy()
    cv2.rectangle(overlay, (panel_x, panel_y),
                  (panel_x + panel_w, panel_y + panel_h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, dst=frame)

    for i, step in enumerate(steps):
        y = panel_y + 18 + i * line_h
        if y > panel_y + panel_h - 8:
            break
        if i < current_idx:
            symbol, color = "OK", (80, 220, 80)
        elif i == current_idx:
            symbol = ">>"
            color = state_colors.get(state, (255, 220, 50))
        else:
            symbol, color = "  ", (160, 160, 160)

        cv2.putText(frame, symbol, (panel_x + 5, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 1, cv2.LINE_AA)
        cv2.putText(frame, f"  {i + 1}. {step.name}", (panel_x + 40, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 1, cv2.LINE_AA)

    return frame


def render_operation_ui(manager: ProcessManager) -> None:
    st.title("Phase 2: Sequence Verification")

    with st.expander("Verification Parameters", expanded=False):
        similarity_threshold = st.slider(
            "Similarity Threshold", 0.50, 1.0, 0.75, 0.01,
            help="Minimum cosine similarity to count a frame as a match.",
        )
        window_duration = st.slider(
            "Detection Window (seconds)", 0.5, 5.0, 2.0, 0.5,
            help="How many seconds of frames to consider when confirming a step.",
        )
        required_fraction = st.slider(
            "Required Confidence", 0.3, 1.0, 0.7, 0.05,
            format="%.0f%%",
            help="Fraction of frames in the window that must match to confirm a step.",
        )

    steps = manager.get_steps()

    if not steps:
        st.warning("No process defined. Please go to Training mode first.")
        return
    if not st.session_state.get("training_finalized"):
        st.warning("Training not finalized. Go to Training mode and finalize.")
        return

    col_restart, col_start, _ = st.columns([1, 1, 3])
    if col_restart.button("↺ Restart"):
        st.session_state.current_op_step = 0
        st.rerun()

    current_idx = st.session_state.current_op_step

    # Colors in RGB order (frame is already converted to RGB before drawing)
    state_colors = {
        VerificationState.IDLE:          (180, 180, 180),
        VerificationState.CORRECT_STEP:  (0,   200, 100),
        VerificationState.CONFIRMED:     (0,   255,   0),
        VerificationState.WRONG_ORDER:   (255, 165,   0),
        VerificationState.SKIPPED:       (255,   0,   0),
        VerificationState.COMPLETE:      (0,   255,   0),
    }

    video_loc = st.empty()
    status_loc = st.empty()

    if col_start.button("Start Monitoring"):
        with st.spinner("Opening camera..."):
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera not available.")
            return

        timed_window: list[tuple[float, int]] = []
        TARGET_FPS = 10
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
            frame_start = time.monotonic()

            emb = get_embedding(frame)
            detected_idx, conf = calculate_similarity(emb, steps, similarity_threshold)
            timed_window.append((time.monotonic(), detected_idx))
            cutoff = time.monotonic() - window_duration
            timed_window = [(ts, idx) for ts, idx in timed_window if ts >= cutoff]

            state = get_verification_state(
                detected_idx, current_idx, len(steps),
                timed_window, window_duration, required_fraction
            )

            if state == VerificationState.IDLE:
                status_text = "Waiting for action..."

            elif state == VerificationState.CORRECT_STEP:
                cutoff = time.monotonic() - window_duration
                recent = [idx for ts, idx in timed_window if ts >= cutoff]
                frac = sum(1 for idx in recent if idx == current_idx) / max(len(recent), 1)
                status_text = (
                    f"Detecting '{steps[current_idx].name}'... "
                    f"({int(frac * 100)}% / {int(required_fraction * 100)}%)"
                )

            elif state == VerificationState.CONFIRMED:
                status_text = f"Step {current_idx + 1} confirmed!"
                run_record["steps"].append({
                    "step": steps[current_idx].name,
                    "result": "OK",
                    "warnings": "; ".join(current_step_warnings) or "-",
                })
                current_step_warnings = []
                st.session_state.current_op_step += 1
                current_idx += 1
                timed_window.clear()

            elif state == VerificationState.WRONG_ORDER:
                past_name = steps[detected_idx].name if detected_idx >= 0 else "unknown"
                status_text = f"Warning: '{past_name}' re-detected (expected step {current_idx + 1})"
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

            # Draw on RGB frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            conf_pct = int(conf * 100)
            cv2.putText(
                frame_rgb,
                f"{state.name}  |  {conf_pct}%",
                (20, frame_rgb.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, state_colors[state], 2, cv2.LINE_AA,
            )
            frame_annotated = _draw_checklist_overlay(
                frame_rgb, steps, current_idx, state, state_colors
            )
            video_loc.image(frame_annotated, use_container_width=True)
            status_loc.caption(status_text)

            elapsed = time.monotonic() - frame_start
            sleep_time = (1.0 / TARGET_FPS) - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

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
