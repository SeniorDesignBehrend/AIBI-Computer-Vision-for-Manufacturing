"""Configuration management for workstation-specific barcode mapping."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class FieldMapping:
    """Maps a barcode position to a data field."""
    position_index: int
    field_name: str
    required: bool = True


@dataclass
class WorkstationConfig:
    """Configuration for a specific workstation."""
    workstation_id: str
    field_mappings: List[FieldMapping]
    camera_index: int = 0
    
    def to_dict(self) -> dict:
        return {
            "workstation_id": self.workstation_id,
            "field_mappings": [asdict(fm) for fm in self.field_mappings],
            "camera_index": self.camera_index
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'WorkstationConfig':
        mappings = [FieldMapping(**m) for m in data.get("field_mappings", [])]
        return cls(
            workstation_id=data["workstation_id"],
            field_mappings=mappings,
            camera_index=data.get("camera_index", 0)
        )


class ConfigManager:
    """Manages workstation configurations."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.configs: Dict[str, WorkstationConfig] = {}
        self._load_all_configs()
    
    def _load_all_configs(self):
        """Load all workstation configurations from disk."""
        for config_file in self.config_dir.glob("*.json"):
            try:
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    config = WorkstationConfig.from_dict(data)
                    self.configs[config.workstation_id] = config
            except Exception as e:
                print(f"Error loading config {config_file}: {e}")
    
    def get_config(self, workstation_id: str) -> Optional[WorkstationConfig]:
        """Get configuration for a specific workstation."""
        return self.configs.get(workstation_id)
    
    def save_config(self, config: WorkstationConfig):
        """Save workstation configuration to disk."""
        config_file = self.config_dir / f"{config.workstation_id}.json"
        with open(config_file, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        self.configs[config.workstation_id] = config
    
    def create_default_config(self, workstation_id: str) -> WorkstationConfig:
        """Create a default configuration for a workstation."""
        config = WorkstationConfig(
            workstation_id=workstation_id,
            field_mappings=[
                FieldMapping(0, "part_number", True),
                FieldMapping(1, "serial_number", True),
                FieldMapping(2, "batch_id", False),
            ],
            camera_index=0
        )
        self.save_config(config)
        return config
