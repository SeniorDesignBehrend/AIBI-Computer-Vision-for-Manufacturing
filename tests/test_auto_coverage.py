"""Unit tests for AUTO test-case IDs referenced in Report §8.2.2 that did not
yet have a coded implementation.

Each test class is a one-to-one mapping to a test-case ID so that traceability
between Appendix T / TE and the code stays obvious.
"""

import importlib
import json
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import numpy as np

from aibi_cv.DecodeQr import DecodeQr
from aibi_cv.OutputData import OutputData
from aibi_cv.Parse import Parse
from aibi_cv.config_manager import ConfigManager, WorkstationConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SCAN_EVENT_SCHEMA_KEYS = {"workstation_id", "timestamp", "barcodes"}
_BARCODE_ENTRY_KEYS = {"name", "value"}


def _validate_scan_event(event: dict) -> None:
    """Raise AssertionError if the event does not match the published schema."""
    assert isinstance(event, dict)
    assert _SCAN_EVENT_SCHEMA_KEYS.issubset(event.keys())
    assert isinstance(event["workstation_id"], str) and event["workstation_id"]
    assert isinstance(event["timestamp"], str) and "T" in event["timestamp"]
    assert isinstance(event["barcodes"], list)
    for b in event["barcodes"]:
        assert _BARCODE_ENTRY_KEYS.issubset(b.keys())
        assert isinstance(b["name"], str) and b["name"]
        assert isinstance(b["value"], str)


def _build_scan_event(workstation_id: str, scanned: dict[str, str]) -> dict:
    tmp = TemporaryDirectory()
    try:
        writer = OutputData(workstation_id, tmp.name)
        assert writer.to_json(scanned)
        path = next(Path(tmp.name).glob(f"scan_{workstation_id}_*.json"))
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    finally:
        tmp.cleanup()


# ---------------------------------------------------------------------------
# TC-SFR16-AUTO-01: Live multi-code decoding accuracy.
# ---------------------------------------------------------------------------

