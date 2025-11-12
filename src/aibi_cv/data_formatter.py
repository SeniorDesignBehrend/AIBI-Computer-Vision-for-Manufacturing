"""JSON data formatting and output generation."""

import json
from typing import List, Dict, Any
from datetime import datetime
from .barcode_scanner import BarcodeDetection
from .config_manager import WorkstationConfig


class DataFormatter:
    """Formats scan results into structured JSON output."""
    
    def __init__(self, workstation_config: WorkstationConfig):
        self.config = workstation_config
    
    def format_scan_event(self, detections: List[BarcodeDetection]) -> Dict[str, Any]:
        """Format detections into structured JSON payload."""
        # Map detections by position index
        mapped_fields = {}
        for i, detection in enumerate(detections):
            mapped_fields[f"field_{i}"] = detection.data
        
        # Build complete payload
        payload = {
            "schema_version": "1.0",
            "event_type": "barcode_scan",
            "workstation_id": self.config.workstation_id,
            "timestamp": datetime.now().isoformat(),
            "scan_data": {
                "fields": mapped_fields,
                "raw_detections": [
                    {
                        "position": d.position_index,
                        "type": d.type,
                        "data": d.data,
                        "confidence": d.confidence,
                        "timestamp": d.timestamp
                    }
                    for d in detections
                ]
            },
            "metadata": {
                "total_detections": len(detections),
                "required_fields_complete": len(detections) > 0
            }
        }
        
        return payload
    
    def to_json_string(self, payload: Dict[str, Any], pretty: bool = False) -> str:
        """Convert payload to JSON string."""
        if pretty:
            return json.dumps(payload, indent=2)
        return json.dumps(payload)
    
    def validate_payload(self, payload: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate payload against schema requirements."""
        errors = []
        
        # Check required top-level fields
        required_fields = ["schema_version", "event_type", "workstation_id", "timestamp", "scan_data"]
        for field in required_fields:
            if field not in payload:
                errors.append(f"Missing required field: {field}")
        
        # Check required data fields
        if "scan_data" in payload and "fields" in payload["scan_data"]:
            for field in self.config.barcode_fields:
                if field.required:
                    value = payload["scan_data"]["fields"].get(field.name)
                    if value is None:
                        errors.append(f"Missing required field: {field.name}")
        
        return len(errors) == 0, errors
