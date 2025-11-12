#!/usr/bin/env python3
"""Advanced QR/Barcode scanner with dynamic barcode tracking."""

import cv2
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Set

from .config_manager import ConfigManager


def decode_qr(img):
    """Decode QR codes using OpenCV."""
    detector = cv2.QRCodeDetector()
    try:
        result = detector.detectAndDecodeMulti(img)
        if len(result) >= 2:
            texts, points = result[0], result[1]
        else:
            return []
        results = []
        if points is not None:
            for i, text in enumerate(texts):
                if text:
                    results.append((text, points[i]))
        return results
    except:
        result = detector.detectAndDecode(img)
        if len(result) >= 2 and result[0]:
            return [(result[0], result[1])]
        return []


def parse_barcode(data: str) -> tuple:
    """Parse barcode data to extract name and value."""
    if ":" in data:
        parts = data.split(":", 1)
        return parts[0].strip(), parts[1].strip()
    return None, data


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
    
    # Build required fields set
    required_fields: Set[str] = {f.name for f in config.barcode_fields if f.required}
    optional_fields: Set[str] = {f.name for f in config.barcode_fields if not f.required}
    all_fields = required_fields | optional_fields
    
    # Tracking
    scanned_data: Dict[str, str] = {}
    
    # Open camera
    cap = cv2.VideoCapture(config.camera_index)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    print(f"=== Advanced Scanner - {workstation_id} ===")
    print(f"Required fields: {', '.join(required_fields)}")
    print(f"Optional fields: {', '.join(optional_fields)}")
    print("\nFormat barcodes as: field_name:value")
    print("Press 's' to save (when all required fields scanned)")
    print("Press 'r' to reset, 'q' to quit\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detect QR codes
        detections = decode_qr(frame)
        
        # Process detections
        for text, box in detections:
            # Debug: show raw text
            print(f"DEBUG: Detected QR code: '{text}'")
            
            name, value = parse_barcode(text)
            print(f"DEBUG: Parsed as name='{name}', value='{value}'")
            
            # Only track barcodes in our field list
            if name and name in all_fields and name not in scanned_data:
                scanned_data[name] = value
                print(f"✓ Scanned: {name} = {value}")
            elif name and name not in all_fields:
                print(f"⚠ Ignored (not in field list): {name}")
            elif name and name in scanned_data:
                print(f"⚠ Already scanned: {name}")
            
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
            status = "✓" if field in scanned_data else "✗"
            color = (0, 255, 0) if field in scanned_data else (0, 0, 255)
            cv2.putText(frame, f"{status} {field}", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            y_pos += 25
        
        if not missing_required:
            cv2.putText(frame, "READY TO SAVE (Press S)", (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow('Advanced Scanner', frame)
        
        # Handle keys
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            scanned_data.clear()
            print("\n--- Reset ---\n")
        elif key == ord('s'):
            if not missing_required:
                # Save to JSON
                output_data = {
                    "workstation_id": workstation_id,
                    "timestamp": datetime.now().isoformat(),
                    "barcodes": [
                        {"name": name, "value": value}
                        for name, value in scanned_data.items()
                    ]
                }
                
                output_file = output_dir / f"scan_{workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(output_file, 'w') as f:
                    json.dump(output_data, f, indent=2)
                
                print(f"\n✓ Saved to {output_file}")
                scanned_data.clear()
                print("--- Ready for next scan ---\n")
            else:
                print(f"\n✗ Cannot save - missing: {', '.join(missing_required)}\n")
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