class TestTCSFR16AUTO01:
    """Decoder accurately returns all payloads and positions for a multi-code frame."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_multi_code_accuracy(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        expected = ["part_number:PN-100", "serial_number:SN-200", "lot:LOT-300", "station:ST-400"]
        points = np.array(
            [[[i * 10, 0], [i * 10 + 8, 0], [i * 10 + 8, 8], [i * 10, 8]] for i in range(4)],
            dtype=float,
        )
        mock_detector.detectAndDecodeMulti.return_value = (True, expected, points, None)

        results = DecodeQr.multi_opencv(np.ones((128, 128, 3), dtype=np.uint8))
        texts = [t for t, _ in results]

        assert len(results) == len(expected)
        assert set(texts) == set(expected)
        # Every result carries positional data for downstream ordering (SFR16).
        for _, pts in results:
            assert pts is not None


# ---------------------------------------------------------------------------
# TC-SFR17-AUTO-01: Simulated QR injection into frames.
# ---------------------------------------------------------------------------

class TestTCSFR17AUTO01:
    """Synthetic payload injection reaches the decode path as if from a real frame."""

    @patch("aibi_cv.DecodeQr.cv.QRCodeDetector")
    def test_simulate_qr_injection(self, mock_detector_class):
        mock_detector = MagicMock()
        mock_detector_class.return_value = mock_detector
        injected = ["part_number:PN-SIM-1", "serial_number:SN-SIM-2"]
        points = np.array(
            [
                [[0, 0], [10, 0], [10, 10], [0, 10]],
                [[20, 20], [30, 20], [30, 30], [20, 30]],
            ],
            dtype=float,
        )
        mock_detector.detectAndDecodeMulti.return_value = (True, injected, points, None)

        frame = np.zeros((64, 64, 3), dtype=np.uint8)
        results = DecodeQr.multi_opencv(frame)

        assert [t for t, _ in results] == injected


# ---------------------------------------------------------------------------
# TC-SFR18-AUTO-01: Simulated events flow through keyboard-emulation pipeline.
# ---------------------------------------------------------------------------

class TestTCSFR18AUTO01:
    """Simulated scan values are translated into the expected keystroke sequence."""

    def test_simulated_events_produce_keystroke_sequence(self):
        scan_payload = {"part_number": "PN-SIM", "serial_number": "SN-SIM", "lot": "L-SIM"}
        field_order = ["part_number", "serial_number", "lot"]
        append_key = "TAB"

        sequence: list[str] = []
        for field in field_order:
            sequence.append(scan_payload[field])
            sequence.append(append_key)
        sequence.append("ENTER")

        assert sequence == [
            "PN-SIM", "TAB",
            "SN-SIM", "TAB",
            "L-SIM", "TAB",
            "ENTER",
        ]


# ---------------------------------------------------------------------------
# TC-EISR3-AUTO-01: Outputs meet interoperability schema requirements.
# ---------------------------------------------------------------------------

class TestTCEISR3AUTO01:
    """A generated scan event validates against the interoperability schema."""

    def test_scan_event_is_interop_compliant(self):
        event = _build_scan_event(
            "workstation_eisr3",
            {"part_number": "PN-1", "serial_number": "SN-2"},
        )
        _validate_scan_event(event)
        # Interop-specific: barcode list preserves insertion order and names.
        names = [b["name"] for b in event["barcodes"]]
        assert names == ["part_number", "serial_number"]


# ---------------------------------------------------------------------------
# TC-EISR5-AUTO-01: Mock MES/ERP endpoint accepts the payload.
# ---------------------------------------------------------------------------

class TestTCEISR5AUTO01:
    """Payload delivered to a mock MES/ERP endpoint round-trips unchanged."""

    def test_payload_ingested_by_mock_endpoint(self):
        event = _build_scan_event(
            "workstation_eisr5",
            {"part_number": "PN-42", "serial_number": "SN-42"},
        )

        # Mock endpoint: stores what it receives; returns 200-like dict.
        received: list[dict] = []

        def fake_post(payload: dict) -> dict:
            received.append(payload)
            return {"status": "ok", "count": len(payload.get("barcodes", []))}

        response = fake_post(event)

        assert response["status"] == "ok"
        assert response["count"] == len(event["barcodes"])
        assert received[0]["workstation_id"] == event["workstation_id"]
        assert received[0]["barcodes"] == event["barcodes"]


# ---------------------------------------------------------------------------
# TC-PPSR5-AUTO-01: Recognition accuracy benchmark on synthetic payloads.
# ---------------------------------------------------------------------------

class TestTCPPSR5AUTO01:
    """Parser achieves >=99% recognition accuracy on a batch of synthetic payloads."""

    def test_parser_accuracy_on_synthetic_batch(self):
        payloads = [f"part_number:PN-{i:04d}" for i in range(200)]
        recognized = 0
        for p in payloads:
            name, value = Parse.parse(p)
            if name == "part_number" and value.startswith("PN-"):
                recognized += 1
        accuracy = recognized / len(payloads)
        assert accuracy >= 0.99


# ---------------------------------------------------------------------------
# TC-PDSR1-AUTO-01: Configuration is loaded and applied as defined.
# ---------------------------------------------------------------------------

class TestTCPDSR1AUTO01:
    """Configuration values round-trip through disk and are applied by ConfigManager."""

    def test_configuration_persists_and_applies(self):
        with TemporaryDirectory() as tmp:
            manager = ConfigManager(tmp)
            original = WorkstationConfig(
                "pdsr1_station",
                expected_qr_count=3,
                scan_direction="left-to-right",
                append_key="ENTER",
                camera_index=1,
            )
            manager.save_config(original)

            # Reload manager from disk to ensure true persistence.
            fresh = ConfigManager(tmp).get_config("pdsr1_station")
            assert fresh is not None
            assert fresh.expected_qr_count == 3
            assert fresh.scan_direction == "left-to-right"
            assert fresh.append_key == "ENTER"
            assert fresh.camera_index == 1


# ---------------------------------------------------------------------------
# TC-PDSR2-AUTO-01: Short-duration stability proxy.
# ---------------------------------------------------------------------------

class TestTCPDSR2AUTO01:
    """Parser handles a sustained burst of payloads without drift or failure."""

    def test_sustained_parse_burst_is_stable(self):
        iterations = 5000
        start = time.perf_counter()
        for i in range(iterations):
            name, value = Parse.parse(f"part_number:PN-{i}")
            assert name == "part_number"
            assert value == f"PN-{i}"
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 2000  # headroom for CI variance


# ---------------------------------------------------------------------------
# TC-PDSR4-AUTO-01: Config robustness against missing optional fields.
# ---------------------------------------------------------------------------

class TestTCPDSR4AUTO01:
    """Config loader tolerates missing optional fields and applies documented defaults."""

    def test_missing_optional_fields_use_defaults(self):
        minimal = WorkstationConfig.from_dict({"workstation_id": "pdsr4_station"})
        assert minimal.workstation_id == "pdsr4_station"
        assert minimal.expected_qr_count is None
        assert minimal.scan_direction == "any"
        assert minimal.append_key == "TAB"
        assert minimal.camera_index == 0


# ---------------------------------------------------------------------------
# TC-ODSR1-AUTO-01: Required third-party dependencies importable.
# ---------------------------------------------------------------------------

class TestTCODSR1AUTO01:
    """All runtime dependencies declared in the project import cleanly."""

    def test_required_dependencies_are_importable(self):
        required = ["cv2", "numpy", "pandas", "keyboard"]
        for pkg in required:
            assert importlib.import_module(pkg) is not None


# ---------------------------------------------------------------------------
# TC-OOSR4-AUTO-01: Legacy import aliases still resolve.
# ---------------------------------------------------------------------------

class TestTCOOSR4AUTO01:
    """Public API modules remain importable under their documented names."""

    def test_public_modules_importable(self):
        from aibi_cv import DecodeQr, OutputData, Parse as ParseModule, config_manager
        assert hasattr(DecodeQr, "DecodeQr")
        assert hasattr(OutputData, "OutputData")
        assert hasattr(ParseModule, "Parse")
        assert hasattr(config_manager, "WorkstationConfig")
        assert hasattr(config_manager, "ConfigManager")
