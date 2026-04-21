import sys
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QListWidget, 
                               QListWidgetItem, QGroupBox, QComboBox)
from PySide6.QtCore import QTimer, Qt, Signal, QThread
from PySide6.QtGui import QImage, QPixmap, QFont
import cv2

try:
    from .DecodeQr import DecodeQr
    from .Parse import Parse
    from .OutputData import OutputData
    from .ScanSorter import ScanSorter
    from .config_manager import ConfigManager
except Exception:
    repo_src = Path(__file__).resolve().parents[1]
    if str(repo_src) not in sys.path:
        sys.path.insert(0, str(repo_src))
    from aibi_cv.DecodeQr import DecodeQr
    from aibi_cv.Parse import Parse
    from aibi_cv.OutputData import OutputData
    from aibi_cv.ScanSorter import ScanSorter
    from aibi_cv.config_manager import ConfigManager


class CameraThread(QThread):
    frame_ready = Signal(np.ndarray)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None
        
    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.running = True
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)
            self.msleep(30)
    
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()


class Camera(QMainWindow):

    __decode: DecodeQr
    __parse: Parse
    __output: OutputData
    __workstation_id: str
    __config_manager: ConfigManager

    def __init__(self, workstationId: str):
        super().__init__()
        self.__workstation_id = workstationId
        self.__decode = DecodeQr()
        self.__parse = Parse()
        self.__output = OutputData(self.__workstation_id, "./output")
        self.__config_manager = ConfigManager("./configs")
        self.__config = self.__config_manager.get_config(self.__workstation_id)
        
        if not self.__config:
            self.__config = self.__config_manager.create_default_config(self.__workstation_id)
        
        self.__scanned_items: List[Dict[str, Optional[str]]] = []
        self.__last_seen: Dict[str, int] = {}
        self.__frame_count = 0
        self.__cooldown_frames = 30
        self.__camera_thread = None
        self.__current_frame = None
        self.__frozen = False
        self.__last_sorted_detections = []
        self.__dark_mode = True
        self.__last_excel_data = None
        
        self._init_ui()
        self._start_camera()

    def _init_ui(self):
        self.setWindowTitle(f"Barcode Scanner - {self.__workstation_id}")
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Camera feed
        left_panel = QVBoxLayout()
        self.__video_label = QLabel()
        self.__video_label.setMinimumSize(800, 600)
        self.__video_label.setStyleSheet("border: 2px solid #333; background-color: black;")
        self.__video_label.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(self.__video_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.__quit_btn = QPushButton("Quit (Q)")
        self.__quit_btn.clicked.connect(self.close)
        self.__continue_btn = QPushButton("Continue (Enter)")
        self.__continue_btn.clicked.connect(self._continue_scan)
        self.__continue_btn.setEnabled(False)
        self.__undo_btn = QPushButton("Undo Excel (U)")
        self.__undo_btn.clicked.connect(self._undo_excel)
        self.__undo_btn.setEnabled(False)
        self.__theme_btn = QPushButton("🌙")
        self.__theme_btn.setMaximumWidth(50)
        self.__theme_btn.setToolTip("Toggle Theme (T)")
        self.__theme_btn.clicked.connect(self._toggle_theme)
        button_layout.addWidget(self.__quit_btn)
        button_layout.addWidget(self.__continue_btn)
        button_layout.addWidget(self.__undo_btn)
        button_layout.addWidget(self.__theme_btn)
        left_panel.addLayout(button_layout)
        
        main_layout.addLayout(left_panel, 3)
        
        # Right panel - Info and scanned items
        right_panel = QVBoxLayout()
        
        # Workstation info
        info_group = QGroupBox("Workstation Info")
        info_layout = QVBoxLayout()
        
        ws_layout = QHBoxLayout()
        ws_layout.addWidget(QLabel("<b>Workstation:</b>"))
        self.__workstation_combo = QComboBox()
        self.__workstation_combo.currentTextChanged.connect(self._change_workstation)
        self._populate_workstations()
        ws_layout.addWidget(self.__workstation_combo)
        info_layout.addLayout(ws_layout)
        
        self.__expected_label = QLabel(f"<b>Expected QR Count:</b> {self.__config.expected_qr_count}")
        self.__direction_label = QLabel(f"<b>Scan Direction:</b> {self.__config.scan_direction}")
        
        info_layout.addWidget(self.__expected_label)
        info_layout.addWidget(self.__direction_label)
        info_group.setLayout(info_layout)
        right_panel.addWidget(info_group)
        
        # Scanned items list
        scan_group = QGroupBox("Scanned Items")
        scan_layout = QVBoxLayout()
        
        self.__status_label = QLabel("Scanned: 0 / Needed: 0")
        self.__status_label.setFont(QFont("Arial", 12, QFont.Bold))
        scan_layout.addWidget(self.__status_label)
        
        self.__scan_list = QListWidget()
        self.__scan_list.setStyleSheet("QListWidget { font-size: 11pt; }")
        scan_layout.addWidget(self.__scan_list)
        
        scan_group.setLayout(scan_layout)
        right_panel.addWidget(scan_group)
        
        main_layout.addLayout(right_panel, 1)
        
        self._apply_theme()
    
    def _apply_theme(self):
        if self.__dark_mode:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QGroupBox {
                    border: 2px solid #555;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-weight: bold;
                    color: #ffffff;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QLabel {
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #3a3a3a;
                    color: #ffffff;
                    border: 1px solid #555;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    color: #666;
                }
                QListWidget {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #555;
                    border-radius: 4px;
                    font-size: 11pt;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f5f5f5;
                    color: #000000;
                }
                QGroupBox {
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                    font-weight: bold;
                    color: #000000;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QLabel {
                    color: #000000;
                }
                QPushButton {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11pt;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
                QPushButton:disabled {
                    background-color: #e0e0e0;
                    color: #999;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #000000;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 11pt;
                }
            """)
        need = int(self.__config.expected_qr_count) if self.__config.expected_qr_count else 1
        self._update_status(len(self.__scanned_items), need)
    
    def _toggle_theme(self):
        self.__dark_mode = not self.__dark_mode
        self.__theme_btn.setText("☀️" if self.__dark_mode else "🌙")
        self._apply_theme()
    
    def _populate_workstations(self):
        available = sorted(self.__config_manager.configs.keys())
        self.__workstation_combo.blockSignals(True)
        self.__workstation_combo.clear()
        self.__workstation_combo.addItems(available)
        idx = self.__workstation_combo.findText(self.__workstation_id)
        if idx >= 0:
            self.__workstation_combo.setCurrentIndex(idx)
        self.__workstation_combo.blockSignals(False)
    
    def _change_workstation(self, new_id):
        if not new_id or new_id == self.__workstation_id:
            return
        
        self.__workstation_id = new_id
        self.__config = self.__config_manager.get_config(new_id)
        if not self.__config:
            self.__config = self.__config_manager.create_default_config(new_id)
        
        self.__output = OutputData(self.__workstation_id, "./output")
        self.setWindowTitle(f"Barcode Scanner - {self.__workstation_id}")
        self.__expected_label.setText(f"<b>Expected QR Count:</b> {self.__config.expected_qr_count}")
        self.__direction_label.setText(f"<b>Scan Direction:</b> {self.__config.scan_direction}")
        
        if self.__camera_thread:
            self.__camera_thread.stop()
            self.__camera_thread.wait()
        
        self._reset_scan()
        self._start_camera()
    
    def _start_camera(self):
        self.__camera_thread = CameraThread(self.__config.camera_index)
        self.__camera_thread.frame_ready.connect(self._process_frame)
        self.__camera_thread.start()
    
    def _display_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.__video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.__video_label.setPixmap(scaled_pixmap)
    
    def _update_status(self, scanned, needed):
        self.__status_label.setText(f"Scanned: {scanned} / Needed: {needed}")
        if scanned >= needed:
            self.__status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            color = "#ffffff" if self.__dark_mode else "#000000"
            self.__status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def _update_scan_list(self):
        self.__scan_list.clear()
        for item in self.__scanned_items:
            display_key = item['name'] if item['name'] else item['value']
            list_item = QListWidgetItem(f"✓ {display_key}: {item['value']}")
            list_item.setForeground(Qt.darkGreen)
            self.__scan_list.addItem(list_item)
    
    def _auto_enter(self):
        self.__frozen = True
        self.__continue_btn.setEnabled(True)
        
        # Build data dict
        scanned_data = {}
        for itm in self.__scanned_items:
            key = itm['name'] if itm['name'] else itm['value']
            scanned_data[key] = itm['value']
        
        print(f"[Camera] Attempting to enter data to Excel: {scanned_data}")
        
        # Store for undo
        self.__last_excel_data = scanned_data.copy()
        
        # Save data
        append_key = self.__config.append_key
        ok = self.__output.to_exel(scanned_data, None, append_key)
        print(f"[Camera] Excel entry result: {ok}")
        if not ok:
            print("[Camera] Excel failed, saving to JSON instead")
            self.__output.to_json(scanned_data, None)
        else:
            self.__undo_btn.setEnabled(True)
        
        # Show frozen frame with scan order visualization
        if self.__current_frame is not None:
            frozen_frame = self.__current_frame.copy()
            
            # Draw the scan order lines and arrows on freeze frame
            if len(self.__last_sorted_detections) > 1:
                try:
                    centroids = []
                    for _, box in self.__last_sorted_detections:
                        if box is not None:
                            cx, cy = ScanSorter.centroid(box)
                            if cx is not None:
                                centroids.append((int(cx), int(cy)))

                    for i in range(len(centroids) - 1):
                        pt1 = centroids[i]
                        pt2 = centroids[i + 1]
                        cv2.arrowedLine(frozen_frame, pt1, pt2, (255, 0, 255), 3, tipLength=0.3)
                        cv2.circle(frozen_frame, pt1, 20, (255, 0, 255), 2)
                        cv2.putText(frozen_frame, str(i + 1), (pt1[0] - 8, pt1[1] + 8),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    if centroids:
                        last_pt = centroids[-1]
                        cv2.circle(frozen_frame, last_pt, 20, (255, 0, 255), 2)
                        cv2.putText(frozen_frame, str(len(centroids)), (last_pt[0] - 8, last_pt[1] + 8),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                except Exception:
                    pass
            
            cv2.putText(frozen_frame, "DATA ENTERED - Press Continue",
                        (10, frozen_frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            self._display_frame(frozen_frame)
    
    def _undo_excel(self):
        if self.__last_excel_data is None:
            return
        
        try:
            import pygetwindow as gw
            import keyboard
            import time
            
            excel_windows = [w for w in gw.getAllWindows() if 'excel' in w.title.lower()]
            if not excel_windows:
                print("[Undo] Excel window not found")
                return
            
            excel_windows[0].activate()
            time.sleep(0.3)
            
            # Move up one row
            keyboard.press_and_release('up')
            time.sleep(0.1)
            
            # Select the entire row and delete
            keyboard.press_and_release('shift+space')
            time.sleep(0.1)
            keyboard.press_and_release('ctrl+minus')
            time.sleep(0.1)
            keyboard.press_and_release('enter')  # Confirm delete
            
            print("[Undo] Deleted last Excel entry")
            
            # Switch back to scanner
            time.sleep(0.3)
            scanner_windows = [w for w in gw.getAllWindows() if 'Barcode Scanner' in w.title]
            if scanner_windows:
                scanner_windows[0].activate()
            
            self.__undo_btn.setEnabled(False)
            self.__last_excel_data = None
            
        except Exception as e:
            print(f"[Undo] Error: {e}")
    
    def _continue_scan(self):
        self.__frozen = False
        self.__continue_btn.setEnabled(False)
        self.__scanned_items.clear()
        self.__last_seen.clear()
        self.__scan_list.clear()
        need = int(self.__config.expected_qr_count) if self.__config.expected_qr_count else 1
        self._update_status(0, need)
    
    def _reset_scan(self):
        self.__frozen = False
        self.__continue_btn.setEnabled(False)
        self.__scanned_items.clear()
        self.__last_seen.clear()
        self.__scan_list.clear()
        need = int(self.__config.expected_qr_count) if self.__config.expected_qr_count else 1
        self._update_status(0, need)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.__continue_btn.isEnabled():
                self._continue_scan()
        elif event.key() == Qt.Key_U:
            if self.__undo_btn.isEnabled():
                self._undo_excel()
        elif event.key() == Qt.Key_T:
            self._toggle_theme()
    
    def closeEvent(self, event):
        if self.__camera_thread:
            self.__camera_thread.stop()
            self.__camera_thread.wait()
        event.accept()

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

        # Show completion message when all codes scanned
        scanned_count = len(scanned_items)
        if scanned_count >= need:
            cv2.putText(frame, "AUTO-ENTERING TO EXCEL...", (10, frame.shape[0] - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return frame

    def _process_frame(self, frame):
        if self.__frozen:
            return
            
        self.__current_frame = frame.copy()
        self.__frame_count += 1
        
        need = int(self.__config.expected_qr_count) if self.__config.expected_qr_count else 1
        
        detections = self._detect(frame)
        
        # Sort detections
        scan_direction = self.__config.scan_direction
        if scan_direction and scan_direction != 'any' and len(detections) >= need:
            sorted_detections = ScanSorter.sort(detections, scan_direction)
        else:
            sorted_detections = detections
        
        # Store sorted detections for freeze frame
        self.__last_sorted_detections = sorted_detections
        
        # Register scans
        if len(detections) >= need:
            for text, box in sorted_detections:
                try:
                    name, value = self.__parse.parse(text)
                except Exception:
                    name, value = None, text
                
                raw_text = text if isinstance(text, str) else str(text)
                
                if raw_text in self.__last_seen and (self.__frame_count - self.__last_seen[raw_text]) < self.__cooldown_frames:
                    continue
                
                if not any(item.get('text') == raw_text for item in self.__scanned_items):
                    self.__scanned_items.append({'name': name, 'value': value, 'text': raw_text})
                    self.__last_seen[raw_text] = self.__frame_count
                    self._update_scan_list()
        
        # Draw overlays
        frame = self._draw_overlays(frame, sorted_detections, self.__scanned_items, need)
        
        # Update display
        self._update_status(len(self.__scanned_items), need)
        self._display_frame(frame)
        
        # Auto-enter when complete
        if len(self.__scanned_items) >= need:
            self._auto_enter()

    def start(self):
        print(f"=== Advanced Scanner - {self.__workstation_id} ===")
        print(f"Expected QR count: {self.__config.expected_qr_count}")
        print(f"Scan direction: {self.__config.scan_direction}")
        print(f"Append key: {self.__config.append_key}")
        print("\nFormat barcodes as: field_name:value")
        print("Data will auto-enter to Excel, then freeze for confirmation")
        print("Press 'r' to reset, 'q' to quit\n")
        self.show()

def main():
    app = QApplication(sys.argv)
    camera = Camera("workstation_11")
    camera.start()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
