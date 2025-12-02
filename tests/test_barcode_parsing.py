"""Basic barcode parsing tests - see test_comprehensive.py for SFR compliance tests."""

import pytest
from aibi_cv.advanced_scanner import parse_barcode


class TestBasicBarcodeParser:
    """Basic barcode parsing functionality tests."""
    
    def test_parse_colon_format(self):
        """Test parsing standard colon-separated format."""
        name, value = parse_barcode("part_number:PN-12345")
        assert name == "part_number"
        assert value == "PN-12345"

    def test_parse_json_format(self):
        """Test parsing JSON format barcodes."""
        json_data = '{"part_number": "PN-99999"}'
        name, value = parse_barcode(json_data)
        assert name == "part_number"
        assert value == "PN-99999"

    def test_parse_no_colon_returns_none_name(self):
        """Test parsing data without colon separator."""
        name, value = parse_barcode("PLAIN_TEXT_CODE")
        assert name is None
        assert value == "PLAIN_TEXT_CODE"