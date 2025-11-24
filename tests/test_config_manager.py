"""Tests for config_manager module."""

import json
import pytest
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
        fields = [
            BarcodeField("part_number", True),
            BarcodeField("serial_number", True),
            BarcodeField("batch_id", False)
        ]
        config = WorkstationConfig("ws01", fields, 0)
        
        assert config.workstation_id == "ws01"
        assert len(config.barcode_fields) == 3
        assert config.camera_index == 0

    def test_to_dict(self):
        fields = [BarcodeField("part_number", True)]
        config = WorkstationConfig("ws01", fields)
        
        result = config.to_dict()
        expected = {
            "workstation_id": "ws01",
            "barcode_fields": [{"name": "part_number", "required": True}],
            "camera_index": 0
        }
        assert result == expected

    def test_from_dict(self):
        data = {
            "workstation_id": "ws01",
            "barcode_fields": [
                {"name": "part_number", "required": True},
                {"name": "batch_id", "required": False}
            ],
            "camera_index": 1
        }
        
        config = WorkstationConfig.from_dict(data)
        assert config.workstation_id == "ws01"
        assert len(config.barcode_fields) == 2
        assert config.barcode_fields[0].name == "part_number"
        assert config.barcode_fields[0].required is True
        assert config.barcode_fields[1].name == "batch_id"
        assert config.barcode_fields[1].required is False
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
            
            fields = [BarcodeField("part_number", True)]
            config = WorkstationConfig("test_ws", fields)
            
            manager.save_config(config)
            retrieved = manager.get_config("test_ws")
            
            assert retrieved is not None
            assert retrieved.workstation_id == "test_ws"
            assert len(retrieved.barcode_fields) == 1

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
            assert len(config.barcode_fields) == 3
            
            # Check default fields
            field_names = [f.name for f in config.barcode_fields]
            assert "part_number" in field_names
            assert "serial_number" in field_names
            assert "batch_id" in field_names

    def test_load_existing_configs(self):
        with TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)
            
            # Create a config file manually
            config_data = {
                "workstation_id": "existing_ws",
                "barcode_fields": [{"name": "test_field", "required": True}],
                "camera_index": 2
            }
            
            config_file = config_dir / "existing_ws.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
            
            # Initialize manager - should load existing config
            manager = ConfigManager(config_dir)
            config = manager.get_config("existing_ws")
            
            assert config is not None
            assert config.workstation_id == "existing_ws"
            assert config.camera_index == 2