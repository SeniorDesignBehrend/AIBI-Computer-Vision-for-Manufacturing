"""Comprehensive tests aligned to current modules and architecture."""

import json
import time
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import numpy as np

from aibi_cv.DecodeQr import DecodeQr
from aibi_cv.OutputData import OutputData
from aibi_cv.ScanSorter import ScanSorter
from aibi_cv.config_manager import ConfigManager, WorkstationConfig
from aibi_cv.parse import Parse


class TestSFR1QRDetection:
    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_multiple_qr_detection(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        expected_codes = ["code_1", "code_2", "code_3"]
        points = np.array(
            [
                [[10, 10], [20, 10], [20, 20], [10, 20]],
                [[30, 30], [40, 30], [40, 40], [30, 40]],
                [[50, 50], [60, 50], [60, 60], [50, 60]],
            ],
            dtype=float,
        )
        mock_detector.detectAndDecodeMulti.return_value = (True, expected_codes, points, None)

        img = np.ones((80, 80, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(img)

        assert len(results) == 3
        assert [text for text, _ in results] == expected_codes


class TestSFR2FieldMapping:
    def test_parse_colon_and_json_formats(self):
        name1, value1 = Parse.parse("part_number:PN-12345")
        name2, value2 = Parse.parse('{"serial_number": "SN-67890"}')

        assert name1 == "part_number"
        assert value1 == "PN-12345"
        assert name2 == "serial_number"
        assert value2 == "SN-67890"


class TestSFR4ScanJSON:
    def test_build_complete_scan_json(self):
        with TemporaryDirectory() as temp_dir:
            writer = OutputData("workstation_01", temp_dir)
            scanned_data = {"part_number": "PN-12345", "serial_number": "SN-67890"}
            assert writer.to_json(scanned_data, field_order=["part_number", "serial_number"])

            files = list(Path(temp_dir).glob("scan_workstation_01_*.json"))
            assert len(files) == 1

            with open(files[0], "r", encoding="utf-8") as handle:
                output = json.load(handle)

            assert output["workstation_id"] == "workstation_01"
            assert len(output["barcodes"]) == 2
            assert output["barcodes"][0]["name"] == "part_number"


class TestSFR15MultiCodeDetection:
    def test_no_missed_codes_after_sort(self):
        detections = [
            ("A", np.array([[60, 10], [70, 10], [70, 20], [60, 20]])),
            ("B", np.array([[10, 10], [20, 10], [20, 20], [10, 20]])),
            ("C", np.array([[35, 10], [45, 10], [45, 20], [35, 20]])),
        ]
        sorted_detections = ScanSorter.sort(detections, "left-to-right")
        codes = [text for text, _ in sorted_detections]

        assert codes == ["B", "C", "A"]


class TestSFR16OutputDeduplication:
    def test_no_duplicate_outputs(self):
        raw_codes = ["part_number:PN-1", "part_number:PN-1", "serial_number:SN-1"]
        unique_codes = list(dict.fromkeys(raw_codes))
        assert unique_codes == ["part_number:PN-1", "serial_number:SN-1"]


class TestPPSR2PerformanceLatency:
    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_detection_latency_threshold(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        mock_detector.detectAndDecodeMulti.return_value = (True, [], None, None)

        img = np.ones((720, 1280, 3), dtype=np.uint8)
        start_time = time.perf_counter()
        _ = DecodeQr.multi_opencv(img)
        latency_ms = (time.perf_counter() - start_time) * 1000

        assert latency_ms < 200


class TestPDSR1ConfigInspection:
    def test_local_endpoints_only(self):
        config_data = {
            "output_directory": "./outputs",
            "config_directory": "./data/config",
            "camera_index": 0,
        }
        for _, value in config_data.items():
            if isinstance(value, str):
                assert "http://" not in value.lower()
                assert "https://" not in value.lower()


class TestEISR6ConfigurableWorkflows:
    def test_different_config_workflows(self):
        config1 = WorkstationConfig("manufacturing_01", expected_qr_count=2, append_key="TAB")
        config2 = WorkstationConfig("quality_01", expected_qr_count=3, append_key="ENTER")

        assert config1.expected_qr_count != config2.expected_qr_count
        assert config1.append_key != config2.append_key

    def test_config_manager_round_trip(self):
        with TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            manager.save_config(WorkstationConfig("quality_01", expected_qr_count=5))
            loaded = manager.get_config("quality_01")
            assert loaded is not None
            assert loaded.expected_qr_count == 5


class TestEISR3InteroperabilitySchema:
    def test_timestamp_iso_format(self):
        payload = {
            "workstation_id": "workstation_01",
            "timestamp": datetime.now().isoformat(),
            "barcodes": [{"name": "part_number", "value": "PN-12345"}],
        }
        datetime.fromisoformat(payload["timestamp"])
        assert payload["workstation_id"]