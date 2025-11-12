"""Main vision system controller integrating all components."""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Callable
from .barcode_scanner import BarcodeScanner, BarcodeDetection
from .config_manager import ConfigManager, WorkstationConfig
from .data_formatter import DataFormatter
from .data_storage import DataStorage


class VisionSystem:
    """Main controller for the barcode scanning vision system."""
    
    def __init__(
        self,
        workstation_id: str,
        config_dir: Path,
        db_path: Path,
        camera_index: int = 0
    ):
        self.workstation_id = workstation_id
        
        # Initialize components
        self.config_manager = ConfigManager(config_dir)
        self.storage = DataStorage(db_path)
        
        # Get or create workstation config
        self.config = self.config_manager.get_config(workstation_id)
        if not self.config:
            self.config = self.config_manager.create_default_config(workstation_id)
        
        self.scanner = BarcodeScanner(workstation_id)
        self.formatter = DataFormatter(self.config)
        
        # Camera setup
        self.camera_index = camera_index
        self.cap: Optional[cv2.VideoCapture] = None
        
        # Stats
        self.total_scans = 0
        self.successful_scans = 0
        self.failed_scans = 0
    
    def start_camera(self) -> bool:
        """Initialize camera capture."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            self.storage.log_event("ERROR", f"Failed to open camera {self.camera_index}", self.workstation_id)
            return False
        
        self.storage.log_event("INFO", f"Camera {self.camera_index} opened successfully", self.workstation_id)
        return True
    
    def stop_camera(self):
        """Release camera resources."""
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def process_frame(self, frame: np.ndarray) -> tuple[list, dict]:
        """Process a single frame and return detections and payload."""
        # Detect and decode barcodes
        detections = self.scanner.detect_and_decode(frame)
        
        # Format as JSON payload
        payload = self.formatter.format_scan_event(detections)
        
        # Validate payload
        is_valid, errors = self.formatter.validate_payload(payload)
        
        if is_valid:
            self.successful_scans += 1
        else:
            self.failed_scans += 1
            self.storage.log_event("WARNING", f"Invalid scan: {errors}", self.workstation_id)
        
        self.total_scans += 1
        
        return detections, payload
    
    def store_scan(self, payload: dict) -> int:
        """Store scan event to local database."""
        return self.storage.store_scan_event(payload)
    
    def run_live(self, display: bool = True, callback: Optional[Callable] = None):
        """Run live scanning from camera feed."""
        if not self.start_camera():
            return
        
        print(f"Vision System started for workstation: {self.workstation_id}")
        print("Press 'q' to quit, 's' to save current scan")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Process frame
                detections, payload = self.process_frame(frame)
                
                # Draw detections
                if display:
                    display_frame = self.scanner.draw_detections(frame, detections)
                    
                    # Add stats overlay
                    stats_text = f"Scans: {self.total_scans} | Success: {self.successful_scans} | Failed: {self.failed_scans}"
                    cv2.putText(display_frame, stats_text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    cv2.imshow(f'Vision System - {self.workstation_id}', display_frame)
                
                # Call callback if provided
                if callback and detections:
                    callback(detections, payload)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s') and detections:
                    event_id = self.store_scan(payload)
                    print(f"Scan saved with ID: {event_id}")
                    self.storage.log_event("INFO", f"Manual scan saved: {event_id}", self.workstation_id)
        
        finally:
            self.stop_camera()
            if display:
                cv2.destroyAllWindows()
    
    def process_image(self, image_path: Path) -> tuple[list, dict]:
        """Process a single image file."""
        frame = cv2.imread(str(image_path))
        if frame is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        return self.process_frame(frame)
    
    def get_stats(self) -> dict:
        """Get system statistics."""
        return {
            "workstation_id": self.workstation_id,
            "total_scans": self.total_scans,
            "successful_scans": self.successful_scans,
            "failed_scans": self.failed_scans,
            "success_rate": self.successful_scans / self.total_scans if self.total_scans > 0 else 0
        }
