#!/usr/bin/env python3
"""Simulation environment for testing barcode scanning without live camera."""

from pathlib import Path
import sys
import cv2
import numpy as np
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aibi_cv.vision_system import VisionSystem


def generate_test_qr_image(data: str, size: int = 300) -> np.ndarray:
    """Generate a test QR code image."""
    # Create white background
    img = np.ones((size, size, 3), dtype=np.uint8) * 255
    
    # Generate QR code
    qr_encoder = cv2.QRCodeEncoder.create()
    qr_code = qr_encoder.encode(data)
    
    # Resize and place in center
    qr_size = size - 40
    qr_resized = cv2.resize(qr_code, (qr_size, qr_size), interpolation=cv2.INTER_NEAREST)
    
    # Convert to 3-channel
    if len(qr_resized.shape) == 2:
        qr_resized = cv2.cvtColor(qr_resized, cv2.COLOR_GRAY2BGR)
    
    # Place in center
    y_offset = (size - qr_size) // 2
    x_offset = (size - qr_size) // 2
    img[y_offset:y_offset+qr_size, x_offset:x_offset+qr_size] = qr_resized
    
    return img


def create_multi_qr_image(qr_data: list, layout: tuple = (1, 3)) -> np.ndarray:
    """Create an image with multiple QR codes."""
    rows, cols = layout
    qr_size = 300
    margin = 20
    
    # Calculate canvas size
    canvas_width = cols * qr_size + (cols + 1) * margin
    canvas_height = rows * qr_size + (rows + 1) * margin
    
    # Create canvas
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 200
    
    # Place QR codes
    for idx, data in enumerate(qr_data[:rows * cols]):
        row = idx // cols
        col = idx % cols
        
        # Generate QR code
        qr_img = generate_test_qr_image(data, qr_size)
        
        # Calculate position
        y = margin + row * (qr_size + margin)
        x = margin + col * (qr_size + margin)
        
        # Place on canvas
        canvas[y:y+qr_size, x:x+qr_size] = qr_img
    
    return canvas


def run_simulation():
    """Run simulation test with synthetic QR codes."""
    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    config_dir = project_root / "data" / "config"
    db_path = project_root / "data" / "simulation.db"
    
    # Initialize vision system
    workstation_id = "simulation_workstation"
    system = VisionSystem(
        workstation_id=workstation_id,
        config_dir=config_dir,
        db_path=db_path,
        camera_index=0
    )
    
    print("=== Barcode Scanning Simulation ===\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Complete Part Scan",
            "qr_data": ["PN-12345", "SN-67890", "BATCH-2024-01"]
        },
        {
            "name": "Missing Optional Field",
            "qr_data": ["PN-54321", "SN-09876"]
        },
        {
            "name": "Single QR Code",
            "qr_data": ["PN-99999"]
        },
        {
            "name": "Multiple Parts",
            "qr_data": ["PN-AAA", "SN-BBB", "BATCH-CCC", "PN-DDD"]
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- Test: {scenario['name']} ---")
        
        # Generate test image
        test_image = create_multi_qr_image(scenario['qr_data'])
        
        # Process image
        detections, payload = system.process_frame(test_image)
        
        # Display results
        print(f"Detections: {len(detections)}")
        for det in detections:
            print(f"  [{det.position_index}] {det.type}: {det.data}")
        
        # Show payload
        print(f"\nPayload:")
        print(f"  Workstation: {payload['workstation_id']}")
        print(f"  Fields: {payload['scan_data']['fields']}")
        print(f"  Complete: {payload['metadata']['required_fields_complete']}")
        
        # Store scan
        event_id = system.store_scan(payload)
        print(f"  Stored as event ID: {event_id}")
        
        # Display image
        display_img = system.scanner.draw_detections(test_image, detections)
        cv2.imshow(f"Simulation - {scenario['name']}", display_img)
        cv2.waitKey(2000)  # Show for 2 seconds
    
    cv2.destroyAllWindows()
    
    # Print final statistics
    print("\n=== Simulation Complete ===")
    stats = system.get_stats()
    print(f"Total scans: {stats['total_scans']}")
    print(f"Successful: {stats['successful_scans']}")
    print(f"Failed: {stats['failed_scans']}")
    print(f"Success rate: {stats['success_rate']:.1%}")
    
    # Show unsynced events
    unsynced = system.storage.get_unsynced_events()
    print(f"\nUnsynced events: {len(unsynced)}")


if __name__ == "__main__":
    run_simulation()
