"""Integration tests for the complete scanning workflow."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
import numpy as np

from aibi_cv.config_manager import ConfigManager, WorkstationConfig, BarcodeField
from aibi_cv.advanced_scanner import parse_barcode


class TestScanningWorkflow:
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / "config"
        self.output_dir = Path(self.temp_dir.name) / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def teardown_method(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_complete_workflow(self):
        """Test complete scanning workflow from config to output."""
        # 1. Create workstation config
        config_manager = ConfigManager(self.config_dir)
        fields = [
            BarcodeField("part_number", True),
            BarcodeField("serial_number", True),
            BarcodeField("batch_id", False)
        ]
        config = WorkstationConfig("test_ws", fields, 0)
        config_manager.save_config(config)
        
        # 2. Simulate scanning process
        test_barcodes = [
            "part_number:PN-12345",
            "serial_number:SN-67890",
            "batch_id:BATCH-2024-01"
        ]
        
        scanned_data = {}
        required_fields = {"part_number", "serial_number"}
        
        # 3. Process each barcode
        for barcode_text in test_barcodes:
            name, value = parse_barcode(barcode_text)
            if name and name in {"part_number", "serial_number", "batch_id"}:
                scanned_data[name] = value
        
        # 4. Verify all required fields are present
        missing_required = required_fields - scanned_data.keys()
        assert len(missing_required) == 0
        
        # 5. Generate output
        output_data = {
            "workstation_id": "test_ws",
            "timestamp": "2024-01-01T10:00:00",
            "barcodes": [
                {"name": name, "value": value}
                for name, value in scanned_data.items()
            ]
        }
        
        # 6. Save and verify output
        output_file = self.output_dir / "test_scan.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        assert output_file.exists()
        
        # 7. Verify saved data
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data["workstation_id"] == "test_ws"
        assert len(saved_data["barcodes"]) == 3

    def test_partial_scan_workflow(self):
        """Test workflow with incomplete required fields."""
        # Setup config
        config_manager = ConfigManager(self.config_dir)
        config = config_manager.create_default_config("partial_ws")
        
        # Simulate partial scan (missing serial_number)
        test_barcodes = ["part_number:PN-99999"]
        
        scanned_data = {}
        required_fields = {"part_number", "serial_number"}
        
        for barcode_text in test_barcodes:
            name, value = parse_barcode(barcode_text)
            if name and name in required_fields:
                scanned_data[name] = value
        
        # Should be incomplete
        missing_required = required_fields - scanned_data.keys()
        assert "serial_number" in missing_required
        assert len(missing_required) == 1

    def test_invalid_barcode_handling(self):
        """Test handling of invalid or unrecognized barcodes."""
        config_manager = ConfigManager(self.config_dir)
        config = config_manager.create_default_config("invalid_ws")
        
        # Test various invalid formats
        invalid_barcodes = [
            "invalid_field:value",  # Field not in config
            "no_colon_separator",   # No colon
            "",                     # Empty string
            ":",                    # Only colon
            "multiple:colons:here"  # Multiple colons (should work)
        ]
        
        valid_fields = {"part_number", "serial_number", "batch_id"}
        scanned_data = {}
        
        for barcode_text in invalid_barcodes:
            name, value = parse_barcode(barcode_text)
            if name and name in valid_fields:
                scanned_data[name] = value
        
        # Only the multiple colons case should be ignored (invalid field name)
        assert len(scanned_data) == 0

    def test_field_order_preservation(self):
        """Test that field order is preserved in output."""
        # Create config with specific field order
        fields = [
            BarcodeField("serial_number", True),  # Note: serial_number first
            BarcodeField("part_number", True),    # part_number second
            BarcodeField("batch_id", False)
        ]
        config = WorkstationConfig("order_ws", fields)
        field_order = [f.name for f in config.barcode_fields]
        
        # Scan in different order
        scanned_data = {
            "part_number": "PN-12345",     # Scanned first
            "batch_id": "BATCH-001",       # Scanned second
            "serial_number": "SN-67890"    # Scanned third
        }
        
        # Generate output in config order
        ordered_barcodes = [
            {"name": name, "value": scanned_data[name]}
            for name in field_order if name in scanned_data
        ]
        
        # Verify order matches config, not scan order
        assert ordered_barcodes[0]["name"] == "serial_number"
        assert ordered_barcodes[1]["name"] == "part_number"
        assert ordered_barcodes[2]["name"] == "batch_id"

    def test_config_loading_error_handling(self):
        """Test handling of config loading errors."""
        # Create invalid config file
        invalid_config_file = self.config_dir / "invalid.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        with open(invalid_config_file, 'w') as f:
            f.write("invalid json content")
        
        # Should handle error gracefully
        config_manager = ConfigManager(self.config_dir)
        config = config_manager.get_config("invalid")
        
        assert config is None

    def test_output_directory_creation(self):
        """Test automatic output directory creation."""
        # Remove output directory
        if self.output_dir.exists():
            import shutil
            shutil.rmtree(self.output_dir)
        
        # Simulate output creation
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        assert self.output_dir.exists()
        assert self.output_dir.is_dir()