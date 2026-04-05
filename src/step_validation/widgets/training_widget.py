from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import Qt, QSize, QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..process_manager import ProcessManager
from ..serialization import deserialize_process, serialize_process
from ..workers.camera_worker import CameraWorker

SAMPLE_EVERY_N = 3
THUMB_WIDTH = 160
THUMB_HEIGHT = 90
ROW_HEIGHT = THUMB_HEIGHT + 20


def _frame_to_pixmap(frame_bgr: np.ndarray, w: int = 0, h: int = 0) -> QPixmap:
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    qh, qw, ch = rgb.shape
    # Use tobytes() so Qt owns the data and the numpy array can be GC'd safely
    img = QImage(rgb.tobytes(), qw, qh, ch * qw, QImage.Format.Format_RGB888)
    px = QPixmap.fromImage(img)
    if w > 0 and h > 0:
        px = px.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio,
                       Qt.TransformationMode.SmoothTransformation)
    return px


class _FinalizeWorker(QThread):
    """Runs finalize_training_from_segments in a background thread."""
    done = Signal()   # named 'done' to avoid shadowing QThread's built-in 'finished'
    error = Signal(str)

    def __init__(self, manager: ProcessManager, segments: list, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.segments = segments

    def run(self):
        try:
            self.manager.finalize_training_from_segments(self.segments)
            self.done.emit()
        except Exception as exc:
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Record phase — camera tab
# ---------------------------------------------------------------------------

class _CameraTab(QWidget):
    segment_saved = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buffer: list[np.ndarray] = []
        self._camera_worker: CameraWorker | None = None
        self._recording = False

        layout = QVBoxLayout(self)

        self._preview = QLabel("Camera preview will appear here.")
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setMinimumHeight(300)
        self._preview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._preview.setStyleSheet("background: #1a1a1a; color: #888;")
        layout.addWidget(self._preview)

        btn_row = QHBoxLayout()
        self._btn_start = QPushButton("Start Recording")
        self._btn_start.clicked.connect(self._start_recording)
        self._btn_stop = QPushButton("Stop Recording")
        self._btn_stop.setEnabled(False)
        self._btn_stop.clicked.connect(self._stop_recording)
        btn_row.addWidget(self._btn_start)
        btn_row.addWidget(self._btn_stop)
        layout.addLayout(btn_row)

        # Save controls (hidden until recording stops with frames)
        self._save_group = QGroupBox("Save segment")
        self._save_group.setVisible(False)
        save_layout = QVBoxLayout(self._save_group)
        self._label_info = QLabel()
        save_layout.addWidget(self._label_info)
        self._name_input = QLineEdit()
        self._name_input.setPlaceholderText("Step name (e.g. 'Attach Left Bracket')")
        save_layout.addWidget(self._name_input)
        save_btns = QHBoxLayout()
        btn_save = QPushButton("Save Segment")
        btn_save.clicked.connect(self._save_segment)
        btn_discard = QPushButton("Discard")
        btn_discard.clicked.connect(self._discard_buffer)
        save_btns.addWidget(btn_save)
        save_btns.addWidget(btn_discard)
        save_layout.addLayout(save_btns)
        layout.addWidget(self._save_group)

    def showEvent(self, event):
        super().showEvent(event)
        # Start preview lazily so the label has been laid out and has real dimensions
        if self._camera_worker is None:
            self._start_preview()

    def _start_preview(self):
        self._camera_worker = CameraWorker(fps=30)
        self._camera_worker.frame_ready.connect(self._on_preview_frame)
        self._camera_worker.camera_error.connect(self._on_camera_error)
        self._camera_worker.start()

    @Slot()
    def _on_camera_error(self):
        self._preview.setText("Camera not available.\nCheck that no other application is using it.")
        self._btn_start.setEnabled(False)

    def _start_recording(self):
        self._recording = True
        self._buffer = []
        self._save_group.setVisible(False)
        self._btn_start.setEnabled(False)
        self._btn_stop.setEnabled(True)

    def _stop_recording(self):
        self._recording = False
        self._btn_start.setEnabled(True)
        self._btn_stop.setEnabled(False)
        if self._buffer:
            self._label_info.setText(f"Captured {len(self._buffer)} frames. Name this step to save it.")
            self._name_input.clear()
            self._save_group.setVisible(True)

    @Slot(object)
    def _on_preview_frame(self, frame: np.ndarray):
        lw = self._preview.width() or 640
        lh = self._preview.height() or 480
        if self._recording:
            self._buffer.append(frame.copy())
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.putText(rgb, f"REC  {len(self._buffer)} frames", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (220, 50, 50), 2, cv2.LINE_AA)
            fh, fw, ch = rgb.shape
            img = QImage(rgb.tobytes(), fw, fh, ch * fw, QImage.Format.Format_RGB888)
            self._preview.setPixmap(
                QPixmap.fromImage(img).scaled(
                    lw, lh,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self._preview.setPixmap(_frame_to_pixmap(frame, lw, lh))

    def _save_segment(self):
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Name required", "Please enter a step name.")
            return
        self.segment_saved.emit({"label": name, "frames": self._buffer, "source": "camera"})
        self._buffer = []
        self._save_group.setVisible(False)

    def _discard_buffer(self):
        self._buffer = []
        self._save_group.setVisible(False)

    def cleanup(self):
        if self._camera_worker:
            self._camera_worker.stop()


# ---------------------------------------------------------------------------
# Record phase — upload tab
# ---------------------------------------------------------------------------

class _UploadTab(QWidget):
    segment_saved = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        btn_open = QPushButton("Upload Video Files...")
        btn_open.clicked.connect(self._open_files)
        layout.addWidget(btn_open)

        self._info_label = QLabel("No videos uploaded.")
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._info_label.setStyleSheet("color: #888;")
        layout.addWidget(self._info_label)
        layout.addStretch()

    def _open_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Upload Videos", "", "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        if not paths:
            return

        for path in paths:
            cap = cv2.VideoCapture(path)
            all_frames: list[np.ndarray] = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                all_frames.append(frame.copy())
            cap.release()

            if not all_frames:
                QMessageBox.warning(self, "Error", f"Could not read frames from {Path(path).name}")
                continue

            frames = [f for idx, f in enumerate(all_frames) if idx % SAMPLE_EVERY_N == 0]
            name = Path(path).stem
            self.segment_saved.emit({"label": name, "frames": frames, "source": "upload"})

        self._info_label.setText(f"Uploaded {len(paths)} video(s) as segments.")


# ---------------------------------------------------------------------------
# Record phase
# ---------------------------------------------------------------------------

class _RecordPhase(QWidget):
    go_to_review = Signal()

    def __init__(self, manager: ProcessManager, parent=None):
        super().__init__(parent)
        self._manager = manager

        layout = QVBoxLayout(self)

        header = QLabel("Step 1: Record a Segment")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        layout.addWidget(QLabel(
            "Record video of yourself performing one step, then give it a name. "
            "Repeat for each step."
        ))

        tabs = QTabWidget()
        self._camera_tab = _CameraTab()
        self._camera_tab.segment_saved.connect(self._on_segment_saved)
        self._upload_tab = _UploadTab()
        self._upload_tab.segment_saved.connect(self._on_segment_saved)
        tabs.addTab(self._camera_tab, "Live Camera")
        tabs.addTab(self._upload_tab, "Upload Video File")
        layout.addWidget(tabs)

        self._review_btn = QPushButton("Review segments and finalize →")
        self._review_btn.setEnabled(False)
        self._review_btn.clicked.connect(self.go_to_review)
        layout.addWidget(self._review_btn)

        self._refresh_review_button()

    @Slot(dict)
    def _on_segment_saved(self, seg: dict):
        self._manager.recorded_segments.append(seg)
        self._refresh_review_button()

    def _refresh_review_button(self):
        n = len(self._manager.recorded_segments)
        self._review_btn.setEnabled(n > 0)
        self._review_btn.setText(f"Review {n} segment(s) and finalize →")

    def cleanup(self):
        self._camera_tab.cleanup()


# ---------------------------------------------------------------------------
# Review phase — draggable / reorderable segment list
# ---------------------------------------------------------------------------

class _DragList(QListWidget):
    """QListWidget with internal drag-and-drop reordering."""
    reordered = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSpacing(2)
        self.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
            "QListWidget::item { background: transparent; border: none; }"
            "QListWidget::item:selected { background: transparent; }"
        )

    def dropEvent(self, event):
        super().dropEvent(event)
        self.reordered.emit()


class _SegmentRowWidget(QWidget):
    """One row in the review list."""
    delete_clicked = Signal()
    move_up_clicked = Signal()
    move_down_clicked = Signal()

    def __init__(self, seg: dict, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        # Drag handle (visual indicator)
        handle = QLabel("⠿")
        handle.setFixedWidth(18)
        handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        handle.setStyleSheet("color: #555; font-size: 20px;")
        handle.setToolTip("Drag to reorder")
        layout.addWidget(handle)

        # Step info
        info = QVBoxLayout()
        info.setSpacing(2)
        name_edit = QLineEdit(seg.get("label", ""))
        name_edit.setPlaceholderText("Step name")
        # Update dict in-place so manager's list stays in sync
        name_edit.textChanged.connect(lambda t, s=seg: s.update({"label": t}))
        source = "Camera" if seg.get("source") == "camera" else "Upload"
        caption = QLabel(f"{source}  |  {len(seg.get('frames', []))} frames")
        caption.setStyleSheet("color: #888; font-size: 11px;")
        info.addWidget(name_edit)
        info.addWidget(caption)
        layout.addLayout(info, stretch=3)

        # Thumbnail
        thumb = QLabel()
        frames = seg.get("frames", [])
        if frames:
            mid = frames[len(frames) // 2]
            thumb.setPixmap(_frame_to_pixmap(mid, THUMB_WIDTH, THUMB_HEIGHT))
        thumb.setFixedSize(THUMB_WIDTH, THUMB_HEIGHT)
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb.setStyleSheet("background: #222;")
        layout.addWidget(thumb)

        # Action buttons (up / down / delete)
        btns = QVBoxLayout()
        btns.setSpacing(2)
        btn_up = QPushButton("↑")
        btn_up.setFixedSize(32, 28)
        btn_up.setToolTip("Move up")
        btn_up.clicked.connect(self.move_up_clicked)
        btn_down = QPushButton("↓")
        btn_down.setFixedSize(32, 28)
        btn_down.setToolTip("Move down")
        btn_down.clicked.connect(self.move_down_clicked)
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(32, 28)
        btn_del.setToolTip("Delete")
        btn_del.setStyleSheet("color: #f66;")
        btn_del.clicked.connect(self.delete_clicked)
        btns.addWidget(btn_up)
        btns.addWidget(btn_down)
        btns.addWidget(btn_del)
        layout.addLayout(btns)


class _ReviewPhase(QWidget):
    go_back = Signal()
    training_finalized = Signal()

    def __init__(self, manager: ProcessManager, parent=None):
        super().__init__(parent)
        self._manager = manager
        self._finalize_worker: _FinalizeWorker | None = None

        layout = QVBoxLayout(self)

        header = QLabel("Step 2: Review & Finalize")
        header.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        layout.addWidget(QLabel(
            "Drag rows to reorder, or use ↑/↓ buttons. All steps must be named before finalizing."
        ))

        self._list = _DragList()
        self._list.reordered.connect(self._sync_from_list)
        layout.addWidget(self._list, stretch=1)

        btn_row = QHBoxLayout()
        self._btn_back = QPushButton("← Record Another")
        self._btn_back.clicked.connect(self.go_back)
        self._btn_finalize = QPushButton("Finalize Training")
        self._btn_finalize.clicked.connect(self._finalize)
        btn_row.addWidget(self._btn_back)
        btn_row.addStretch()
        btn_row.addWidget(self._btn_finalize)
        layout.addLayout(btn_row)

        self._status_label = QLabel()
        layout.addWidget(self._status_label)

        self._btn_save = QPushButton("Save Process (.pkl)")
        self._btn_save.setVisible(False)
        self._btn_save.clicked.connect(self._save_process)
        layout.addWidget(self._btn_save)

    def refresh(self):
        """Rebuild the list widget from manager.recorded_segments."""
        self._list.clear()
        for seg in self._manager.recorded_segments:
            row_widget = _SegmentRowWidget(seg)
            row_widget.delete_clicked.connect(lambda s=seg: self._delete(s))
            row_widget.move_up_clicked.connect(lambda s=seg: self._move(s, -1))
            row_widget.move_down_clicked.connect(lambda s=seg: self._move(s, 1))

            item = QListWidgetItem(self._list)
            item.setData(Qt.ItemDataRole.UserRole, seg)
            item.setSizeHint(QSize(0, ROW_HEIGHT))
            self._list.addItem(item)
            self._list.setItemWidget(item, row_widget)

        self._update_finalize_btn()
        self._btn_save.setVisible(self._manager.training_finalized)

    def _sync_from_list(self):
        """Called after a drag-drop: re-sync manager data from list order, then rebuild."""
        new_order = [
            self._list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self._list.count())
        ]
        self._manager.recorded_segments = new_order
        # Rebuild widgets so they're always in the correct list positions
        self.refresh()

    def _delete(self, seg: dict):
        try:
            self._manager.recorded_segments.remove(seg)
        except ValueError:
            pass
        self.refresh()

    def _move(self, seg: dict, direction: int):
        segs = self._manager.recorded_segments
        try:
            idx = segs.index(seg)
        except ValueError:
            return
        new_idx = idx + direction
        if 0 <= new_idx < len(segs):
            segs[idx], segs[new_idx] = segs[new_idx], segs[idx]
            self.refresh()
            # Re-select the moved item
            self._list.setCurrentRow(new_idx)

    def _update_finalize_btn(self):
        segs = self._manager.recorded_segments
        all_labeled = bool(segs) and all(
            seg.get("label", "").strip() for seg in segs
        )
        self._btn_finalize.setEnabled(all_labeled)

    def _finalize(self):
        self._btn_finalize.setEnabled(False)
        self._btn_back.setEnabled(False)
        self._status_label.setText("Computing embeddings... this may take a moment.")

        self._finalize_worker = _FinalizeWorker(
            self._manager, list(self._manager.recorded_segments)
        )
        self._finalize_worker.done.connect(self._on_finalized)
        self._finalize_worker.error.connect(self._on_finalize_error)
        self._finalize_worker.start()

    @Slot()
    def _on_finalized(self):
        if self._finalize_worker:
            self._finalize_worker.wait()
        self._status_label.setText("Training complete!")
        self._btn_save.setVisible(True)
        self._btn_finalize.setEnabled(True)
        self._btn_back.setEnabled(True)
        self.training_finalized.emit()

    @Slot(str)
    def _on_finalize_error(self, msg: str):
        self._status_label.setText(f"Error: {msg}")
        self._btn_finalize.setEnabled(True)
        self._btn_back.setEnabled(True)

    def _save_process(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Process", "process.pkl", "Process Files (*.pkl)"
        )
        if not path:
            return
        data = serialize_process(self._manager.get_steps())
        Path(path).write_bytes(data)
        self._status_label.setText(f"Saved to {path}")


# ---------------------------------------------------------------------------
# Top-level TrainingWidget
# ---------------------------------------------------------------------------

class TrainingWidget(QWidget):
    def __init__(self, manager: ProcessManager, parent=None):
        super().__init__(parent)
        self._manager = manager

        outer = QVBoxLayout(self)

        # Load saved process button (always visible at top)
        load_row = QHBoxLayout()
        btn_load = QPushButton("Load Saved Process (.pkl)")
        btn_load.clicked.connect(self._load_process)
        load_row.addWidget(btn_load)
        load_row.addStretch()
        outer.addLayout(load_row)

        self._stack = QStackedWidget()
        self._record_phase = _RecordPhase(manager)
        self._review_phase = _ReviewPhase(manager)
        self._stack.addWidget(self._record_phase)   # index 0
        self._stack.addWidget(self._review_phase)   # index 1
        outer.addWidget(self._stack)

        self._record_phase.go_to_review.connect(self._show_review)
        self._review_phase.go_back.connect(self._show_record)
        self._review_phase.training_finalized.connect(self._on_training_finalized)

    def _show_review(self):
        self._review_phase.refresh()
        self._stack.setCurrentIndex(1)

    def _show_record(self):
        self._stack.setCurrentIndex(0)

    @Slot()
    def _on_training_finalized(self):
        pass  # MainWindow can connect to this if needed

    def _load_process(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Process", "", "Process Files (*.pkl)"
        )
        if not path:
            return
        try:
            steps = deserialize_process(Path(path).read_bytes())
            self._manager.steps = steps
            self._manager.training_finalized = True
            self._manager.current_op_step = 0
            QMessageBox.information(
                self, "Loaded",
                f"Loaded {len(steps)} step(s) from {Path(path).name}"
            )
        except Exception as exc:
            QMessageBox.critical(self, "Load Error", str(exc))

    def cleanup(self):
        self._record_phase.cleanup()
