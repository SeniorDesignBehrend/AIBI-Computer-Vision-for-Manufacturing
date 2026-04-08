# Barcode Format Guide

## Overview

The advanced scanner uses named barcodes to track which fields have been scanned. Each workstation has a configuration file that defines which barcode fields are required.

## Barcode Format

All barcodes must follow this format:
```
field_name:value
```

### Examples

```
part_number:PN-12345
serial_number:SN-67890
batch_id:BATCH-2024-01
operator_id:OP-001
quality_check:PASS
```

## Workstation Configuration

Each workstation defines its required and optional fields in `data/config/{workstation_id}.json`:

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

## Scanner Behavior

1. **Scanning**: The scanner continuously looks for QR codes
2. **Filtering**: Only barcodes matching the workstation's field list are tracked
3. **Tracking**: Each field can only be scanned once per session
4. **Validation**: All required fields must be scanned before saving
5. **Saving**: Press 's' to save when all required fields are complete
6. **Reset**: Press 'r' to clear and start a new scan

## Output Format

Saved to `outputs/scan_{workstation_id}_{timestamp}.json`:

```json
{
  "workstation_id": "workstation_01",
  "timestamp": "2024-01-15T10:30:45.123456",
  "barcodes": [
    {"name": "part_number", "value": "PN-12345"},
    {"name": "serial_number", "value": "SN-67890"},
    {"name": "batch_id", "value": "BATCH-2024-01"}
  ]
}
```

## Creating New Workstations

1. Create a new config file: `data/config/workstation_03.json`
2. Define the barcode fields needed for that workstation
3. Launch the scanner for the intended workstation via the Camera entrypoint
4. Run the scanner

## Example Workstations

### Workstation 01 - Assembly
- part_number (required)
- serial_number (required)
- batch_id (optional)

### Workstation 02 - Quality Control
- product_id (required)
- operator_id (required)
- quality_check (required)
- notes (optional)
