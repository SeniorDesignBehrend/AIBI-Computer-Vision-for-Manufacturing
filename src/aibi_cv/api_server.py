"""REST API server for vision system integration."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List, Dict, Any
import uvicorn
from .vision_system import VisionSystem
from .data_storage import DataStorage


app = FastAPI(title="AIBI Vision System API", version="1.0")

# Global state
vision_systems: Dict[str, VisionSystem] = {}
storage: Optional[DataStorage] = None


class ScanRequest(BaseModel):
    workstation_id: str
    image_data: Optional[str] = None  # Base64 encoded image


class ConfigUpdate(BaseModel):
    workstation_id: str
    field_mappings: List[Dict[str, Any]]
    camera_index: int = 0


def init_api(config_dir: Path, db_path: Path):
    """Initialize API with configuration."""
    global storage
    storage = DataStorage(db_path)


@app.get("/")
async def root():
    """API health check."""
    return {"status": "online", "service": "AIBI Vision System"}


@app.get("/api/v1/workstations")
async def list_workstations():
    """List all configured workstations."""
    return {"workstations": list(vision_systems.keys())}


@app.get("/api/v1/workstation/{workstation_id}/status")
async def get_workstation_status(workstation_id: str):
    """Get status of a specific workstation."""
    if workstation_id not in vision_systems:
        raise HTTPException(status_code=404, detail="Workstation not found")
    
    system = vision_systems[workstation_id]
    return system.get_stats()


@app.get("/api/v1/scans/unsynced")
async def get_unsynced_scans(limit: int = 100):
    """Retrieve unsynced scan events."""
    if not storage:
        raise HTTPException(status_code=500, detail="Storage not initialized")
    
    events = storage.get_unsynced_events(limit)
    return {"events": events, "count": len(events)}


@app.post("/api/v1/scans/mark-synced")
async def mark_scans_synced(event_ids: List[int]):
    """Mark scan events as synced."""
    if not storage:
        raise HTTPException(status_code=500, detail="Storage not initialized")
    
    storage.mark_synced(event_ids)
    return {"status": "success", "synced_count": len(event_ids)}


@app.get("/api/v1/logs")
async def get_logs(limit: int = 100, level: Optional[str] = None):
    """Retrieve system logs."""
    if not storage:
        raise HTTPException(status_code=500, detail="Storage not initialized")
    
    logs = storage.get_recent_logs(limit, level)
    return {"logs": logs, "count": len(logs)}


@app.get("/api/v1/schema")
async def get_json_schema():
    """Get the JSON schema for scan events."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Barcode Scan Event",
        "type": "object",
        "required": ["schema_version", "event_type", "workstation_id", "timestamp", "scan_data"],
        "properties": {
            "schema_version": {"type": "string", "const": "1.0"},
            "event_type": {"type": "string", "const": "barcode_scan"},
            "workstation_id": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "scan_data": {
                "type": "object",
                "properties": {
                    "fields": {"type": "object"},
                    "raw_detections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "position": {"type": "integer"},
                                "type": {"type": "string"},
                                "data": {"type": "string"},
                                "confidence": {"type": "number"},
                                "timestamp": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "total_detections": {"type": "integer"},
                    "required_fields_complete": {"type": "boolean"}
                }
            }
        }
    }
    return schema


def run_server(host: str = "127.0.0.1", port: int = 8000, config_dir: Path = None, db_path: Path = None):
    """Run the API server."""
    if config_dir and db_path:
        init_api(config_dir, db_path)
    
    uvicorn.run(app, host=host, port=port)
