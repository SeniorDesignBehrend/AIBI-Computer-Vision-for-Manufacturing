import time
from datetime import datetime
from typing import List

import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal

from ..embeddings import get_embedding
from ..models import ActionStep
from ..state import VerificationState
from ..verification import calculate_similarity, get_verification_state

# Colors in BGR order for OpenCV drawing
_STATE_COLORS_BGR = {
    VerificationState.IDLE:         (180, 180, 180),
    VerificationState.CORRECT_STEP: (100, 200,   0),
    VerificationState.CONFIRMED:    (0,   255,   0),
    VerificationState.WRONG_ORDER:  (0,   165, 255),
    VerificationState.SKIPPED:      (0,     0, 255),
    VerificationState.COMPLETE:     (0,   255,   0),
}


def draw_checklist_overlay(
    frame_bgr: np.ndarray,
    steps: List[ActionStep],
    current_idx: int,
    state: VerificationState,
) -> np.ndarray:
    frame = frame_bgr.copy()
    h, w = frame.shape[:2]
    color = _STATE_COLORS_BGR.get(state, (180, 180, 180))

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
            symbol, c = "OK", (80, 220, 80)
        elif i == current_idx:
            symbol, c = ">>", color
        else:
            symbol, c = "  ", (160, 160, 160)

        cv2.putText(frame, symbol, (panel_x + 5, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, c, 1, cv2.LINE_AA)
        cv2.putText(frame, f"  {i + 1}. {step.name}", (panel_x + 40, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, c, 1, cv2.LINE_AA)

    return frame


class OperationWorker(QThread):
    """Owns the full monitoring loop: camera capture, DINOv2 inference,
    state machine, and overlay drawing. Emits signals for the UI to consume.

    Signals
    -------
    frame_processed(frame_bgr, state, status_text, current_idx, confidence)
    step_confirmed(step_index)
    run_finished(run_record_dict)
    camera_error()
    """

    frame_processed = Signal(object, object, str, int, float)
    step_confirmed = Signal(int)
    run_finished = Signal(dict)
    camera_error = Signal()
    camera_opened = Signal()

    def __init__(
        self,
        steps: List[ActionStep],
        threshold: float,
        window_duration: float,
        required_fraction: float,
        run_number: int,
        camera_index: int = 0,
        target_fps: int = 10,
        parent=None,
    ):
        super().__init__(parent)
        self.steps = steps
        self.threshold = threshold
        self.window_duration = window_duration
        self.required_fraction = required_fraction
        self.run_number = run_number
        self.camera_index = camera_index
        self._interval = 1.0 / target_fps
        self._running = False

    _WARMUP_ATTEMPTS = 30

    def _open_camera(self) -> cv2.VideoCapture | None:
        # Try MSMF (default), then DirectShow fallback
        for backend in (cv2.CAP_ANY, cv2.CAP_DSHOW):
            cap = cv2.VideoCapture(self.camera_index, backend)
            if not cap.isOpened():
                continue
            for _ in range(self._WARMUP_ATTEMPTS):
                ret, _ = cap.read()
                if ret:
                    return cap
                time.sleep(self._interval)
            cap.release()
        return None

    def run(self):
        cap = self._open_camera()
        if cap is None:
            self.camera_error.emit()
            return

        self.camera_opened.emit()

        self._running = True
        current_idx = 0
        timed_window: list[tuple[float, int]] = []
        run_record = {
            "run": self.run_number,
            "started": datetime.now().strftime("%H:%M:%S"),
            "completed": False,
            "steps": [],
        }
        current_step_warnings: list[str] = []

        while self._running and cap.isOpened():
            frame_start = time.monotonic()

            ret, frame = cap.read()
            if not ret:
                break

            emb = get_embedding(frame)
            detected_idx, conf = calculate_similarity(emb, self.steps, self.threshold)
            timed_window.append((time.monotonic(), detected_idx))
            cutoff = time.monotonic() - self.window_duration
            timed_window = [(ts, idx) for ts, idx in timed_window if ts >= cutoff]

            state = get_verification_state(
                detected_idx, current_idx, len(self.steps),
                timed_window, self.window_duration, self.required_fraction,
            )

            if state == VerificationState.IDLE:
                status_text = "Waiting for action..."

            elif state == VerificationState.CORRECT_STEP:
                recent = [idx for ts, idx in timed_window if ts >= cutoff]
                frac = sum(1 for idx in recent if idx == current_idx) / max(len(recent), 1)
                status_text = (
                    f"Detecting '{self.steps[current_idx].name}'... "
                    f"({int(frac * 100)}% / {int(self.required_fraction * 100)}%)"
                )

            elif state == VerificationState.CONFIRMED:
                status_text = f"Step {current_idx + 1} confirmed!"
                run_record["steps"].append({
                    "step": self.steps[current_idx].name,
                    "result": "OK",
                    "warnings": "; ".join(current_step_warnings) or "-",
                })
                self.step_confirmed.emit(current_idx)
                current_step_warnings = []
                current_idx += 1
                timed_window.clear()

            elif state == VerificationState.WRONG_ORDER:
                past_name = self.steps[detected_idx].name if detected_idx >= 0 else "unknown"
                status_text = f"Warning: '{past_name}' re-detected (expected step {current_idx + 1})"
                current_step_warnings.append(f"Re-detected '{past_name}'")

            elif state == VerificationState.SKIPPED:
                future_name = self.steps[detected_idx].name
                status_text = (
                    f"WARNING: Skipped to '{future_name}'! "
                    f"(Expected '{self.steps[current_idx].name}')"
                )
                current_step_warnings.append(f"Skipped to '{future_name}'")

            elif state == VerificationState.COMPLETE:
                status_text = "Process Complete!"

            else:
                status_text = ""

            # Draw overlays on BGR frame
            color = _STATE_COLORS_BGR.get(state, (180, 180, 180))
            cv2.putText(
                frame,
                f"{state.name}  |  {int(conf * 100)}%",
                (20, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA,
            )
            annotated = draw_checklist_overlay(frame, self.steps, current_idx, state)
            self.frame_processed.emit(annotated, state, status_text, current_idx, conf)

            if state == VerificationState.COMPLETE:
                self._running = False

            elapsed = time.monotonic() - frame_start
            sleep_time = self._interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        cap.release()
        run_record["completed"] = (current_idx >= len(self.steps))
        self.run_finished.emit(run_record)

    def stop(self):
        self._running = False
        self.wait()
