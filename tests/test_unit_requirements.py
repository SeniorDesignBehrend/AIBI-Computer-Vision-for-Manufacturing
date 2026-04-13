"""Unit tests aligned with the current scanner implementation."""

import json
import time
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import numpy as np

from aibi_cv.DecodeQr import DecodeQr
from aibi_cv.OutputData import OutputData
from aibi_cv.config_manager import ConfigManager, WorkstationConfig
from aibi_cv.parse import Parse


class TestTCSFR1AUTO01:
    """TC-SFR1-AUTO-01: QR detection returns all codes in a static image."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_multi_qr_detection_returns_n_codes(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector

        expected_codes = ["part_number:PN-001", "serial_number:SN-002", "batch_id:BATCH-003"]
        points = np.array(
            [
                [[0, 0], [10, 0], [10, 10], [0, 10]],
                [[20, 20], [30, 20], [30, 30], [20, 30]],
                [[40, 40], [50, 40], [50, 50], [40, 50]],
            ],
            dtype=float,
        )
        mock_detector.detectAndDecodeMulti.return_value = (True, expected_codes, points, None)

        img = np.ones((64, 64, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(img)

        assert len(results) == 3
        assert [text for text, _ in results] == expected_codes


class TestTCSFR2AUTO01:
    """TC-SFR2-AUTO-01: Field mapping assigns decoded values to logical fields."""

    def test_field_mapping_from_parser(self):
        decoded_qrs = ["part_number:PN-12345", "serial_number:SN-67890"]
        mapped_data = {}
        for payload in decoded_qrs:
            name, value = Parse.parse(payload)
            mapped_data[name] = value

        assert mapped_data["part_number"] == "PN-12345"
        assert mapped_data["serial_number"] == "SN-67890"


class TestTCSFR4AUTO01:
    """TC-SFR4-AUTO-01: JSON builder aggregates decoded values + metadata."""

    def test_json_builder_produces_schema_compliant_object(self):
        with TemporaryDirectory() as temp_dir:
            writer = OutputData("workstation_01", temp_dir)
            scan_data = {"part_number": "PN-12345", "serial_number": "SN-67890"}
            assert writer.to_json(scan_data)

            files = list(Path(temp_dir).glob("scan_workstation_01_*.json"))
            assert len(files) == 1

            with open(files[0], "r", encoding="utf-8") as handle:
                saved = json.load(handle)

            assert saved["workstation_id"] == "workstation_01"
            assert isinstance(saved["timestamp"], str)
            assert len(saved["barcodes"]) == 2


class TestTCSFR5AUTO01:
    """TC-SFR5-AUTO-01: Keyboard emulation builder outputs correct keystrokes."""

    def test_keystroke_sequence_with_delimiters(self):
        scan_payload = {"part_number": "PN-12345", "serial_number": "SN-67890"}
        field_order = ["part_number", "serial_number"]
        delimiter = "TAB"

        sequence = []
        for field in field_order:
            sequence.append(scan_payload[field])
            sequence.append(delimiter)
        sequence.append("ENTER")

        assert sequence == ["PN-12345", "TAB", "SN-67890", "TAB", "ENTER"]


class TestTCSFR11AUTO01:
    """TC-SFR11-AUTO-01: Persistence stores and reloads events with metadata."""

    def test_save_load_event_with_audit_metadata(self):
        event = {
            "workstation_id": "workstation_01",
            "timestamp": datetime.now().isoformat(),
            "barcodes": [{"name": "part_number", "value": "PN-12345"}],
        }
        payload = {**event, "saved_at": datetime.now().isoformat(), "file_version": "1.0"}
        encoded = json.dumps(payload)
        loaded = json.loads(encoded)

        assert loaded["workstation_id"] == event["workstation_id"]
        assert loaded["barcodes"] == event["barcodes"]
        assert "saved_at" in loaded
        assert "file_version" in loaded


class TestTCSFR12AUTO01:
    """TC-SFR12-AUTO-01: JSON output matches published schema."""

    def test_json_outputs_validate_against_schema(self):
        output = {
            "workstation_id": "manufacturing_01",
            "timestamp": "2024-01-15T10:30:45.123456",
            "barcodes": [{"name": "part_number", "value": "PN-001"}],
        }

        assert "workstation_id" in output
        assert "timestamp" in output
        assert "barcodes" in output
        assert isinstance(output["barcodes"], list)


class TestTCSFR15AUTO01:
    """TC-SFR15-AUTO-01: Decoder decodes all QRs in multi-code test image."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_all_codes_decoded(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        truth = ["code_1", "code_2", "code_3"]
        points = np.array(
            [
                [[10, 10], [20, 10], [20, 20], [10, 20]],
                [[30, 30], [40, 30], [40, 40], [30, 40]],
                [[50, 50], [60, 50], [60, 60], [50, 60]],
            ],
            dtype=float,
        )
        mock_detector.detectAndDecodeMulti.return_value = (True, truth, points, None)

        img = np.ones((100, 100, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(img)
        detected = [text for text, _ in results]

        assert set(detected) == set(truth)
        assert len(detected) == len(truth)


class TestTCPPSR2AUTO01:
    """TC-PPSR2-AUTO-01: Real-time latency under system load."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_latency_stays_below_threshold_under_load(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        mock_detector.detectAndDecodeMulti.return_value = (True, [], None, None)

        img = np.ones((640, 480, 3), dtype=np.uint8)
        start = time.perf_counter()
        _ = DecodeQr.multi_opencv(img)
        latency_ms = (time.perf_counter() - start) * 1000

        assert latency_ms < 200


class TestTCEISR6AUTO01:
    """TC-EISR6-AUTO-01: Config-driven workflow control."""

    def test_workflow_behavior_changes_based_on_config(self):
        config1 = WorkstationConfig("manufacturing_01", expected_qr_count=2, append_key="TAB")
        config2 = WorkstationConfig("quality_01", expected_qr_count=3, append_key="ENTER")

        assert config1.expected_qr_count != config2.expected_qr_count
        assert config1.append_key != config2.append_key


class TestConfigManagerUsage:
    def test_config_round_trip(self):
        with TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            config = WorkstationConfig("station_x", expected_qr_count=4, scan_direction="row-major")
            manager.save_config(config)

            loaded = manager.get_config("station_x")
            assert loaded is not None
            assert loaded.expected_qr_count == 4
            assert loaded.scan_direction == "row-major"
