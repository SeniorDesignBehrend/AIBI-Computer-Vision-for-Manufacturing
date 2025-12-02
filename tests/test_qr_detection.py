"""Basic QR detection tests - see test_comprehensive.py for SFR compliance tests."""

import cv2
import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from aibi_cv.advanced_scanner import decode_qr


class TestBasicQRDetection:
    """Basic QR detection functionality tests."""
    
    def test_empty_image_returns_empty_list(self):
        """Test QR detection on empty image returns empty list."""
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        results = decode_qr(img)
        assert results == []

    @patch('aibi_cv.advanced_scanner.cv2.QRCodeDetector')
    def test_exception_handling_returns_empty_list(self, mock_detector_class):
        """Test that exceptions are handled gracefully."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        
        # Mock all methods to raise exceptions
        mock_detector.detectAndDecodeMulti.side_effect = Exception("Detection failed")
        mock_detector.detectAndDecode.side_effect = Exception("Single detection failed")
        
        img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        results = decode_qr(img)
        
        assert results == []