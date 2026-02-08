import time
from datetime import datetime
import json
import keyboard

try:
    import pygetwindow as gw
    import tkinter as tk
    from tkinter import messagebox
    import cv2
except Exception:
    gw = None

class OutputData:
    __workstation_id: str ## These are private variables
    __outputDir: str

    def __init__(self, workstation_id: str, outputDir: str ):
        self.__workstation_id = workstation_id
        self.__outputDir = outputDir

    def to_json(self, scanned_data: dict[str, str], field_order: list | None = None):
        """Save scanned data to JSON. Returns True on success."""
        try:
            keys = field_order if field_order is not None else list(scanned_data.keys())
            output_data = {
                "workstation_id": self.__workstation_id,
                "timestamp": datetime.now().isoformat(),
                "barcodes": [
                    {"name": n, "value": scanned_data[n]}
                    for n in keys if n in scanned_data
                ]
            }
            from pathlib import Path
            output_dir_path = Path(self.__outputDir)
            output_dir_path.mkdir(parents=True, exist_ok=True)

            output_file = output_dir_path / f"scan_{self.__workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)

            print(f"✓ Saved to {output_file}")
            return True
        except Exception as e:
            print(f"[OutputData] Unexpected error in to_json: {e}")
            return False


    def to_exel(self, scanned_data: dict[str, str], field_order: list | None = None, append_key: str = "TAB"):
        """Type scanned data into Excel. Returns True on success.

        - `field_order` optional: when None, types values in insertion order of `scanned_data`.
        - `append_key`: one of "TAB", "ENTER", "NONE".
        """
        from pathlib import Path

        # Normalize keys order
        keys = field_order if field_order is not None else list(scanned_data.keys())

        # If pygetwindow not available, fallback to JSON
        if gw is None:
            print("[OutputData] pygetwindow not available; falling back to JSON export")
            return self.to_json(scanned_data, keys)

        try:
            scanner_windows = [w for w in gw.getAllWindows() if self.__workstation_id in w.title]
            excel_windows = [w for w in gw.getAllWindows() if 'excel' in w.title.lower()]

            if not excel_windows:
                print("[OutputData] Excel window not found; showing error and falling back to JSON")
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Excel Not Found", "Please open Excel and try again.")
                    root.destroy()
                except Exception:
                    pass
                return self.to_json(scanned_data, keys)

            try:
                excel_windows[0].activate()
                print("[OutputData] Switched to Excel window")
                time.sleep(0.5)
            except Exception as e:
                print(f"[OutputData] Failed to activate Excel window: {e}; falling back to JSON")
                return self.to_json(scanned_data, keys)

            # Map append_key to keyboard key names (keyboard library expects names like 'tab'/'enter')
            append_key_map = {"TAB": "tab", "ENTER": "enter", "NONE": None}
            mapped = append_key_map.get((append_key or "").upper(), "tab")

            try:
                for i, name in enumerate(keys):
                    if name in scanned_data:
                        keyboard.write(str(scanned_data[name]))
                    # Press between-field key unless NONE
                    if mapped:
                        keyboard.press_and_release(mapped)
                    time.sleep(0.1)

                # Finalize row by pressing Enter (best-effort) to submit the row in Excel
                try:
                    keyboard.press_and_release('enter')
                except Exception:
                    pass

                print("[OutputData] Data successfully typed into Excel")
            except Exception as e:
                print(f"[OutputData] Error while typing to Excel: {e}")

            # Switch back to scanner window if found
            time.sleep(0.5)
            if scanner_windows:
                try:
                    scanner_windows[0].activate()
                    print("[OutputData] Successfully switched back to scanner")
                except Exception:
                    pass
            else:
                try:
                    cv2.setWindowProperty(self.__workstation_id, cv2.WND_PROP_TOPMOST, 1)
                    cv2.setWindowProperty(self.__workstation_id, cv2.WND_PROP_TOPMOST, 0)
                except Exception:
                    pass

            return True
        except Exception as e:
            print(f"[OutputData] Unexpected error in to_exel: {e}")
            return False
