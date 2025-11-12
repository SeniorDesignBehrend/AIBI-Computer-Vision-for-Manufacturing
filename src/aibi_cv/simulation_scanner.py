#!/usr/bin/env python3
"""Simulation scanner - generates synthetic QR codes for testing."""

import cv2
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Set

from .config_manager import ConfigManager


def generate_qr_image(data: str, size: int = 300) -> np.ndarray:
    """Generate a QR code image."""
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    qr_encoder = cv2.QRCodeEncoder.create()
    qr_code = qr_encoder.encode(data)
    qr_size = size - 40
    qr_resized = cv2.resize(qr_code, (qr_size, qr_size), interpolation=cv2.INTER_NEAREST)
    if len(qr_resized.shape) == 2:
        qr_resized = cv2.cvtColor(qr_resized, cv2.COLOR_GRAY2BGR)
    y_offset = (size - qr_size) // 2
    x_offset = (size - qr_size) // 2
    img[y_offset:y_offset+qr_size, x_offset:x_offset+qr_size] = qr_resized
    return img


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
    
    # Build required fields set
    required_fields: Set[str] = {f.name for f in config.barcode_fields if f.required}
    optional_fields: Set[str] = {f.name for f in config.barcode_fields if not f.required}
    all_fields = required_fields | optional_fields
    
    print(f"=== Simulation Scanner - {workstation_id} ===\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Complete Scan",
            "codes": ["part_number:PN-12345", "serial_number:SN-67890", "batch_id:BATCH-2024-01"]
        },
        {
            "name": "Minimal Required",
            "codes": ["part_number:PN-99999", "serial_number:SN-11111"]
        },
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- Test: {scenario['name']} ---")
        scanned_data: Dict[str, str] = {}
        
        for code_text in scenario['codes']:
            # Generate QR code
            qr_img = generate_qr_image(code_text)
            
            # Decode it
            detections = decode_qr(qr_img)
            
            for text, _ in detections:
                name, value = parse_barcode(text)
                if name and name in all_fields and name not in scanned_data:
                    scanned_data[name] = value
                    print(f"✓ Scanned: {name} = {value}")
        
        # Check if complete
        missing_required = required_fields - scanned_data.keys()
        
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
            
            output_file = output_dir / f"sim_{workstation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"✓ Saved to {output_file}")
        else:
            print(f"✗ Incomplete - missing: {', '.join(missing_required)}")
    
    print("\n=== Simulation Complete ===")


if __name__ == "__main__":
    main()
