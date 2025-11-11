#!/usr/bin/env python3
"""Simple QR/Barcode scanner using main camera."""

import cv2
import numpy as np
from typing import List, Tuple

def decode_qr(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Decode QR codes using OpenCV."""
    detector = cv2.QRCodeDetector()
    try:
        texts, points, _ = detector.detectAndDecodeMulti(img)
        results = []
        if points is not None:
            for i, text in enumerate(texts):
                if text:
                    box = points[i].astype(np.int32)
                    results.append((text, box))
        return results
    except:
        # Fallback to single detection
        text, pts, _ = detector.detectAndDecode(img)
        if text and pts is not None:
            return [(text, pts.astype(np.int32))]
        return []

def draw_detections(img: np.ndarray, detections: List[Tuple[str, np.ndarray]]) -> np.ndarray:
    """Draw bounding boxes and text on image."""
    for text, box in detections:
        cv2.polylines(img, [box], True, (0, 255, 0), 2)
        x, y = int(box[0][0]), int(box[0][1])
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = decode_qr(frame)
        frame = draw_detections(frame, detections)
        
        cv2.imshow('QR/Barcode Scanner', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()