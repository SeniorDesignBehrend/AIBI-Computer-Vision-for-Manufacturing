

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
    __workstation_id: str = 'workstation_01' #Set this to the proper workstation id
    __config_manager: ConfigManager

    def __init__(self):
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
        saved_items = set()
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
                            try:
                                excel_ok = self.__output.to_exel(scanned_data, field_order)
                            except Exception:
                                excel_ok = False

                            output_data = {
                                "workstation_id": self.__workstation_id,
                                "timestamp": datetime.now().isoformat(),
                                "barcodes": [
                                    {"name": n, "value": scanned_data[n]}
                                    for n in field_order if n in scanned_data
                                ]
                            }
                            output_file = output_dir / f"scan_{self.__workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(output_data, f, indent=2)

                            print(f"✓ Saved to {output_file}")
                            # Remember which fields were saved so they remain green
                            saved_items.update(scanned_data.keys())
                            scanned_data.clear()
                            last_seen.clear()
                            print("--- Ready for next scan ---\n")

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
                # Consider a field completed if it's scanned now or was previously saved
                completed = (field in scanned_data) or (field in saved_items)
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
                saved_items.clear()
                print("\n--- Reset ---\n")

        cap.release()
        cv2.destroyAllWindows()

def main():
    camera = Camera()
    camera.start()

if __name__ == "__main__":
    main()