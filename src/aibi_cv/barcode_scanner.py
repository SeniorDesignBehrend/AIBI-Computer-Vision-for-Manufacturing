"""Barcode and QR code detection and decoding module."""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime
import json


@dataclass
class BarcodeDetection:
    """Represents a detected barcode or QR code."""
    data: str
    type: str
    bbox: np.ndarray
    confidence: float
    position_index: int
    timestamp: str


class BarcodeScanner:
    """Handles detection and decoding of barcodes and QR codes."""
    
    def __init__(self, workstation_id: str = "default"):
        self.workstation_id = workstation_id
        self.qr_detector = cv2.QRCodeDetector()
        
    def detect_and_decode(self, frame: np.ndarray) -> List[BarcodeDetection]:
        """Detect and decode all visible barcodes/QR codes in frame."""
        detections = []
        timestamp = datetime.now().isoformat()
        
        # QR code detection
        qr_results = self._detect_qr_codes(frame, timestamp)
        detections.extend(qr_results)
        
        return detections
    
    def _detect_qr_codes(self, frame: np.ndarray, timestamp: str) -> List[BarcodeDetection]:
        """Detect QR codes using OpenCV."""
        results = []
        
        try:
            # Try multi-detection first
            retval, decoded_info, points, _ = self.qr_detector.detectAndDecodeMulti(frame)
            
            if retval and points is not None:
                for idx, (data, bbox) in enumerate(zip(decoded_info, points)):
                    if data:
                        results.append(BarcodeDetection(
                            data=data,
                            type="QR_CODE",
                            bbox=bbox.astype(np.int32),
                            confidence=1.0,
                            position_index=idx,
                            timestamp=timestamp
                        ))
        except Exception:
            # Fallback to single detection
            data, bbox, _ = self.qr_detector.detectAndDecode(frame)
            if data and bbox is not None:
                results.append(BarcodeDetection(
                    data=data,
                    type="QR_CODE",
                    bbox=bbox.astype(np.int32),
                    confidence=1.0,
                    position_index=0,
                    timestamp=timestamp
                ))
        
        return results
    
    def draw_detections(self, frame: np.ndarray, detections: List[BarcodeDetection]) -> np.ndarray:
        """Draw bounding boxes and labels on frame."""
        output = frame.copy()
        
        for detection in detections:
            # Draw bounding box
            cv2.polylines(output, [detection.bbox], True, (0, 255, 0), 2)
            
            # Draw label
            pt = detection.bbox[0].flatten()
            x, y = int(pt[0]), int(pt[1])
            label = f"{detection.type}: {detection.data[:20]}"
            cv2.putText(output, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return output
