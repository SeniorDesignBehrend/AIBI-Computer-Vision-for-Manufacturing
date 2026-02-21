import cv2
from datetime import datetime
import time
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    from .DecodeQr import DecodeQr
    from .parse import Parse
    from .OutputData import OutputData
    from .config_manager import ConfigManager
except Exception:
    # Running as a script (not as a package). Add the `src` directory to sys.path
    # so `aibi_cv` can be imported as a top-level package.
    repo_src = Path(__file__).resolve().parents[1]
    if str(repo_src) not in sys.path:
        sys.path.insert(0, str(repo_src))
    from aibi_cv.DecodeQr import DecodeQr
    from aibi_cv.parse import Parse
    from aibi_cv.OutputData import OutputData
    from aibi_cv.config_manager import ConfigManager



class Camera:

    __decode: DecodeQr
    __parse: Parse
    __output: OutputData
    __workstation_id: str 
    __config_manager: ConfigManager

    def __init__(self, workstationId: str):
        self.__workstation_id = workstationId
        self.__decode = DecodeQr()
        self.__parse = Parse()
        self.__output = OutputData(self.__workstation_id, "./output")
        self.__config_manager = ConfigManager("./configs")
        self.__config = self.__config_manager.get_config(self.__workstation_id)

    def start(self):
        import json
        from pathlib import Path

        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)

        config = self.__config
        if not config:
            config = self.__config_manager.get_config(self.__workstation_id)
        if not config:
            config = self.__config_manager.create_default_config(self.__workstation_id)

        expected_qr_count = getattr(config, "expected_qr_count", None)
        scan_direction = getattr(config, "scan_direction", "any")
        append_key = getattr(config, "append_key", "TAB")

        scanned_data = {}
        last_seen = {}
        # saved_items removed: status will reflect only current `scanned_data`
        cooldown_frames = 30
        frame_count = 0

        # helper to compute centroid of detection polygon
        def _centroid(box):
            try:
                pts = box.astype(float)
                cx = pts[:, 0].mean()
                cy = pts[:, 1].mean()
                return cx, cy
            except Exception:
                return None, None

        cap = cv2.VideoCapture(config.camera_index)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        print(f"=== Advanced Scanner - {self.__workstation_id} ===")
        print(f"Expected QR count: {expected_qr_count}")
        print(f"Scan direction: {scan_direction}")
        print(f"Append key: {append_key}")
        print("\nFormat barcodes as: field_name:value")
        print("Data will auto-enter to Excel when all required fields are scanned")
        print("Press 'r' to reset, 'q' to quit\n")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Detect using pyzbar first, then OpenCV fallbacks
            detections = []
            try:
                detections = self.__decode.multi_pyzbar(frame)
            except Exception:
                detections = []

            if not detections:
                try:
                    detections = self.__decode.multi_opencv(frame)
                except Exception:
                    detections = []

            if not detections:
                try:
                    detections = self.__decode.single_opencv(frame)
                except Exception:
                    detections = []
            if detections:
                sorted_detections = detections
                if scan_direction and scan_direction != 'any':
                    def _sort_key(item):
                        _, box = item
                        cx, cy = _centroid(box)
                        if cx is None:
                            return (float('inf'), float('inf'))
                        # Row-major (left-to-right then down): sort by y then x
                        if scan_direction in ('row-major', 'left-to-right-down'):
                            return (cy, cx)
                        if scan_direction == 'right-to-left-down':
                            return (cy, -cx)
                        # Column-major (top-to-bottom then left-to-right): sort by x then y
                        if scan_direction in ('column-major', 'top-to-bottom-left-to-right'):
                            return (cx, cy)
                        if scan_direction == 'left-to-right':
                            return cx
                        if scan_direction == 'right-to-left':
                            return -cx
                        if scan_direction == 'top-to-bottom':
                            return cy
                        if scan_direction == 'bottom-to-top':
                            return -cy
                        return (cy, cx)
                    try:
                        sorted_detections = sorted(detections, key=_sort_key)
                    except Exception:
                        sorted_detections = detections

                for idx, (text, box) in enumerate(sorted_detections, start=1):
                    try:
                        name, value = self.__parse.parse(text)
                    except Exception:
                        name, value = None, text

                    # choose a stable key for this detection
                    key = name if name else f"raw_{idx}"

                    if key in last_seen and (frame_count - last_seen[key]) < cooldown_frames:
                        continue

                    if key not in scanned_data:
                        scanned_data[key] = value
                        last_seen[key] = frame_count
                        print(f"✓ Scanned: {key} = {value}")

                        # finalize when we have enough unique scans
                        try:
                            need = int(expected_qr_count) if expected_qr_count else 1
                        except Exception:
                            need = 1

                        if len(scanned_data) >= need:
                            print("\nExpected QR count reached - attempting output...\n")
                            # map append_key to keyboard lib names
                            ak = (append_key or "TAB").upper()
                            mapped = 'tab' if ak == 'TAB' else ('enter' if ak == 'ENTER' else None)

                            # Try automated Excel entry (OutputData). If not available, save JSON.
                            try:
                                ok = self.__output.to_exel(scanned_data, None, mapped)
                            except TypeError:
                                # fallback if OutputData expects different append_key form
                                ok = self.__output.to_exel(scanned_data, None, append_key)

                            if not ok:
                                print("Error: Excel not used, saving scan data to JSON")
                                if self.__output.to_json(scanned_data, None):
                                    print("✓ Saved scan to outputs (JSON)")
                                    scanned_data.clear()
                                    last_seen.clear()
                                    print("--- Ready for next scan ---\n")
                                else:
                                    print("Error: Failed to save scan data")

                    # Draw detection polygon
                    if box is not None:
                        try:
                            pts = box.astype(int)
                            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                        except Exception:
                            pass

            # Display status
            y_pos = 30
            cv2.putText(frame, f"Workstation: {self.__workstation_id}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_pos += 30

            try:
                need = int(expected_qr_count) if expected_qr_count else 1
            except Exception:
                need = 1

            cv2.putText(frame, f"Scanned: {len(scanned_data)}/{need}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
            y_pos += 25

            # show recent scanned items
            for k, v in list(scanned_data.items())[:6]:
                display = f"{k}: {v}"
                cv2.putText(frame, display, (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
                y_pos += 20

            if len(scanned_data) >= need:
                cv2.putText(frame, "READY TO SAVE", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow('Advanced Scanner', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                scanned_data.clear()
                last_seen.clear()
                print("\n--- Reset ---\n")

        cap.release()
        cv2.destroyAllWindows()

def main():
    camera = Camera("workstation_1")
    camera.start()

if __name__ == "__main__":
    main()