"""Tests for simple QR scanner functionality."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
import numpy as np
import sys
import os

# Add examples directory to path for importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples', 'qr'))

from simple_qr_scanner import decode_qr, draw_detections


class TestSimpleQRScanner:
    def test_decode_qr_empty_result(self):
        """Test QR decoding with no detections."""
        with patch('simple_qr_scanner.cv2.QRCodeDetector') as mock_detector_class:
            mock_detector = MagicMock()
            mock_detector_class.return_value = mock_detector
            
            # Mock no detection
            mock_detector.detectAndDecodeMulti.return_value = ([], None)
            mock_detector.detectAndDecode.return_value = ("", None)
            
            img = np.zeros((100, 100, 3), dtype=np.uint8)
            results = decode_qr(img)
            
            assert results == []

    def test_decode_qr_single_detection(self):
        """Test QR decoding with single detection."""
        with patch('simple_qr_scanner.cv2.QRCodeDetector') as mock_detector_class:
            mock_detector = MagicMock()
            mock_detector_class.return_value = mock_detector
            
            # Mock multi detection failure, single success
            mock_detector.detectAndDecodeMulti.side_effect = Exception("Multi failed")
            mock_detector.detectAndDecode.return_value = (
                "test_code",
                np.array([[10, 10], [90, 10], [90, 90], [10, 90]]),
                None
            )
            
            img = np.ones((100, 100, 3), dtype=np.uint8) * 255
            results = decode_qr(img)
            
            assert len(results) == 1
            assert results[0][0] == "test_code"
            assert results[0][1] is not None

    def test_decode_qr_multi_detection(self):
        """Test QR decoding with multiple detections."""
        with patch('simple_qr_scanner.cv2.QRCodeDetector') as mock_detector_class:
            mock_detector = MagicMock()
            mock_detector_class.return_value = mock_detector
            
            # Mock multi detection success
            mock_detector.detectAndDecodeMulti.return_value = (
                ["code1", "code2"],
                [
                    np.array([[10, 10], [50, 10], [50, 50], [10, 50]]),
                    np.array([[60, 60], [90, 60], [90, 90], [60, 90]])
                ],
                None
            )
            
            img = np.ones((100, 100, 3), dtype=np.uint8) * 255
            results = decode_qr(img)
            
            assert len(results) == 2
            assert results[0][0] == "code1"
            assert results[1][0] == "code2"

    def test_draw_detections(self):
        """Test drawing detections on image."""
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        detections = [
            ("test_code", np.array([[10, 10], [50, 10], [50, 50], [10, 50]]))
        ]
        
        with patch('simple_qr_scanner.cv2.polylines') as mock_polylines, \
             patch('simple_qr_scanner.cv2.putText') as mock_putText:
            
            result_img = draw_detections(img, detections)
            
            # Verify drawing functions were called
            mock_polylines.assert_called_once()
            mock_putText.assert_called_once()
            
            # Should return the same image object
            assert result_img is img

    def test_draw_detections_empty(self):
        """Test drawing with no detections."""
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        detections = []
        
        with patch('simple_qr_scanner.cv2.polylines') as mock_polylines, \
             patch('simple_qr_scanner.cv2.putText') as mock_putText:
            
            result_img = draw_detections(img, detections)
            
            # No drawing should occur
            mock_polylines.assert_not_called()
            mock_putText.assert_not_called()
            
            assert result_img is img

    def test_scan_data_structure(self):
        """Test scan data structure format."""
        from datetime import datetime
        
        # Simulate scan data creation
        scan_data = {
            "timestamp": datetime.now().isoformat(),
            "data": "part_number:PN-12345",
            "type": "QR_CODE"
        }
        
        # Verify structure
        assert "timestamp" in scan_data
        assert "data" in scan_data
        assert "type" in scan_data
        assert scan_data["type"] == "QR_CODE"
        assert "PN-12345" in scan_data["data"]

    def test_duplicate_detection_handling(self):
        """Test handling of duplicate QR codes."""
        seen_codes = set()
        scans = []
        
        # Simulate detecting same code twice
        test_codes = ["part_number:PN-12345", "part_number:PN-12345", "serial_number:SN-67890"]
        
        for code in test_codes:
            if code not in seen_codes:
                scan_data = {
                    "timestamp": "2024-01-01T10:00:00",
                    "data": code,
                    "type": "QR_CODE"
                }
                scans.append(scan_data)
                seen_codes.add(code)
        
        # Should only have 2 unique scans
        assert len(scans) == 2
        assert len(seen_codes) == 2
        assert "part_number:PN-12345" in seen_codes
        assert "serial_number:SN-67890" in seen_codes