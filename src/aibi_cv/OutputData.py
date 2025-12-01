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

    def to_json(self, scanned_data: dict[str, str], field_order: list):
        """Try to type scanned data into a JSON file. Returns True on success.
        """
        try:
            output_data = {
                "workstation_id": self.__workstation_id,
                "timestamp": datetime.now().isoformat(),
                "barcodes": [
                    {"name": n, "value": scanned_data[n]}
                    for n in field_order if n in scanned_data
                ]
            }
            from pathlib import Path
            output_file = Path(self.__outputDir) / f"scan_{self.__workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)

                print(f"✓ Saved to {output_file}")
                # Clear scanned state so UI returns to waiting (red) state
                return True
        except Exception as e:
            print(f"[OutputData] Unexpected error in to_json: {e}")
            return False
          

    def to_exel(self, scanned_data: dict[str, str], field_order: list):
        """Try to type scanned data into Excel. Returns True on success.

        If GUI automation (pygetwindow) is not available or typing fails,
        fall back to appending a CSV file in `self.__outputDir`.
        """
        from pathlib import Path

        # If pygetwindow is not available, skip GUI automation and fall back
        if gw is None:
            print("[OutputData] pygetwindow not available; falling back to CSV export")
            return self.to_json(scanned_data, field_order)

        try:
            # Store current scanner window (if present)
            scanner_windows = [w for w in gw.getAllWindows() if self.__workstation_id in w.title]

            # Find Excel window
            excel_windows = [w for w in gw.getAllWindows() if 'excel' in w.title.lower()]

            if not excel_windows:
                print("[OutputData] Excel window not found; showing error and falling back to CSV")
                try:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Excel Not Found", "Please open Excel and try again.")
                    root.destroy()
                except Exception:
                    pass
                return self.to_json(scanned_data, field_order)

            # Activate Excel window
            try:
                excel_windows[0].activate()
                print("[OutputData] Switched to Excel window")
                time.sleep(0.5)
            except Exception as e:
                print(f"[OutputData] Failed to activate Excel window: {e}; falling back to CSV")
                return self.to_json(scanned_data, field_order)

            # Type data in config order
            try:
                for field_name in field_order:
                    if field_name in scanned_data:
                        keyboard.write(str(scanned_data[field_name]))
                    keyboard.press_and_release('tab')
                    time.sleep(0.1)

                keyboard.press_and_release('enter')
                print("[OutputData] Data successfully typed into Excel")
            except Exception as e:
                print(f"[OutputData] Error while typing to Excel")

            # Switch back to scanner window if found
            time.sleep(0.5)
            if scanner_windows:
                try:
                    scanner_windows[0].activate()
                    print("[OutputData] Successfully switched back to scanner")
                except Exception:
                    pass
            else:
                # Fallback: Try to activate OpenCV window
                try:
                    cv2.setWindowProperty(self.__workstation_id, cv2.WND_PROP_TOPMOST, 1)
                    cv2.setWindowProperty(self.__workstation_id, cv2.WND_PROP_TOPMOST, 0)
                except Exception:
                    pass

            return True
        except Exception as e:
            print(f"[OutputData] Unexpected error in to_exel")
          