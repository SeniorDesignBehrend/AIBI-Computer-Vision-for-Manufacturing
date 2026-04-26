"""Basic parsing tests for the current parser implementation."""

from aibi_cv.parse import Parse


class TestBasicBarcodeParser:
    """Basic Data Matrix code parsing functionality tests."""

    def test_parse_colon_format(self):
        """Test parsing standard colon-separated format."""
        name, value = Parse.parse("part_number:PN-12345")
        assert name == "part_number"
        assert value == "PN-12345"

    def test_parse_json_format(self):
        """Test parsing JSON format Data Matrix codes."""
        json_data = '{"part_number": "PN-99999"}'
        name, value = Parse.parse(json_data)
        assert name == "part_number"
        assert value == "PN-99999"

    def test_parse_no_colon_returns_none_name(self):
        """Test parsing Data Matrix code without colon separator."""
        name, value = Parse.parse("PLAIN_TEXT_CODE")
        assert name is None
        assert value == "PLAIN_TEXT_CODE"