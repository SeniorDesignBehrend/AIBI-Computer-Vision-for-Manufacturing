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

# For development (includes pytest)
uv sync --extra dev
```

### 3. Run Scanner

**Camera File** - Tracks required barcodes per workstation:
```bash
uv run python -m aibi_cv.Camera
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
3. Launch scanner with the target workstation ID in the Camera entrypoint
4. Run scanner

## Testing

**Run SFR compliance tests:**
```bash
uv run python run_sfr_tests.py --sfr-only
```

**Run all tests:**
```bash
uv run python run_sfr_tests.py
```

**Run with coverage:**
```bash
uv run python run_sfr_tests.py --coverage
```

**Legacy test runner:**
```bash
uv run python run_tests.py
```

### Test Categories

- **SFR Compliance Tests** (`test_comprehensive.py`) - Full Software Functional Requirements validation
- **Basic Tests** (`test_*.py`) - Core functionality verification
- **Integration Tests** - End-to-end workflow validation

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
