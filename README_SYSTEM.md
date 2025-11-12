# QR Code Scanning System

Simple QR code scanning system that outputs scan data to JSON files.

## System Architecture

The system implements the following key requirements:

### Functional Requirements Implemented

- **SFR1, SFR15, SFR16**: Fixed-station cameras detect, decode, and output all barcodes/QR codes in a single frame
- **SFR4**: Aggregates decoded values into structured JSON documents
- **SFR11**: Local data storage with audit metadata

### Core Components

```
src/aibi_cv/
├── barcode_scanner.py    # QR/barcode detection and decoding
├── config_manager.py     # Workstation configuration management
├── data_formatter.py     # JSON payload formatting
├── data_storage.py       # SQLite-based local persistence
├── vision_system.py      # Main system controller
└── cli.py               # Command-line interface
```

## Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Run Simple QR Scanner

```bash
# Outputs to outputs/qr_scans.json
uv run python examples/qr/simple_qr_scanner.py
```

Press 's' to save scans to JSON file, 'q' to quit without saving.

### 3. Run Advanced Scanner (Optional)

```bash
# Using CLI
uv run python -m aibi_cv.cli scan --workstation workstation_01

# Using example script
uv run python examples/qr/advanced_scanner.py
```

### 4. Run Simulation (No Camera Required)

```bash
uv run python examples/qr/simulation_test.py
```

## Configuration

### Workstation Configuration

Each workstation has a JSON configuration file that maps barcode positions to data fields:

```json
{
  "workstation_id": "workstation_01",
  "field_mappings": [
    {"position_index": 0, "field_name": "part_number", "required": true},
    {"position_index": 1, "field_name": "serial_number", "required": true},
    {"position_index": 2, "field_name": "batch_id", "required": false}
  ],
  "camera_index": 0
}
```

### Create New Configuration

```bash
uv run python -m aibi_cv.cli config --create workstation_02
```

### List Configurations

```bash
uv run python -m aibi_cv.cli config --list
```

## JSON Output Schema

### Simple Scanner Output

The simple scanner outputs to `outputs/qr_scans.json`:

```json
[
  {
    "timestamp": "2024-01-15T10:30:45.123456",
    "data": "QR_CODE_CONTENT",
    "type": "QR_CODE"
  }
]
```

### Advanced Scanner Output

The advanced scanner follows this schema (v1.0):

```json
{
  "schema_version": "1.0",
  "event_type": "barcode_scan",
  "workstation_id": "workstation_01",
  "timestamp": "2024-01-15T10:30:45.123456",
  "scan_data": {
    "fields": {
      "part_number": "PN-12345",
      "serial_number": "SN-67890",
      "batch_id": "BATCH-2024-01"
    },
    "raw_detections": [
      {
        "position": 0,
        "type": "QR_CODE",
        "data": "PN-12345",
        "confidence": 1.0,
        "timestamp": "2024-01-15T10:30:45.123456"
      }
    ]
  },
  "metadata": {
    "total_detections": 3,
    "required_fields_complete": true
  }
}
```

## Data Storage

All data is stored locally in SQLite:

- **scan_events**: All barcode scan events with JSON payloads
- **system_logs**: System events and errors

Database location: `data/scans.db` (configurable)

## Usage Examples

### Python API

```python
from pathlib import Path
from aibi_cv import VisionSystem

# Initialize system
system = VisionSystem(
    workstation_id="workstation_01",
    config_dir=Path("data/config"),
    db_path=Path("data/scans.db"),
    camera_index=0
)

# Run live scanning with callback
def on_detection(detections, payload):
    if payload["metadata"]["required_fields_complete"]:
        print(f"Complete scan: {payload['scan_data']['fields']}")

system.run_live(display=True, callback=on_detection)
```

### Process Single Image

```python
from pathlib import Path
from aibi_cv import VisionSystem

system = VisionSystem(
    workstation_id="workstation_01",
    config_dir=Path("data/config"),
    db_path=Path("data/scans.db")
)

detections, payload = system.process_image(Path("test_image.jpg"))
print(f"Found {len(detections)} barcodes")
```

## Testing

### Run Simulation Tests

The simulation environment generates synthetic QR codes for testing:

```bash
uv run python examples/qr/simulation_test.py
```

This tests multiple scenarios:
- Complete part scan (all required fields)
- Missing optional fields
- Single QR code
- Multiple parts

## Performance

- **Latency**: <200ms processing time per frame (PPSR1)
- **Accuracy**: >99% barcode detection accuracy (PPSR3)
- **Camera Support**: Works with 720p cameras (PPSR5)
- **Uptime**: 99% minimum during operational hours (PDSR3)

## Security & Compliance

- **On-Premises Only**: All processing and storage local (PDSR1, PDSR2)
- **No Cloud Dependencies**: Fully offline capable
- **Audit Trail**: Complete logging of all events
- **Data Privacy**: No external data transmission

## Integration

The system provides multiple integration methods:

1. **JSON Files**: Simple scanner outputs to `outputs/qr_scans.json`
2. **Database**: Advanced scanner uses SQLite for batch processing
3. **Python API**: Direct integration via VisionSystem class

## Troubleshooting

### Camera Not Opening
```bash
# Test camera access
uv run python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Database Issues
```bash
# Check database
sqlite3 data/scans.db "SELECT COUNT(*) FROM scan_events;"
```

## Next Steps

1. **Barcode Support**: Add support for 1D barcodes using pyzbar
2. **Enhanced Output**: Add more metadata to JSON output
3. **Batch Processing**: Process multiple images from a folder
4. **Performance Optimization**: Optimize detection speed
