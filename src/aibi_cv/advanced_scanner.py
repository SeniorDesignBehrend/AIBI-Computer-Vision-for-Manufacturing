#!/usr/bin/env python3
"""Advanced QR/Barcode scanner with dynamic barcode tracking."""

import cv2
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Set
import keyboard
import time
import pygetwindow as gw
import tkinter as tk
from tkinter import messagebox

from .config_manager import ConfigManager

class AdvancedScanner:

    def __init__(self):
        pass

    def decode_qr(img):
        """Decode QR/barcodes from `img`.

        Attempts to use `pyzbar` first (reliable multi-barcode detection for many
        symbologies). Falls back to OpenCV's `QRCodeDetector.detectAndDecodeMulti`.

        Returns a list of tuples `(text, points)` where `points` is either a
        numpy array of polygon points or `None` if not available.
        """
        results = []

        # Prefer pyzbar when available (handles multiple barcodes reliably)
        try:
            from pyzbar.pyzbar import decode as pyzbar_decode
            try:
                decoded = pyzbar_decode(img)
                if decoded:
                    import numpy as _np
                    for d in decoded:
                        try:
                            text = d.data.decode('utf-8') if isinstance(d.data, (bytes, bytearray)) else str(d.data)
                        except Exception:
                            text = str(d.data)

                        pts = None
                        if getattr(d, 'polygon', None):
                            try:
                                pts = _np.array([[p.x, p.y] for p in d.polygon], dtype=int)
                            except Exception:
                                pts = None

                        results.append((text, pts))
                    return results
            except Exception:
                # If pyzbar fails for some reason, fall through to OpenCV fallback
                results = []
        except Exception:
            # pyzbar not installed or import failed; use OpenCV fallback
            pass

        # OpenCV fallback: try multi-detect-decode first
        try:
            detector = cv2.QRCodeDetector()
            res = detector.detectAndDecodeMulti(img)

            # detectAndDecodeMulti has different return shapes across OpenCV
            # versions; attempt to normalize to (texts, points)
            texts = None
            points = None
            if isinstance(res, tuple) and len(res) >= 2:
                # Try to find the list-of-strings and the points array inside the tuple
                for item in res:
                    if isinstance(item, (list, tuple)) and item and all(isinstance(x, str) for x in item):
                        texts = list(item)
                    elif hasattr(item, 'shape') or (isinstance(item, (list, tuple)) and item and isinstance(item[0], (list, tuple))):
                        points = item
            elif isinstance(res, list):
                # Some bindings may return a list-of-texts directly
                texts = res

            if texts:
                import numpy as _np
                for i, t in enumerate(texts):
                    if not t:
                        continue
                    pts = None
                    try:
                        if points is not None:
                            pts = _np.array(points[i], dtype=int)
                    except Exception:
                        pts = None
                    results.append((t, pts))
                if results:
                    return results
        except Exception:
            pass

        # Final fallback: single QR decode
        try:
            detector = cv2.QRCodeDetector()
            text, pts, _ = detector.detectAndDecode(img)
            if text:
                try:
                    import numpy as _np
                    pts_arr = _np.array(pts, dtype=int) if pts is not None else None
                except Exception:
                    pts_arr = None
                return [(text, pts_arr)]
        except Exception:
            pass

        return []


    def parse_barcode(data: str) -> tuple:
        """Parse barcode data to extract name and value."""
        # Try to parse as JSON first
        try:
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                # Get first key-value pair
                for key, value in json_data.items():
                    return key, str(value)
        except:
            pass
        
        # Fallback to colon format
        if ":" in data:
            parts = data.split(":", 1)
            return parts[0].strip(), parts[1].strip()
        return None, data


    def type_to_excel(scanned_data: Dict[str, str], field_order: list):
        """Type scanned data into Excel using keyboard simulation in configured order."""
        # Store current scanner window
        scanner_windows = [w for w in gw.getAllWindows() if 'Advanced Scanner' in w.title]
        
        # Find Excel window
        excel_windows = [w for w in gw.getAllWindows() if 'excel' in w.title.lower()]
        
        if excel_windows:
            excel_windows[0].activate()
            print("\n✓ Switched to Excel")
            time.sleep(0.5)
        else:
            # Show popup window
            root = tk.Tk()
            root.withdraw()  # Hide main window
            messagebox.showerror("Excel Not Found", "Please open Excel and try again.")
            root.destroy()
            print("\n⚠️ Excel not found - please open Excel")
            return False
        
        # Type data in configuration order
        for field_name in field_order:
            if field_name in scanned_data:
                keyboard.write(scanned_data[field_name])
            keyboard.press_and_release('tab')
            time.sleep(0.1)
        
        keyboard.press_and_release('enter')
        print("✓ Data typed into Excel")
        
        # Switch back to scanner
        time.sleep(0.5)
        if scanner_windows:
            scanner_windows[0].activate()
            print("✓ Switched back to scanner")
        else:
            # Fallback: try to activate OpenCV window
            cv2.setWindowProperty('Advanced Scanner', cv2.WND_PROP_TOPMOST, 1)
            cv2.setWindowProperty('Advanced Scanner', cv2.WND_PROP_TOPMOST, 0)
        return True


    def main():
        # Setup paths
        project_root = Path(__file__).parent.parent.parent
        config_dir = project_root / "data" / "config"
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Load workstation config
        workstation_id = "workstation_01"
        config_manager = ConfigManager(config_dir)
        config = config_manager.get_config(workstation_id)
        
        if not config:
            config = config_manager.create_default_config(workstation_id)
            print(f"Created default config for {workstation_id}")
        
        # Build required fields set and maintain order
        required_fields: Set[str] = {f.name for f in config.barcode_fields if f.required}
        optional_fields: Set[str] = {f.name for f in config.barcode_fields if not f.required}
        all_fields = required_fields | optional_fields
        field_order = [f.name for f in config.barcode_fields]  # Maintain config order
        
        # Tracking
        scanned_data: Dict[str, str] = {}
        last_seen: Dict[str, int] = {}  # Track when each code was last seen
        cooldown_frames = 30  # Ignore same code for 30 frames (~1 second)
        frame_count = 0
        
        # Open camera
        cap = cv2.VideoCapture(config.camera_index)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print(f"=== Advanced Scanner - {workstation_id} ===")
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
            
            # Detect QR codes
            detections = decode_qr(frame)
            
            # Process detections
            for text, box in detections:
                name, value = parse_barcode(text)
                
                # Check cooldown, if the same code has been seen in the last N frames, then skip
                if name in last_seen and (frame_count - last_seen[name]) < cooldown_frames:
                    continue
                
                # Only track barcodes in our field list
                if name and name in all_fields and name not in scanned_data:
                    scanned_data[name] = value
                    last_seen[name] = frame_count
                    print(f"✓ Scanned: {name} = {value}")
                    
                    # Check if all required fields are now complete
                    if required_fields.issubset(scanned_data.keys()):
                        print("\nAll required fields scanned - auto-entering to Excel...")
                        
                        # Type to Excel in configured order
                        if not type_to_excel(scanned_data, field_order):
                            print("Error: Excel not found, scan data will not be saved/reset.")
                            continue  # Excel not found, don't save/reset
                        
                        # Save to JSON in configured order
                        output_data = {
                            "workstation_id": workstation_id,
                            "timestamp": datetime.now().isoformat(),
                            "barcodes": [
                                {"name": name, "value": scanned_data[name]}
                                for name in field_order if name in scanned_data
                            ]
                        }
                        
                        output_file = output_dir / f"scan_{workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        with open(output_file, 'w') as f:
                            json.dump(output_data, f, indent=2)
                        
                        print(f"✓ Saved to {output_file}")
                        scanned_data.clear()
                        last_seen.clear()
                        print("--- Ready for next scan ---\n")
                
                # Draw on frame
                if box is not None:
                    pts = box.astype(int)
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
            
            # Check completion
            scanned_required = required_fields & scanned_data.keys()
            missing_required = required_fields - scanned_data.keys()
            
            # Display status
            y_pos = 30
            cv2.putText(frame, f"Workstation: {workstation_id}", (10, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_pos += 30
            
            for field in required_fields:
                if field in scanned_data:
                    display_text = f"✓ {field}: {scanned_data[field]}"
                    color = (0, 255, 0)
                else:
                    display_text = f"✗ {field}"
                    color = (0, 0, 255)
                cv2.putText(frame, display_text, (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                y_pos += 25
            
            if not missing_required:
                cv2.putText(frame, "AUTO-ENTERING TO EXCEL...", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Advanced Scanner', frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                scanned_data.clear()
                last_seen.clear()
                print("\n--- Reset ---\n")

        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
