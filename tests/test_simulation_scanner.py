"""Simulation-style tests built on current scanner modules."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import numpy as np

from aibi_cv.DecodeQr import DecodeQr
from aibi_cv.config_manager import ConfigManager, WorkstationConfig
from aibi_cv.parse import Parse


class TestSimulationScenarios:
    def setup_method(self):
        self.temp_dir = TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / "config"

        self.config_manager = ConfigManager(self.config_dir)
        self.config = WorkstationConfig("test_ws", expected_qr_count=2)
        self.config_manager.save_config(self.config)

    def teardown_method(self):
        self.temp_dir.cleanup()

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_synthetic_frame_decode_pipeline(self, mock_detector_class):
        """A synthetic frame should produce detections when detector returns codes."""
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        mock_detector.detectAndDecodeMulti.return_value = (
            True,
            ["part_number:PN-12345", "serial_number:SN-67890"],
            np.array(
                [
                    [[10, 10], [50, 10], [50, 50], [10, 50]],
                    [[60, 60], [100, 60], [100, 100], [60, 100]],
                ],
                dtype=float,
            ),
            None,
        )

        img = np.ones((140, 140, 3), dtype=np.uint8) * 255
        detections = DecodeQr.multi_opencv(img)

        assert len(detections) == 2
        parsed = dict(Parse.parse(text) for text, _ in detections)
        assert parsed["part_number"] == "PN-12345"
        assert parsed["serial_number"] == "SN-67890"

    def test_expected_qr_count_gate(self):
        """Simulation acceptance can use expected_qr_count from workstation config."""
        scanned_payloads = ["part_number:PN-1", "serial_number:SN-1"]
        parsed = [Parse.parse(item) for item in scanned_payloads]
        found_count = len([p for p in parsed if p[0] is not None])

        assert self.config.expected_qr_count == 2
        assert found_count >= self.config.expected_qr_count

    def test_missing_count_blocks_completion(self):
        """When less than expected QR codes are detected, workflow is incomplete."""
        scanned_payloads = ["part_number:PN-1"]
        parsed = [Parse.parse(item) for item in scanned_payloads]
        found_count = len([p for p in parsed if p[0] is not None])

        assert self.config.expected_qr_count == 2
        assert found_count < self.config.expected_qr_count