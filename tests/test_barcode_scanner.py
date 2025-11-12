"""Tests for barcode scanner module."""

import pytest
import numpy as np
import cv2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aibi_cv.barcode_scanner import BarcodeScanner, BarcodeDetection


def generate_qr_image(data: str, size: int = 300) -> np.ndarray:
    """Generate a test QR code image."""
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


def test_scanner_initialization():
    """Test scanner can be initialized."""
    scanner = BarcodeScanner("test_workstation")
    assert scanner.workstation_id == "test_workstation"


def test_qr_detection():
    """Test QR code detection."""
    scanner = BarcodeScanner("test")
    test_image = generate_qr_image("TEST_DATA_123")
    
    detections = scanner.detect_and_decode(test_image)
    
    assert len(detections) > 0
    assert detections[0].data == "TEST_DATA_123"
    assert detections[0].type == "QR_CODE"


def test_empty_frame():
    """Test detection on empty frame."""
    scanner = BarcodeScanner("test")
    empty_frame = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    detections = scanner.detect_and_decode(empty_frame)
    
    assert len(detections) == 0


def test_draw_detections():
    """Test drawing detections on frame."""
    scanner = BarcodeScanner("test")
    test_image = generate_qr_image("DRAW_TEST")
    
    detections = scanner.detect_and_decode(test_image)
    output = scanner.draw_detections(test_image, detections)
    
    assert output.shape == test_image.shape
    assert not np.array_equal(output, test_image)  # Image should be modified
