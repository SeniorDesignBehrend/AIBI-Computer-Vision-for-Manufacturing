"""Tests for vision system integration."""

import pytest
from pathlib import Path
import tempfile
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aibi_cv.vision_system import VisionSystem
from aibi_cv.config_manager import ConfigManager, WorkstationConfig, FieldMapping


def test_vision_system_initialization():
    """Test vision system can be initialized."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        db_path = Path(tmpdir) / "test.db"
        
        system = VisionSystem(
            workstation_id="test_ws",
            config_dir=config_dir,
            db_path=db_path,
            camera_index=0
        )
        
        assert system.workstation_id == "test_ws"
        assert system.config is not None


def test_config_creation():
    """Test default configuration is created."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        db_path = Path(tmpdir) / "test.db"
        
        system = VisionSystem(
            workstation_id="new_ws",
            config_dir=config_dir,
            db_path=db_path
        )
        
        assert system.config.workstation_id == "new_ws"
        assert len(system.config.field_mappings) > 0


def test_stats_tracking():
    """Test statistics tracking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        db_path = Path(tmpdir) / "test.db"
        
        system = VisionSystem(
            workstation_id="stats_test",
            config_dir=config_dir,
            db_path=db_path
        )
        
        stats = system.get_stats()
        
        assert stats["workstation_id"] == "stats_test"
        assert stats["total_scans"] == 0
        assert stats["successful_scans"] == 0
        assert stats["failed_scans"] == 0
