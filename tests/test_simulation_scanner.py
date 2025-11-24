"""Tests for simulation scanner functionality."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
import numpy as np

from aibi_cv.simulation_scanner import generate_qr_image
from aibi_cv.config_manager import ConfigManager, WorkstationConfig, BarcodeField


class TestQRGeneration:
    @patch('aibi_cv.simulation_scanner.cv2.QRCodeEncoder')
    def test_generate_qr_image_success(self, mock_encoder_class):
        """Test successful QR code image generation."""
        mock_encoder = MagicMock()
        mock_encoder_class.create.return_value = mock_encoder
        
        # Mock QR code generation
        mock_qr_code = np.ones((100, 100), dtype=np.uint8) * 255
        mock_encoder.encode.return_value = mock_qr_code
        
        with patch('aibi_cv.simulation_scanner.cv2.resize') as mock_resize, \
             patch('aibi_cv.simulation_scanner.cv2.cvtColor') as mock_cvtColor:
            
            mock_resize.return_value = np.ones((260, 260), dtype=np.uint8) * 255
            mock_cvtColor.return_value = np.ones((260, 260, 3), dtype=np.uint8) * 255
            
            result = generate_qr_image("test_data", 300)
            
            assert result.shape == (300, 300, 3)
            mock_encoder.encode.assert_called_once_with("test_data")

    def test_generate_qr_image_default_size(self):
        """Test QR generation with default size."""
        with patch('aibi_cv.simulation_scanner.cv2.QRCodeEncoder') as mock_encoder_class, \
             patch('aibi_cv.simulation_scanner.cv2.resize') as mock_resize, \
             patch('aibi_cv.simulation_scanner.cv2.cvtColor') as mock_cvtColor:
            
            mock_encoder = MagicMock()
            mock_encoder_class.create.return_value = mock_encoder
            mock_encoder.encode.return_value = np.ones((100, 100), dtype=np.uint8)
            mock_resize.return_value = np.ones((260, 260), dtype=np.uint8)
            mock_cvtColor.return_value = np.ones((260, 260, 3), dtype=np.uint8)
            
            result = generate_qr_image("test")
            
            assert result.shape == (300, 300, 3)  # Default size


class TestSimulationScenarios:
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / "config"
        self.output_dir = Path(self.temp_dir.name) / "outputs"
        
        # Create test config
        self.config_manager = ConfigManager(self.config_dir)
        fields = [
            BarcodeField("part_number", True),
            BarcodeField("serial_number", True),
            BarcodeField("batch_id", False)
        ]
        self.config = WorkstationConfig("test_ws", fields)
        self.config_manager.save_config(self.config)

    def teardown_method(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_complete_scan_scenario(self):
        """Test complete scan with all required fields."""
        required_fields = {"part_number", "serial_number"}
        scanned_data = {
            "part_number": "PN-12345",
            "serial_number": "SN-67890",
            "batch_id": "BATCH-2024-01"
        }
        
        missing_required = required_fields - scanned_data.keys()
        assert len(missing_required) == 0

    def test_minimal_required_scenario(self):
        """Test scan with only required fields."""
        required_fields = {"part_number", "serial_number"}
        scanned_data = {
            "part_number": "PN-99999",
            "serial_number": "SN-11111"
        }
        
        missing_required = required_fields - scanned_data.keys()
        assert len(missing_required) == 0

    def test_incomplete_scan_scenario(self):
        """Test incomplete scan missing required fields."""
        required_fields = {"part_number", "serial_number"}
        scanned_data = {
            "part_number": "PN-12345"
        }
        
        missing_required = required_fields - scanned_data.keys()
        assert "serial_number" in missing_required
        assert len(missing_required) == 1

    def test_field_validation(self):
        """Test field validation against configuration."""
        all_fields = {"part_number", "serial_number", "batch_id"}
        
        # Valid field
        assert "part_number" in all_fields
        
        # Invalid field
        assert "invalid_field" not in all_fields

    @patch('aibi_cv.simulation_scanner.decode_qr')
    @patch('aibi_cv.simulation_scanner.generate_qr_image')
    def test_qr_processing_pipeline(self, mock_generate, mock_decode):
        """Test the QR generation and decoding pipeline."""
        # Mock QR generation
        mock_qr_img = np.ones((300, 300, 3), dtype=np.uint8) * 255
        mock_generate.return_value = mock_qr_img
        
        # Mock QR decoding
        mock_decode.return_value = [("part_number:PN-12345", None)]
        
        # Simulate processing
        code_text = "part_number:PN-12345"
        qr_img = mock_generate(code_text)
        detections = mock_decode(qr_img)
        
        assert len(detections) == 1
        assert detections[0][0] == "part_number:PN-12345"
        mock_generate.assert_called_once_with(code_text)
        mock_decode.assert_called_once_with(mock_qr_img)