

import cv2
from datetime import datetime
import time
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    from .DecodeQr import DecodeQr
    from .Parse import Parse
    from .OutputData import OutputData
    from .config_manager import ConfigManager
except Exception:
    # Running as a script (not as a package). Add the `src` directory to sys.path
    # so `aibi_cv` can be imported as a top-level package.
    repo_src = Path(__file__).resolve().parents[1]
    if str(repo_src) not in sys.path:
        sys.path.insert(0, str(repo_src))
    from aibi_cv.DecodeQr import DecodeQr
    from aibi_cv.Parse import Parse
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

        required_fields = {f.name for f in config.barcode_fields if f.required}
        optional_fields = {f.name for f in config.barcode_fields if not f.required}
        all_fields = required_fields | optional_fields
        field_order = [f.name for f in config.barcode_fields]

        scanned_data = {}
        last_seen = {}
        # saved_items removed: status will reflect only current `scanned_data`
        cooldown_frames = 30
        frame_count = 0

        cap = cv2.VideoCapture(config.camera_index)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        print(f"=== Advanced Scanner - {self.__workstation_id} ===")
        print(f"Required fields: {', '.join(required_fields)}")
        print(f"Optional fields: {', '.join(optional_fields)}")
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
                for text, box in detections:
                    try:
                        name, value = self.__parse.parse(text)
                    except Exception:
                        name, value = None, text

                    if name in last_seen and (frame_count - last_seen[name]) < cooldown_frames:
                        continue

                    if name and name in all_fields and name not in scanned_data:
                        scanned_data[name] = value
                        last_seen[name] = frame_count
                        print(f"✓ Scanned: {name} = {value}")

                        if required_fields.issubset(scanned_data.keys()):
                            print("\nAll required fields scanned - attempting output...\n")

                            # Try automated Excel entry (OutputData). If not available, save JSON.
                            if not self.__output.to_exel(scanned_data, field_order):
                                print("Error: Excel not found, scan data will be saved in a file")
                                if self.__output.to_json(scanned_data, field_order):
                                    print(f"✓ Saved to {self.output_file}")
                                    # Clear scanned state so UI returns to waiting (red) state
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

            for field in required_fields:
                # Field is marked complete only while present in scanned_data
                completed = (field in scanned_data)
                status = "✓" if completed else "✗"
                color = (0, 255, 0) if completed else (0, 0, 255)
                cv2.putText(frame, f"{status} {field}", (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                y_pos += 25

            if required_fields and required_fields.issubset(scanned_data.keys()):
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