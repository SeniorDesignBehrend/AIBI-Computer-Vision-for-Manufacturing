"""Entry point for the Action Sequence Trainer.

Usage
-----
    python -m step_validation.main --mode training
    python -m step_validation.main --mode operation --process path/to/process.pkl
    python -m step_validation.main --mode operation --process path/to/process.pkl \\
        --threshold 0.80 --window 2.5 --confidence 0.65 --log-dir C:\\logs --camera 1

VB.NET example
--------------
    Dim proc As New Process()
    proc.StartInfo.FileName = "python"
    proc.StartInfo.Arguments = "-m step_validation.main --mode operation --process C:\\path\\process.pkl --log-dir C:\\logs"
    proc.Start()
"""

import argparse
import sys

import cv2
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow


def main():
    parser = argparse.ArgumentParser(description="Action Sequence Trainer")
    parser.add_argument(
        "--mode",
        choices=["training", "operation"],
        required=True,
        help="Launch in training (teach) or operation (monitor) mode.",
    )
    parser.add_argument(
        "--process",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to a .pkl process file to load on startup.",
    )
    parser.add_argument(
        "--camera",
        type=int,
        default=0,
        metavar="INDEX",
        help="Camera device index (default: 0).",
    )

    # Operation-mode tuning parameters
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.75,
        metavar="FLOAT",
        help="Similarity threshold (0.5–1.0, default 0.75).",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=2.0,
        metavar="SECONDS",
        help="Detection window in seconds (default 2.0).",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.70,
        metavar="FLOAT",
        help="Required fraction of frames to confirm a step (default 0.70).",
    )
    parser.add_argument(
        "--log-dir",
        type=str,
        default="logs",
        metavar="PATH",
        help="Directory to write run log JSON files (default: logs/).",
    )
    args = parser.parse_args()

    cv2.setLogLevel(0)  # Suppress MSMF/backend grab warnings on Windows

    app = QApplication(sys.argv)
    app.setApplicationName("Action Sequence Trainer")

    window = MainWindow(
        mode=args.mode,
        process_path=args.process,
        threshold=args.threshold,
        window_duration=args.window,
        required_fraction=args.confidence,
        log_dir=args.log_dir,
    )
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
