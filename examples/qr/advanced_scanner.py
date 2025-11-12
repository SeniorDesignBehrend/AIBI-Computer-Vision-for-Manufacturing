#!/usr/bin/env python3
"""Advanced QR/Barcode scanner using the full vision system."""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aibi_cv.vision_system import VisionSystem


def main():
    # Setup paths
    project_root = Path(__file__).parent.parent.parent
    config_dir = project_root / "data" / "config"
    db_path = project_root / "data" / "scans.db"
    
    # Initialize vision system
    workstation_id = "workstation_01"
    system = VisionSystem(
        workstation_id=workstation_id,
        config_dir=config_dir,
        db_path=db_path,
        camera_index=0
    )
    
    # Define callback for processing detections
    def on_detection(detections, payload):
        if payload["metadata"]["required_fields_complete"]:
            print(f"\n✓ Complete scan detected:")
            for field, value in payload["scan_data"]["fields"].items():
                print(f"  {field}: {value}")
    
    # Run live scanning
    print(f"Starting vision system for {workstation_id}")
    print("Controls:")
    print("  - Press 's' to save current scan")
    print("  - Press 'q' to quit")
    
    system.run_live(display=True, callback=on_detection)
    
    # Print final stats
    stats = system.get_stats()
    print("\n=== Session Statistics ===")
    print(f"Total scans: {stats['total_scans']}")
    print(f"Successful: {stats['successful_scans']}")
    print(f"Failed: {stats['failed_scans']}")
    print(f"Success rate: {stats['success_rate']:.1%}")


if __name__ == "__main__":
    main()
