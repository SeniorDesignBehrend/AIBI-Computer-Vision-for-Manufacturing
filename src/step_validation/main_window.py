from pathlib import Path

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QProgressDialog,
    QWidget,
)

from .embeddings import load_dinov2_model
from .process_manager import ProcessManager
from .serialization import deserialize_process
from .widgets.operation_widget import OperationWidget
from .widgets.training_widget import TrainingWidget


class _ModelLoader(QThread):
    """Loads DINOv2 in a background thread so the UI stays responsive."""
    finished = Signal()
    error = Signal(str)

    def run(self):
        try:
            load_dinov2_model()
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(
        self,
        mode: str,
        process_path: str | None = None,
        threshold: float = 0.75,
        window_duration: float = 2.0,
        required_fraction: float = 0.70,
        log_dir: str = "logs",
    ):
        super().__init__()
        self.setWindowTitle("Action Sequence Trainer")
        self.resize(1280, 800)

        self._mode = mode
        self._op_params = dict(
            threshold=threshold,
            window_duration=window_duration,
            required_fraction=required_fraction,
            log_dir=log_dir,
        )
        self._manager = ProcessManager()

        # Load a process file if provided (e.g. via --process CLI arg)
        if process_path:
            try:
                steps = deserialize_process(Path(process_path).read_bytes())
                self._manager.steps = steps
                self._manager.training_finalized = True
            except Exception as exc:
                QMessageBox.warning(
                    self, "Load Warning",
                    f"Could not load process file:\n{exc}\n\nStarting with empty process."
                )

        # Show a modal progress dialog while the model loads
        self._progress = QProgressDialog("Loading DINOv2 model...", None, 0, 0, self)
        self._progress.setWindowTitle("Loading")
        self._progress.setCancelButton(None)
        self._progress.setModal(True)
        self._progress.show()

        self._loader = _ModelLoader(self)
        self._loader.finished.connect(self._on_model_loaded)
        self._loader.error.connect(self._on_model_error)
        self._loader.start()

    @Slot()
    def _on_model_loaded(self):
        self._loader.wait()  # Ensure run() has fully returned before we continue
        self._progress.close()
        self._build_ui()

    @Slot(str)
    def _on_model_error(self, msg: str):
        self._loader.wait()
        self._progress.close()
        QMessageBox.critical(self, "Model Load Error",
                             f"Failed to load DINOv2 model:\n{msg}")
        self._build_ui()  # Still open the app — user may want to inspect state

    def _build_ui(self):
        if self._mode == "training":
            self._central: QWidget = TrainingWidget(self._manager)
            self.setWindowTitle("Action Sequence Trainer — Training Mode")
        else:
            self._central = OperationWidget(self._manager, **self._op_params)
            self.setWindowTitle("Action Sequence Trainer — Operation Mode")

        self.setCentralWidget(self._central)

    def closeEvent(self, event):
        # Cleanly stop any background threads before closing
        if hasattr(self, "_central") and hasattr(self._central, "cleanup"):
            self._central.cleanup()
        event.accept()
