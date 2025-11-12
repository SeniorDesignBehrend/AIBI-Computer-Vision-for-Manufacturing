# AIBI Computer Vision for Manufacturing

QR code scanning system for manufacturing that outputs scan data to JSON files.

## Quick Start

### 1. Install uv
```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install dependencies
```bash
uv sync
```

### 3. Run Scanner

**Simple Scanner** - Saves all QR codes to JSON:
```bash
uv run python examples/qr/simple_qr_scanner.py
```
Press 's' to save, 'q' to quit. Output: `outputs/qr_scans.json`

**Advanced Scanner** - Tracks required barcodes per workstation:
```bash
uv run python examples/qr/advanced_scanner.py
```
Press 's' to save (when complete), 'r' to reset, 'q' to quit.

**Simulation Test** - Test without camera (generates synthetic QR codes):
```bash
uv run python examples/qr/simulation_test.py
```

## Barcode Format

Format barcodes as: `field_name:value`

Examples:
- `part_number:PN-12345`
- `serial_number:SN-67890`
- `batch_id:BATCH-2024-01`

## Workstation Configuration

Each workstation defines required barcode fields in `data/config/{workstation_id}.json`:

```json
{
  "workstation_id": "workstation_01",
  "barcode_fields": [
    {"name": "part_number", "required": true},
    {"name": "serial_number", "required": true},
    {"name": "batch_id", "required": false}
  ],
  "camera_index": 0
}
```

## Output Format

**Simple Scanner** (`outputs/qr_scans.json`):
```json
[
  {
    "timestamp": "2024-01-15T10:30:45.123456",
    "data": "part_number:PN-12345",
    "type": "QR_CODE"
  }
]
```

**Advanced Scanner** (`outputs/scan_{workstation_id}_{timestamp}.json`):
```json
{
  "workstation_id": "workstation_01",
  "timestamp": "2024-01-15T10:30:45.123456",
  "barcodes": [
    {"name": "part_number", "value": "PN-12345"},
    {"name": "serial_number", "value": "SN-67890"}
  ]
}
```

## Project Structure

```
├── src/aibi_cv/          # Main package
├── examples/qr/          # Scanner examples
├── data/config/          # Workstation configs
├── outputs/              # Scan results (JSON)
├── tests/                # Test files
└── docs/                 # Documentation
```

## Creating New Workstations

1. Create config: `data/config/workstation_02.json`
2. Define required barcode fields
3. Update `workstation_id` in `advanced_scanner.py`
4. Run scanner

## Troubleshooting

**Camera not opening:**
```bash
uv run python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**Lock file corrupted:**
```bash
del uv.lock
uv sync
```
