#!/usr/bin/env python3
"""Simple QR/Barcode scanner that outputs to JSON file."""

import cv2
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

def decode_qr(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Decode QR codes using OpenCV."""
    detector = cv2.QRCodeDetector()
    try:
        result = detector.detectAndDecodeMulti(img)
        if len(result) == 3:
            texts, points, _ = result
        else:
            texts, points = result
        results = []
        if points is not None:
            for i, text in enumerate(texts):
                if text:
                    box = points[i].astype(np.int32)
                    results.append((text, box))
        return results
    except:
        # Fallback to single detection
        result = detector.detectAndDecode(img)
        if len(result) == 3:
            text, pts, _ = result
        else:
            text, pts = result
        if text and pts is not None:
            return [(text, pts.astype(np.int32))]
        return []

def draw_detections(img: np.ndarray, detections: List[Tuple[str, np.ndarray]]) -> np.ndarray:
    """Draw bounding boxes and text on image."""
    for text, box in detections:
        cv2.polylines(img, [box], True, (0, 255, 0), 2)
        pt = box[0].flatten()
        x, y = int(pt[0]), int(pt[1])
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "qr_scans.json"
    
    scans = []
    seen_codes = set()
    
    print("Press 's' to save and quit, 'q' to quit without saving")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = decode_qr(frame)
        
        for text, box in detections:
            if text not in seen_codes:
                scan_data = {
                    "timestamp": datetime.now().isoformat(),
                    "data": text,
                    "type": "QR_CODE"
                }
                scans.append(scan_data)
                seen_codes.add(text)
                print(f"Detected: {text}")
        
        frame = draw_detections(frame, detections)
        cv2.imshow('QR Scanner - Press S to save', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            with open(output_file, 'w') as f:
                json.dump(scans, f, indent=2)
            print(f"Saved {len(scans)} scans to {output_file}")
            break
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()