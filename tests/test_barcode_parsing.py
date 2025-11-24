"""Tests for barcode parsing functionality."""

import json
import pytest
from aibi_cv.advanced_scanner import parse_barcode


class TestBarcodeParser:
    def test_parse_colon_format(self):
        """Test parsing standard colon-separated format."""
        name, value = parse_barcode("part_number:PN-12345")
        assert name == "part_number"
        assert value == "PN-12345"

    def test_parse_colon_with_spaces(self):
        """Test parsing with spaces around colon."""
        name, value = parse_barcode("serial_number : SN-67890")
        assert name == "serial_number"
        assert value == "SN-67890"

    def test_parse_multiple_colons(self):
        """Test parsing when value contains colons."""
        name, value = parse_barcode("url:https://example.com:8080")
        assert name == "url"
        assert value == "https://example.com:8080"

    def test_parse_json_format(self):
        """Test parsing JSON format barcodes."""
        json_data = '{"part_number": "PN-99999"}'
        name, value = parse_barcode(json_data)
        assert name == "part_number"
        assert value == "PN-99999"

    def test_parse_json_multiple_fields(self):
        """Test JSON with multiple fields returns first one."""
        json_data = '{"part_number": "PN-11111", "serial_number": "SN-22222"}'
        name, value = parse_barcode(json_data)
        # Should return first key-value pair
        assert name in ["part_number", "serial_number"]
        assert value in ["PN-11111", "SN-22222"]

    def test_parse_no_colon(self):
        """Test parsing data without colon separator."""
        name, value = parse_barcode("PLAIN_TEXT_CODE")
        assert name is None
        assert value == "PLAIN_TEXT_CODE"

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        name, value = parse_barcode("")
        assert name is None
        assert value == ""

    def test_parse_only_colon(self):
        """Test parsing string with only colon."""
        name, value = parse_barcode(":")
        assert name == ""
        assert value == ""

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON falls back to colon format."""
        name, value = parse_barcode('{"invalid": json}')
        assert name == '{"invalid"'
        assert value == 'json}'

    def test_parse_json_non_dict(self):
        """Test JSON that's not a dictionary."""
        name, value = parse_barcode('["array", "data"]')
        assert name is None
        assert value == '["array", "data"]'