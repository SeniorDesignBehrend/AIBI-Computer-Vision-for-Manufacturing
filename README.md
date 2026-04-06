# AIBI Computer Vision for Manufacturing

Two-part system for manufacturing quality control:

1. **QR/Barcode Scanner** (`aibi_cv`) — scans barcodes and outputs data to JSON or Excel
2. **Action Sequence Trainer** (`step_validation`) — teaches and verifies manufacturing process steps using computer vision (DINOv2)

---

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

---

## Action Sequence Trainer

A native desktop app (PySide6) for training and verifying that manufacturing workers perform process steps in the correct order. Launched directly or from a host application (e.g. VB.NET) via command-line arguments.

### Running

**Training mode** — record video segments for each step, then finalize to produce a `.pkl` process file:
```bash
uv run python -m step_validation.main --mode training
```

**Operation mode** — monitor a worker against a saved process in real time:
```bash
uv run python -m step_validation.main --mode operation --process path/to/process.pkl
```

### CLI Arguments

| Argument | Default | Description |
|---|---|---|
| `--mode` | *(required)* | `training` or `operation` |
| `--process PATH` | — | `.pkl` process file to load on startup |
| `--camera INDEX` | `0` | Camera device index |
| `--threshold FLOAT` | `0.75` | Min cosine similarity to count a frame as a match (0.5–1.0) |
| `--window SECONDS` | `2.0` | Detection window length in seconds |
| `--confidence FLOAT` | `0.70` | Fraction of frames in window required to confirm a step |
| `--log-dir PATH` | `logs/` | Directory to write run log JSON files |

### Launching from VB.NET

```vbnet
Dim proc As New Process()
proc.StartInfo.FileName = "python"
proc.StartInfo.Arguments = "-m step_validation.main --mode operation " &
    "--process C:\path\process.pkl --log-dir C:\logs"
proc.StartInfo.WorkingDirectory = "C:\path\to\AIBI-Computer-Vision-for-Manufacturing\src"
proc.Start()
```

### Training Workflow

1. Launch in `--mode training`
2. **Record** — use the Live Camera tab to record a video segment of each step, or upload a video file. Give each segment a name.
3. **Review** — reorder segments by dragging or using ↑/↓ buttons. Delete or rename as needed.
4. **Finalize** — click "Finalize Training" to compute DINOv2 embeddings. This may take a minute.
5. **Save** — click "Save Process (.pkl)" and share the file with operation machines.

### Operation Mode

The app shows a fullscreen camera feed with an overlay checklist of steps. It automatically advances through steps as each one is detected with sufficient confidence. State indicators:

| State | Meaning |
|---|---|
| `IDLE` | No action detected |
| `CORRECT_STEP` | Expected step detected, building confidence |
| `CONFIRMED` | Step confirmed, advancing |
| `WRONG_ORDER` | A past step was re-detected |
| `SKIPPED` | A future step detected before the expected one |
| `COMPLETE` | All steps verified |

Run logs are saved as JSON to `--log-dir` after each monitoring session.

### Run Log Format

`logs/run_1_20240115_143022.json`:
```json
{
  "run": 1,
  "started": "14:30:22",
  "completed": true,
  "steps": [
    { "step": "Attach Left Bracket", "result": "OK", "warnings": "-" },
    { "step": "Torque Bolts",        "result": "OK", "warnings": "Re-detected 'Attach Left Bracket'" }
  ]
}
```

---

## QR / Barcode Scanner

### Running

**Camera File** - Tracks required barcodes per workstation:
```bash
uv run python -m aibi_cv.Camera
```

### Barcode Format

Format barcodes as `field_name:value`:
- `part_number:PN-12345`
- `serial_number:SN-67890`
- `batch_id:BATCH-2024-01`

### Workstation Configuration

Each workstation is configured in `configs/{workstation_id}.json`:

```json
{
  "workstation_id": "workstation_01",
  "expected_qr_count": 6,
  "scan_direction": "row-major",
  "append_key": "NONE",
  "camera_index": 0
}
```

### Output Format

(`outputs/scan_{workstation_id}_{timestamp}.json`):
```json
{
  "workstation_id": "workstation_01",
  "timestamp": "2024-01-15T10:30:45.123456",
  "barcodes": [
    { "name": "part_number", "value": "PN-12345" },
    { "name": "serial_number", "value": "SN-67890" }
  ]
}
```

---

## Project Structure

```
src/
├── aibi_cv/                  # QR/barcode scanning package
│   ├── Camera.py             # Main camera/scanner class
└── step_validation/          # Action sequence trainer (PySide6 desktop app)
    ├── main.py               # Entry point (argparse + QApplication)
    ├── main_window.py        # QMainWindow with DINOv2 loading
    ├── process_manager.py    # State management
    ├── embeddings.py         # DINOv2 vision embeddings
    ├── verification.py       # State machine logic
    ├── models.py             # ActionStep dataclass
    ├── serialization.py      # .pkl save/load
    ├── state.py              # VerificationState enum
    ├── widgets/
    │   ├── training_widget.py   # Training UI
    │   └── operation_widget.py  # Operation UI
    └── workers/
        ├── camera_worker.py     # QThread: camera preview
        └── operation_worker.py  # QThread: monitoring loop
configs/                      # Workstation config files (JSON)
examples/                     # Example scanner scripts
tests/                        # Test suite
```

---

## Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov
```

---

## Troubleshooting

**xFormers warnings on startup** (DINOv2) — harmless, no action needed. Install `xformers` for a small speed improvement if desired.

**Lock file corrupted:**
```bash
del uv.lock
uv sync
```
