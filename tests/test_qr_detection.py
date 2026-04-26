"""Basic Data Matrix detection tests for current decoder utilities."""

import numpy as np
from unittest.mock import patch, MagicMock

from aibi_cv.DecodeQr import DecodeQr


class TestBasicQRDetection:
    """Basic Data Matrix detection functionality tests."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_multi_opencv_returns_detections(self, mock_detector_class):
        """detectAndDecodeMulti output is transformed into (text, box) tuples."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector

        points = np.array([[[10, 10], [90, 10], [90, 90], [10, 90]]], dtype=float)
        mock_detector.detectAndDecodeMulti.return_value = (True, ["part_number:PN-1"], points, None)

        img = np.ones((100, 100, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(img)

        assert len(results) == 1
        assert results[0][0] == "part_number:PN-1"
        assert results[0][1] is not None

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_multi_opencv_handles_exceptions(self, mock_detector_class):
        """Decoder should fail safe and return an empty list on exceptions."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        mock_detector.detectAndDecodeMulti.side_effect = RuntimeError("decode failed")

        img = np.zeros((100, 100, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(img)
        assert results == []

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_single_opencv_returns_single_detection(self, mock_detector_class):
        """Single-code fallback returns one tuple when text is present."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        mock_detector.detectAndDecode.return_value = (
            "serial_number:SN-1",
            np.array([[10, 10], [20, 10], [20, 20], [10, 20]], dtype=float),
            None,
        )

        img = np.ones((32, 32, 3), dtype=np.uint8)
        results = DecodeQr.single_opencv(img)

        assert len(results) == 1
        assert results[0][0] == "serial_number:SN-1"