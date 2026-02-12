#!/usr/bin/env python3
"""Advanced QR/Barcode scanner with dynamic barcode tracking."""

import cv2
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, List, Optional
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


    def type_to_excel(scanned_data, field_order: list | None = None, append_key: str = "TAB"):
        """Type scanned data into Excel.

        `scanned_data` may be either a dict mapping field->value or a list of
        scanned items [{'name':..., 'value':...}]. `field_order` optional; `append_key` is TAB|ENTER|NONE.
        """
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
            try:
                root = tk.Tk()
                root.withdraw()  # Hide main window
                messagebox.showerror("Excel Not Found", "Please open Excel and try again.")
                root.destroy()
            except Exception:
                pass
            print("\n⚠️ Excel not found - please open Excel")
            return False

        # Normalize scanned_data to ordered keys and values
        if isinstance(scanned_data, dict):
            keys = field_order if field_order is not None else list(scanned_data.keys())
            values = [scanned_data.get(k) for k in keys]
        else:
            # assume list of items
            items = list(scanned_data)
            if field_order:
                # map by name if names are present
                values = []
                for name in field_order:
                    for itm in items:
                        if itm.get('name') == name:
                            values.append(itm.get('value'))
                            break
                # fill remaining with unnamed values
                for itm in items:
                    if itm.get('name') is None:
                        values.append(itm.get('value'))
            else:
                values = [itm.get('value') for itm in items]
        append_map = {"TAB": "tab", "ENTER": "enter", "NONE": None}
        mapped = append_map.get((append_key or "").upper(), "tab")

        # Type data in configuration order
        try:
            for v in values:
                if v is None:
                    continue
                keyboard.write(str(v))
                if mapped:
                    keyboard.press_and_release(mapped)
                time.sleep(0.1)

            try:
                keyboard.press_and_release('enter')
            except Exception:
                pass
            print("✓ Data typed into Excel")
        except Exception as e:
            print(f"Error typing to Excel: {e}")

        # Switch back to scanner
        time.sleep(0.5)
        if scanner_windows:
            try:
                scanner_windows[0].activate()
                print("✓ Switched back to scanner")
            except Exception:
                pass
        else:
            try:
                cv2.setWindowProperty('Advanced Scanner', cv2.WND_PROP_TOPMOST, 1)
                cv2.setWindowProperty('Advanced Scanner', cv2.WND_PROP_TOPMOST, 0)
            except Exception:
                pass
        return True


    def main():
        # Setup paths
        project_root = Path(__file__).parent.parent.parent
        config_dir = project_root / "data" / "config"
        output_dir = project_root / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Load workstation config
        workstation_id = "workstation_11"
        config_manager = ConfigManager(config_dir)
        config = config_manager.get_config(workstation_id)
        
        if not config:
            config = config_manager.create_default_config(workstation_id)
            print(f"Created default config for {workstation_id}")
        
        # New config shape: use expected_qr_count, scan_direction, append_key
        expected_qr_count = getattr(config, 'expected_qr_count', None)
        scan_direction = getattr(config, 'scan_direction', 'any')
        append_key = getattr(config, 'append_key', 'TAB')
        field_order = None

        # Fallback: also check top-level `configs/` directory and prefer values there
        try:
            fallback_cfg = project_root / "configs" / f"{workstation_id}.json"
            if fallback_cfg.exists():
                with open(fallback_cfg, 'r') as f:
                    fb = json.load(f)
                    if fb.get('expected_qr_count') is not None:
                        expected_qr_count = fb.get('expected_qr_count')
                        print(f"Using expected_qr_count from {fallback_cfg}")
                    if fb.get('scan_direction') is not None:
                        scan_direction = fb.get('scan_direction')
                        print(f"Using scan_direction from {fallback_cfg}: {scan_direction}")
                    if fb.get('append_key') is not None:
                        append_key = fb.get('append_key')
                        print(f"Using append_key from {fallback_cfg}: {append_key}")
                    # camera_index fallback
                    if fb.get('camera_index') is not None:
                        camera_index = fb.get('camera_index')
                    else:
                        camera_index = getattr(config, 'camera_index', 0)
            else:
                camera_index = getattr(config, 'camera_index', 0)
        except Exception:
            camera_index = getattr(config, 'camera_index', 0)

        # Determine how many QRs are required for a complete scan
        try:
            need = int(expected_qr_count) if expected_qr_count is not None else 1
        except Exception:
            need = 1
        
        # Tracking
        scanned_items: List[Dict[str, Optional[str]]] = []  # ordered list of scanned items: {'name':..., 'value':..., 'text':...}
        last_seen: Dict[str, int] = {}  # Track when each raw text was last seen
        cooldown_frames = 30  # Ignore same code for 30 frames (~1 second)
        frame_count = 0
        
        # Open camera
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print(f"=== Advanced Scanner - {workstation_id} ===")
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
            
            # Detect QR codes
            detections = AdvancedScanner.decode_qr(frame)
            
            # Process detections (apply ordering later)
            sorted_detections = detections
            # centroid helper
            def _centroid(box):
                try:
                    import numpy as _np
                    pts = _np.array(box, dtype=float)
                    cx = pts[:, 0].mean()
                    cy = pts[:, 1].mean()
                    return cx, cy
                except Exception:
                    return None, None

            # Only apply directional ordering once we have enough detections in-frame
            if scan_direction and scan_direction != 'any' and len(detections) >= need:
                try:
                    import numpy as _np

                    # compute centroids for all detections
                    centroids = []
                    for item in detections:
                        _, box = item
                        cx, cy = _centroid(box)
                        centroids.append((cx, cy))

                    # collect valid cy values
                    valid_cys = [c[1] for c in centroids if c[1] is not None]
                    if len(valid_cys) >= 2:
                        sorted_cys = sorted(valid_cys)
                        diffs = [_np.diff(_np.array(sorted_cys))]
                        # estimate typical vertical gap between rows
                        try:
                            # median of adjacent differences
                            gaps = _np.diff(_np.array(sorted_cys))
                            median_gap = float(_np.median(gaps)) if gaps.size else 0.0
                        except Exception:
                            median_gap = float(sorted_cys[-1] - sorted_cys[0]) / max(1, len(sorted_cys)-1)
                        row_thresh = max(10.0, median_gap * 0.75)
                    else:
                        row_thresh = 10.0

                    # assign row indices by scanning sorted by cy
                    items_with_pos = []
                    for (item, (cx, cy)) in zip(detections, centroids):
                        items_with_pos.append({'item': item, 'cx': cx, 'cy': cy, 'row': None})

                    # sort by cy to assign rows
                    items_with_pos.sort(key=lambda x: (float('inf') if x['cy'] is None else x['cy']))
                    current_row = 0
                    prev_cy = None
                    for entry in items_with_pos:
                        cy = entry['cy']
                        if cy is None:
                            entry['row'] = 9999
                            continue
                        if prev_cy is None:
                            entry['row'] = current_row
                            prev_cy = cy
                            continue
                        if abs(cy - prev_cy) > row_thresh:
                            current_row += 1
                        entry['row'] = current_row
                        prev_cy = cy

                    # now sort within rows according to direction
                    def _row_sort_key(e):
                        cx = e['cx']
                        row = e['row']
                        if cx is None:
                            cx_val = float('inf')
                        else:
                            cx_val = cx
                        if scan_direction in ('row-major', 'left-to-right-down'):
                            return (row, cx_val)
                        if scan_direction == 'right-to-left-down':
                            return (row, -cx_val)
                        if scan_direction in ('column-major', 'top-to-bottom-left-to-right'):
                            return (cx_val, row)
                        if scan_direction == 'left-to-right':
                            return (0, cx_val)
                        if scan_direction == 'right-to-left':
                            return (0, -cx_val)
                        if scan_direction == 'top-to-bottom':
                            return (row, 0)
                        if scan_direction == 'bottom-to-top':
                            return (-row, 0)
                        return (row, cx_val)

                    items_with_pos.sort(key=_row_sort_key)
                    # extract sorted detections
                    sorted_detections = [e['item'] for e in items_with_pos]
                except Exception:
                    sorted_detections = detections
            else:
                # keep original detection order until enough codes are visible
                sorted_detections = detections

            # Only register scans when enough codes are visible in the same frame
            if len(detections) >= need:
                for idx, (text, box) in enumerate(sorted_detections, start=1):
                    name, value = AdvancedScanner.parse_barcode(text)
                    raw_text = text if isinstance(text, str) else str(text)

                    # cooldown based on raw_text
                    if raw_text in last_seen and (frame_count - last_seen[raw_text]) < cooldown_frames:
                        continue

                    # avoid adding duplicates (same raw_text)
                    if not any(item.get('text') == raw_text for item in scanned_items):
                        scanned_items.append({'name': name, 'value': value, 'text': raw_text})
                        last_seen[raw_text] = frame_count
                        display_key = name if name else value
                        print(f"✓ Scanned: {display_key} = {value}")

                        # auto-enter when we have enough items
                        if len(scanned_items) >= need:
                            print("\nExpected QR count reached - auto-entering...\n")
                            # try to type to excel
                            ok = AdvancedScanner.type_to_excel(scanned_items, field_order, append_key)
                            if not ok:
                                # fallback to JSON
                                output_data = {
                                    "workstation_id": workstation_id,
                                    "timestamp": datetime.now().isoformat(),
                                    "barcodes": [
                                        {"name": itm.get('name'), "value": itm.get('value')} for itm in list(scanned_items)
                                    ]
                                }
                                output_file = output_dir / f"scan_{workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                                with open(output_file, 'w') as f:
                                    json.dump(output_data, f, indent=2)
                                print(f"✓ Saved to {output_file}")
                                scanned_items.clear()
                                last_seen.clear()
                                print("--- Ready for next scan ---\n")
            else:
                # Not enough codes in-frame to register scans yet
                pass

            # Draw all detected boxes (safe: do this regardless of registration)
            for _, box in sorted_detections:
                if box is not None:
                    try:
                        pts = box.astype(int)
                        cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                    except Exception:
                        pass
            
            # Check completion: require `need` number of scanned items
            missing_required = len(scanned_items) < need
            
            # Display status
            y_pos = 30
            cv2.putText(frame, f"Workstation: {workstation_id}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_pos += 30

            # Display scanned vs needed count
            scanned_count = len(scanned_items)
            cv2.putText(frame, f"Scanned: {scanned_count} / Needed: {need}", (10, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 0), 2)
            y_pos += 30
            # Display scanned items (show up to `need` entries)
            for i in range(need):
                if i < len(scanned_items):
                    itm = scanned_items[i]
                    if itm.get('name'):
                        display_text = f"✓ {itm.get('name')}: {itm.get('value')}"
                        color = (0, 255, 0)
                    else:
                        display_text = f"✓ {itm.get('value')}"
                        color = (0, 255, 0)
                else:
                    display_text = f"✗ slot {i+1}"
                    color = (0, 0, 255)
                cv2.putText(frame, display_text, (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                y_pos += 25

            if not missing_required:
                cv2.putText(frame, "AUTO-ENTERING TO EXCEL...", (10, y_pos),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Advanced Scanner', frame)
            
            # Handle keys and window close. Use both OpenCV key and keyboard fallback
            # so 'q' works even if the OpenCV window isn't focused.
            key = cv2.waitKey(1) & 0xFF
            # If OpenCV reports window closed, exit loop
            try:
                if cv2.getWindowProperty('Advanced Scanner', cv2.WND_PROP_VISIBLE) < 1:
                    break
            except Exception:
                pass

            # Primary quit via OpenCV key
            if key == ord('q'):
                break
            elif key == ord('r'):
                scanned_items.clear()
                last_seen.clear()
                print("\n--- Reset ---\n")

            # Fallback: check global keyboard state (non-blocking)
            try:
                if keyboard.is_pressed('q'):
                    break
            except Exception:
                # keyboard may require elevated permissions, ignore if unavailable
                pass

        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    AdvancedScanner.main()
