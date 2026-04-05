import json
from datetime import datetime
from pathlib import Path

import numpy as np
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..process_manager import ProcessManager
from ..state import VerificationState
from ..workers.operation_worker import OperationWorker


def _frame_bgr_to_pixmap(frame_bgr: np.ndarray, max_w: int, max_h: int) -> QPixmap:
    import cv2
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    img = QImage(rgb.tobytes(), w, h, ch * w, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(img).scaled(
        max_w, max_h,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )


_STATE_COLORS = {
    VerificationState.IDLE:         "#aaaaaa",
    VerificationState.CORRECT_STEP: "#00c864",
    VerificationState.CONFIRMED:    "#00ff00",
    VerificationState.WRONG_ORDER:  "#ffa500",
    VerificationState.SKIPPED:      "#ff4444",
    VerificationState.COMPLETE:     "#00ff00",
}


class OperationWidget(QWidget):
    def __init__(
        self,
        manager: ProcessManager,
        threshold: float = 0.75,
        window_duration: float = 2.0,
        required_fraction: float = 0.70,
        log_dir: str = "logs",
        parent=None,
    ):
        super().__init__(parent)
        self._manager = manager
        self._threshold = threshold
        self._window_duration = window_duration
        self._required_fraction = required_fraction
        self._log_dir = Path(log_dir)
        self._worker: OperationWorker | None = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(4, 4, 4, 4)
        outer.setSpacing(4)

        # ---- Toolbar ----
        toolbar = QHBoxLayout()
        self._btn_start = QPushButton("▶  Start")
        self._btn_start.clicked.connect(self._start)
        self._btn_stop = QPushButton("■  Stop")
        self._btn_stop.setEnabled(False)
        self._btn_stop.clicked.connect(self._stop)
        self._btn_restart = QPushButton("↺  Restart")
        self._btn_restart.clicked.connect(self._restart)
        toolbar.addWidget(self._btn_start)
        toolbar.addWidget(self._btn_stop)
        toolbar.addWidget(self._btn_restart)
        toolbar.addStretch()
        outer.addLayout(toolbar)

        # ---- Video (fills remaining space) ----
        self._video_label = QLabel("Press ▶ Start to begin.")
        self._video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._video_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._video_label.setStyleSheet("background: #111; color: #666;")
        outer.addWidget(self._video_label, stretch=1)

        # ---- Thin status bar ----
        self._status_label = QLabel()
        self._status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status_label.setFixedHeight(24)
        self._status_label.setStyleSheet("font-size: 13px; color: #aaa;")
        outer.addWidget(self._status_label)

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    @Slot(object, object, str, int, float)
    def _on_frame(self, frame_bgr: np.ndarray, state: VerificationState,
                  status: str, current_idx: int, conf: float):
        w = self._video_label.width() or 1280
        h = self._video_label.height() or 720
        self._video_label.setPixmap(_frame_bgr_to_pixmap(frame_bgr, w, h))
        self._status_label.setText(status)
        color = _STATE_COLORS.get(state, "#aaaaaa")
        self._status_label.setStyleSheet(f"font-size: 13px; color: {color};")

    @Slot(dict)
    def _on_run_finished(self, record: dict):
        self._manager.run_log.append(record)
        self._btn_start.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._btn_restart.setEnabled(True)
        self._worker = None
        self._save_log(record)
        if record["completed"]:
            self._status_label.setText("Process Completed Successfully!")
            self._status_label.setStyleSheet("font-size: 13px; color: #00ff00;")

    @Slot()
    def _on_camera_error(self):
        QMessageBox.critical(self, "Camera Error", "Could not open camera.")
        self._btn_start.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._btn_restart.setEnabled(True)
        self._worker = None

    # ------------------------------------------------------------------
    # Button handlers
    # ------------------------------------------------------------------

    def _start(self):
        steps = self._manager.get_steps()
        if not steps:
            QMessageBox.warning(self, "No process",
                                "No process defined. Please run training first.")
            return
        if not self._manager.training_finalized:
            QMessageBox.warning(self, "Not finalized",
                                "Training not finalized. Go to Training mode and finalize.")
            return

        self._btn_start.setEnabled(False)
        self._btn_stop.setEnabled(True)
        self._btn_restart.setEnabled(False)
        self._video_label.setText("")

        self._worker = OperationWorker(
            steps=steps,
            threshold=self._threshold,
            window_duration=self._window_duration,
            required_fraction=self._required_fraction,
            run_number=len(self._manager.run_log) + 1,
        )
        self._worker.frame_processed.connect(self._on_frame)
        self._worker.run_finished.connect(self._on_run_finished)
        self._worker.camera_error.connect(self._on_camera_error)
        self._worker.start()

    def _stop(self):
        if self._worker:
            self._worker.stop()
            self._worker = None
        self._btn_start.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._btn_restart.setEnabled(True)

    def _restart(self):
        self._stop()
        self._manager.current_op_step = 0
        self._status_label.setText("")
        self._video_label.setText("Press ▶ Start to begin.")
        self._video_label.setStyleSheet("background: #111; color: #666;")

    # ------------------------------------------------------------------
    # Log saving
    # ------------------------------------------------------------------

    def _save_log(self, record: dict):
        try:
            self._log_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = self._log_dir / f"run_{record['run']}_{timestamp}.json"
            path.write_text(json.dumps(record, indent=2))
        except Exception:
            pass  # Never crash the app over a log write failure

    def cleanup(self):
        if self._worker:
            self._worker.stop()
