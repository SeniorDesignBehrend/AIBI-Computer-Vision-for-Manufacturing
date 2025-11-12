#!/usr/bin/env python3
"""Simple QR/Barcode scanner using pyzbar."""

import cv2
import numpy as np
from pyzbar import pyzbar
from typing import List, Tuple

def decode_codes(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Decode QR codes and barcodes using pyzbar."""
    results = []
    for code in pyzbar.decode(img):
        text = code.data.decode('utf-8')
        points = np.array([(p.x, p.y) for p in code.polygon], dtype=np.int32)
        results.append((text, points))
    return results

def draw_detections(img: np.ndarray, detections: List[Tuple[str, np.ndarray]]) -> np.ndarray:
    """Draw bounding boxes and text on image."""
    for text, points in detections:
        cv2.polylines(img, [points], True, (0, 255, 0), 2)
        x, y = int(points[0][0]), int(points[0][1])
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
            
        detections = decode_codes(frame)
        frame = draw_detections(frame, detections)
        
        cv2.imshow('Pyzbar Scanner', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()