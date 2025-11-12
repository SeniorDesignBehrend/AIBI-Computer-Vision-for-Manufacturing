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
        # Map detections to configured fields
        mapped_fields = {}
        for mapping in self.config.field_mappings:
            matching_detection = next(
                (d for d in detections if d.position_index == mapping.position_index),
                None
            )
            if matching_detection:
                mapped_fields[mapping.field_name] = matching_detection.data
            elif mapping.required:
                mapped_fields[mapping.field_name] = None
        
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
                "required_fields_complete": all(
                    mapped_fields.get(m.field_name) is not None
                    for m in self.config.field_mappings if m.required
                )
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
            for mapping in self.config.field_mappings:
                if mapping.required:
                    value = payload["scan_data"]["fields"].get(mapping.field_name)
                    if value is None:
                        errors.append(f"Missing required field: {mapping.field_name}")
        
        return len(errors) == 0, errors
