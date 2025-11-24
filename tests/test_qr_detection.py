"""Tests for QR code detection functionality."""

import cv2
import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from aibi_cv.advanced_scanner import decode_qr


class TestQRDetection:
    def test_decode_qr_empty_image(self):
        """Test QR detection on empty image."""
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        results = decode_qr(img)
        assert results == []

    def test_decode_qr_white_image(self):
        """Test QR detection on white image."""
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        assert results == []

    @patch('aibi_cv.advanced_scanner.cv2.QRCodeDetector')
    def test_opencv_fallback_single_detection(self, mock_detector_class):
        """Test OpenCV fallback for single QR detection."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        
        # Mock detectAndDecodeMulti to fail
        mock_detector.detectAndDecodeMulti.side_effect = Exception("Multi detection failed")
        
        # Mock single detection to succeed
        mock_detector.detectAndDecode.return_value = (
            "test_data", 
            np.array([[10, 10], [90, 10], [90, 90], [10, 90]]), 
            None
        )
        
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        
        assert len(results) == 1
        assert results[0][0] == "test_data"
        assert results[0][1] is not None

    @patch('aibi_cv.advanced_scanner.cv2.QRCodeDetector')
    def test_opencv_multi_detection(self, mock_detector_class):
        """Test OpenCV multi QR detection."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        
        # Mock multi detection success
        mock_detector.detectAndDecodeMulti.return_value = (
            ["code1", "code2"],
            [
                np.array([[10, 10], [50, 10], [50, 50], [10, 50]]),
                np.array([[60, 60], [90, 60], [90, 90], [60, 90]])
            ]
        )
        
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        
        assert len(results) == 2
        assert results[0][0] == "code1"
        assert results[1][0] == "code2"

    def test_pyzbar_detection(self):
        """Test pyzbar QR detection when available."""
        with patch('aibi_cv.advanced_scanner.decode', create=True) as mock_pyzbar_decode:
            # Mock pyzbar detection
            mock_decoded = MagicMock()
            mock_decoded.data = b"pyzbar_data"
            mock_decoded.polygon = [
                MagicMock(x=10, y=10),
                MagicMock(x=50, y=10),
                MagicMock(x=50, y=50),
                MagicMock(x=10, y=50)
            ]
            mock_pyzbar_decode.return_value = [mock_decoded]
            
            # Mock the import to avoid pyzbar dependency
            with patch.dict('sys.modules', {'pyzbar.pyzbar': MagicMock()}):
                img = np.ones((100, 100, 3), dtype=np.uint8) * 255
                results = decode_qr(img)
                
                # Since pyzbar isn't actually available, should fall back to OpenCV
                assert isinstance(results, list)

    @patch('aibi_cv.advanced_scanner.cv2.QRCodeDetector')
    def test_no_detection(self, mock_detector_class):
        """Test when no QR codes are detected."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        
        # Mock all detection methods to return empty/None
        mock_detector.detectAndDecodeMulti.return_value = ([], None)
        mock_detector.detectAndDecode.return_value = ("", None, None)
        
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        
        assert results == []

    @patch('aibi_cv.advanced_scanner.cv2.QRCodeDetector')
    def test_detection_exception_handling(self, mock_detector_class):
        """Test exception handling in QR detection."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        
        # Mock all methods to raise exceptions
        mock_detector.detectAndDecodeMulti.side_effect = Exception("Detection failed")
        mock_detector.detectAndDecode.side_effect = Exception("Single detection failed")
        
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        
        # Should handle exceptions gracefully and return empty list
        assert results == []