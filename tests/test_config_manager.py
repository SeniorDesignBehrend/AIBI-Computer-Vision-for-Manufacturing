"""Tests for config_manager module."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from aibi_cv.config_manager import ConfigManager, WorkstationConfig, BarcodeField


class TestBarcodeField:
    def test_create_required_field(self):
        field = BarcodeField("part_number", True)
        assert field.name == "part_number"
        assert field.required is True

    def test_create_optional_field(self):
        field = BarcodeField("batch_id", False)
        assert field.name == "batch_id"
        assert field.required is False

    def test_default_required(self):
        field = BarcodeField("serial_number")
        assert field.required is True


class TestWorkstationConfig:
    def test_create_config(self):
        config = WorkstationConfig(
            workstation_id="ws01",
            expected_qr_count=3,
            scan_direction="left-to-right",
            append_key="TAB",
            camera_index=0,
        )

        assert config.workstation_id == "ws01"
        assert config.expected_qr_count == 3
        assert config.scan_direction == "left-to-right"
        assert config.append_key == "TAB"
        assert config.camera_index == 0

    def test_to_dict(self):
        config = WorkstationConfig(
            workstation_id="ws01",
            expected_qr_count=1,
            scan_direction="top-to-bottom",
            append_key="ENTER",
            camera_index=2,
        )

        result = config.to_dict()
        expected = {
            "workstation_id": "ws01",
            "expected_qr_count": 1,
            "scan_direction": "top-to-bottom",
            "append_key": "ENTER",
            "camera_index": 2,
        }
        assert result == expected

    def test_from_dict(self):
        data = {
            "workstation_id": "ws01",
            "expected_qr_count": 2,
            "scan_direction": "right-to-left",
            "append_key": "NONE",
            "camera_index": 1,
        }

        config = WorkstationConfig.from_dict(data)
        assert config.workstation_id == "ws01"
        assert config.expected_qr_count == 2
        assert config.scan_direction == "right-to-left"
        assert config.append_key == "NONE"
        assert config.camera_index == 1


class TestConfigManager:
    def test_init_creates_directory(self):
        with TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config"
            manager = ConfigManager(config_dir)
            assert config_dir.exists()

    def test_save_and_get_config(self):
        with TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir) / "config"
            manager = ConfigManager(config_dir)

            config = WorkstationConfig("test_ws", expected_qr_count=1)

            manager.save_config(config)
            retrieved = manager.get_config("test_ws")

            assert retrieved is not None
            assert retrieved.workstation_id == "test_ws"
            assert retrieved.expected_qr_count == 1

    def test_get_nonexistent_config(self):
        with TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            result = manager.get_config("nonexistent")
            assert result is None

    def test_create_default_config(self):
        with TemporaryDirectory() as temp_dir:
            manager = ConfigManager(temp_dir)
            config = manager.create_default_config("new_ws")

            assert config.workstation_id == "new_ws"
            assert config.expected_qr_count is None
            assert config.scan_direction == "any"
            assert config.append_key == "TAB"
            assert config.camera_index == 0

    def test_load_existing_configs(self):
        with TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)
            
            # Create a config file manually
            config_data = {
                "workstation_id": "existing_ws",
                "expected_qr_count": 4,
                "scan_direction": "row-major",
                "append_key": "ENTER",
                "camera_index": 2,
            }

            config_file = config_dir / "existing_ws.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)

            # Initialize manager - should load existing config
            manager = ConfigManager(config_dir)
            config = manager.get_config("existing_ws")

            assert config is not None
            assert config.workstation_id == "existing_ws"
            assert config.expected_qr_count == 4
            assert config.scan_direction == "row-major"
            assert config.append_key == "ENTER"
            assert config.camera_index == 2