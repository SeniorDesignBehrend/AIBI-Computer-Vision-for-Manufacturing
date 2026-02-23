import cv2
from datetime import datetime
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    from .DecodeQr import DecodeQr
    from .Parse import Parse
    from .OutputData import OutputData
    from .ScanSorter import ScanSorter
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
    from aibi_cv.ScanSorter import ScanSorter
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

    def _detect(self, frame):
        """Run detection using pyzbar first, then OpenCV fallbacks."""
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
                detections = self.__decode.single_opencv(frame) or []
            except Exception:
                detections = []

        return detections

    def _draw_overlays(self, frame, sorted_detections, scanned_items, need):
        """Draw detection boxes, directional arrows, and status text on frame."""
        # Draw detection polygons
        for _, box in sorted_detections:
            if box is not None:
                try:
                    pts = box.astype(int)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                except Exception:
                    pass

        # Draw directional arrows and order numbers
        if len(sorted_detections) > 1:
            try:
                centroids = []
                for _, box in sorted_detections:
                    if box is not None:
                        cx, cy = ScanSorter.centroid(box)
                        if cx is not None:
                            centroids.append((int(cx), int(cy)))

                for i in range(len(centroids) - 1):
                    pt1 = centroids[i]
                    pt2 = centroids[i + 1]
                    cv2.arrowedLine(frame, pt1, pt2, (255, 0, 255), 3, tipLength=0.3)
                    cv2.circle(frame, pt1, 20, (255, 0, 255), 2)
                    cv2.putText(frame, str(i + 1), (pt1[0] - 8, pt1[1] + 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                if centroids:
                    last_pt = centroids[-1]
                    cv2.circle(frame, last_pt, 20, (255, 0, 255), 2)
                    cv2.putText(frame, str(len(centroids)), (last_pt[0] - 8, last_pt[1] + 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            except Exception:
                pass

        # Display status text
        y_pos = 30
        cv2.putText(frame, f"Workstation: {self.__workstation_id}", (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_pos += 30

        scanned_count = len(scanned_items)
        cv2.putText(frame, f"Scanned: {scanned_count} / Needed: {need}", (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
        y_pos += 30

        for i in range(need):
            if i < len(scanned_items):
                itm = scanned_items[i]
                if itm.get('name'):
                    display_text = f"✓ {itm['name']}: {itm['value']}"
                else:
                    display_text = f"✓ {itm['value']}"
                color = (0, 255, 0)
            else:
                display_text = f"✗ slot {i + 1}"
                color = (0, 0, 255)
            cv2.putText(frame, display_text, (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            y_pos += 25

        if scanned_count >= need:
            cv2.putText(frame, "AUTO-ENTERING TO EXCEL...", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return y_pos

    def start(self):
        config = self.__config
        if not config:
            config = self.__config_manager.get_config(self.__workstation_id)
        if not config:
            config = self.__config_manager.create_default_config(self.__workstation_id)

        expected_qr_count = config.expected_qr_count
        scan_direction = config.scan_direction
        append_key = config.append_key

        try:
            need = int(expected_qr_count) if expected_qr_count is not None else 1
        except Exception:
            need = 1

        # Tracking: use a list of dicts for stable ordering
        scanned_items: List[Dict[str, Optional[str]]] = []
        last_seen: Dict[str, int] = {}
        cooldown_frames = 30
        frame_count = 0

        cap = cv2.VideoCapture(config.camera_index)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return

        window_name = 'Advanced Scanner'

        print(f"=== Advanced Scanner - {self.__workstation_id} ===")
        print(f"Expected QR count: {expected_qr_count}")
        print(f"Scan direction: {scan_direction}")
        print(f"Append key: {append_key}")
        print("\nFormat barcodes as: field_name:value")
        print("Data will auto-enter to Excel, then freeze for confirmation")
        print("Press 'r' to reset, 'q' to quit\n")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            detections = self._detect(frame)

            # Sort detections by direction only when enough are visible
            if scan_direction and scan_direction != 'any' and len(detections) >= need:
                sorted_detections = ScanSorter.sort(detections, scan_direction)
            else:
                sorted_detections = detections

            # Only register scans when enough codes are visible in the same frame
            if len(detections) >= need:
                for text, box in sorted_detections:
                    try:
                        name, value = self.__parse.parse(text)
                    except Exception:
                        name, value = None, text

                    raw_text = text if isinstance(text, str) else str(text)

                    # Cooldown based on raw text
                    if raw_text in last_seen and (frame_count - last_seen[raw_text]) < cooldown_frames:
                        continue

                    # Avoid duplicates
                    if not any(item.get('text') == raw_text for item in scanned_items):
                        scanned_items.append({'name': name, 'value': value, 'text': raw_text})
                        last_seen[raw_text] = frame_count
                        display_key = name if name else value
                        print(f"✓ Scanned: {display_key} = {value}")

            # Draw overlays
            self._draw_overlays(frame, sorted_detections, scanned_items, need)

            cv2.imshow(window_name, frame)

            # Auto-enter and freeze when we have enough items
            if len(scanned_items) >= need:
                print("\n✓ All codes detected - Auto-entering to Excel...")

                # Build dict for OutputData
                scanned_data = {}
                for itm in scanned_items:
                    key = itm['name'] if itm['name'] else itm['value']
                    scanned_data[key] = itm['value']

                ok = self.__output.to_exel(scanned_data, None, append_key)
                if not ok:
                    self.__output.to_json(scanned_data, None)

                # Show freeze frame after data entry
                frozen_frame = frame.copy()
                cv2.putText(frozen_frame, "DATA ENTERED - Press ENTER for next scan",
                            (10, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.imshow(window_name, frozen_frame)
                print("\nPress ENTER to scan next set of codes...\n")

                while True:
                    freeze_key = cv2.waitKey(100) & 0xFF
                    if freeze_key == 13:  # Enter key
                        break
                    elif freeze_key == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                scanned_items.clear()
                last_seen.clear()
                print("--- Ready for next scan ---\n")

            # Handle keys and window close
            key = cv2.waitKey(1) & 0xFF

            try:
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
            except Exception:
                pass

            if key == ord('q'):
                break
            elif key == ord('r'):
                scanned_items.clear()
                last_seen.clear()
                print("\n--- Reset ---\n")

        cap.release()
        cv2.destroyAllWindows()

def main():
    camera = Camera("workstation_1")
    camera.start()

if __name__ == "__main__":
    main()
