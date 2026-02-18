# Appendix TE — Test Execution Records

> **Project Name:** AIBI CV for Manufacturing
> **Document Version:** 2.0
> **Last Updated:** 2025-12-03

---

## Automated Test Execution Records

---

### TC-SFR1-AUTO-01 — QR Detection on Static Test Image

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR1-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy, cv2.QRCodeDetector |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Mock `cv2.QRCodeDetector` with 3 known QR codes.
2. Call `AdvancedScanner.decode_qr()` with test image (200×200).
3. Verify return count equals 3 detections.
4. Compare decoded payloads: `["part_number:PN-001", "serial_number:SN-002", "batch_id:BATCH-003"]`.
5. Assert all payloads match expected values exactly.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-12 | `AdvancedScanner.decode_qr` method not found | FAIL | `decode_qr` static method not implemented in `AdvancedScanner` | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | Mock detector setup returning None values | FAIL | Mock configuration for `cv2.QRCodeDetector` returning None | 2025-11-30 by Nathan |
| 3 | Nathan | 2025-11-30 | Single QR detection working correctly | PASS | — | — |
| 4 | Nathan | 2025-12-01 | `test_single_qr_detection` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. SFR1 QR detection tests passing after implementing `decode_qr` method and fixing mock configuration.

---

### TC-SFR2-AUTO-01 — Field Mapping Logic

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR2-AUTO-01 |
| **Testing Tools Used** | pytest, ConfigManager, WorkstationConfig, BarcodeField |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create `WorkstationConfig` with `part_number` and `serial_number` fields.
2. Process decoded QR list: `["part_number:PN-12345", "serial_number:SN-67890"]`.
3. Execute `AdvancedScanner.parse_barcode()` for field mapping.
4. Verify `mapped_data` contains correct field-value pairs.
5. Assert `part_number="PN-12345"` and `serial_number="SN-67890"`.
6. Confirm no unmapped fields exist.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | `parse_barcode` method not implemented | FAIL | `parse_barcode` static method missing from `AdvancedScanner` | 2025-11-24 by Jacob |
| 2 | Nathan | 2025-11-24 | Field mapping logic working for colon format | PASS | — | — |
| 3 | Collin | 2025-12-01 | `test_parse_colon_format` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR2 field mapping tests passing — colon and JSON formats working correctly.

---

### TC-SFR4-AUTO-01 — JSON Builder Output

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR4-AUTO-01 |
| **Testing Tools Used** | pytest, json module, datetime |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create scan data with `workstation_id`, `timestamp`, and barcode data.
2. Build JSON object with `workstation_id="workstation_01"` and barcodes array.
3. Verify single JSON object with required schema fields.
4. Validate presence of `workstation_id`, `timestamp`, `barcodes` fields.
5. Assert JSON is serializable using `json.dumps()`.
6. Confirm metadata integrity and structure compliance.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | JSON output missing required schema fields | FAIL | JSON schema definition incomplete with missing required fields | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Schema validation failing on data types | FAIL | Data type validation logic error in JSON builder | 2025-11-30 by Jacob |
| 3 | Jacob | 2025-11-30 | JSON structure matches expected schema | PASS | — | — |
| 4 | Jacob | 2025-12-01 | `test_build_complete_scan_json` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. SFR4 JSON builder working correctly after schema definition and data type fixes.

---

### TC-SFR5-AUTO-01 — Keystroke Sequence Builder

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR5-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create scan payload: `{"part_number": "PN-12345", "serial_number": "SN-67890"}`.
2. Set `field_order` and `delimiter="TAB"` configuration.
3. Execute keystroke sequence builder logic.
4. Capture sequence: `["PN-12345", "TAB", "SN-67890", "TAB", "ENTER"]`.
5. Compare against expected pattern with TAB delimiters.
6. Assert correct delimiter insertion between fields.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | Keyboard emulation logic not implemented | FAIL | Keystroke sequence generation logic not implemented | 2025-11-24 by Collin |
| 2 | Daniel | 2025-11-24 | Keystroke sequence with TAB delimiters working | PASS | — | — |
| 3 | Jacob | 2025-12-01 | `test_keystroke_sequence_generation` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR5 keystroke sequence generation working correctly with TAB delimiters.

---

### TC-SFR11-AUTO-01 — JSON Schema Validation and Persistence

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR11-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, mock_open, json |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create event: `{"workstation_id": "workstation_01", "barcodes": [{"name": "part_number", "value": "PN-12345"}]}`.
2. Mock file operations with save/load cycle.
3. Add audit metadata: `saved_at`, `file_version` during save.
4. Execute load operation and parse JSON data.
5. Compare core data integrity: `workstation_id`, `barcodes` match.
6. Verify audit metadata (`saved_at`, `file_version`) present.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-12 | File persistence methods not implemented | FAIL | `save_event` and `load_event` methods missing | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | Mock file operations not working correctly | FAIL | `mock_open` configuration error in test setup | 2025-11-30 by Daniel |
| 3 | Daniel | 2025-11-30 | Audit metadata not being added to saved events | FAIL | Audit metadata (`saved_at`, `file_version`) not implemented | 2025-12-01 by Daniel |
| 4 | Daniel | 2025-12-01 | `test_save_and_load_event` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. SFR11 persistence and schema validation working after implementing save/load methods, fixing mock configuration, and adding audit metadata.

---

### TC-SFR12-AUTO-01 — Schema Compliance Across Workflows

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR12-AUTO-01 |
| **Testing Tools Used** | pytest, json validation |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Generate outputs from manufacturing and quality workflows.
2. Validate required fields: `workstation_id`, `timestamp`, `barcodes`.
3. Check data types: `workstation_id` (str), `timestamp` (str), `barcodes` (list).
4. Verify barcode structure: each has `"name"` and `"value"` fields.
5. Assert all workflow outputs pass schema validation.
6. Confirm no missing required fields in any output.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | Schema validation logic not implemented | FAIL | JSON schema validation functions missing | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Data type validation failing for barcodes array | FAIL | Data type checking logic error for barcode objects | 2025-11-30 by Jacob |
| 3 | Nathan | 2025-11-30 | Schema validation working for all workflows | PASS | — | — |
| 4 | Nathan | 2025-12-01 | `test_scan_json_schema_compliance` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. SFR12 schema validation working correctly after implementing validation functions and fixing data type checking.

---

### TC-SFR15-AUTO-01 — Multi-Code Detection Accuracy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR15-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Mock 5 ground truth QR codes: `["code_1", "code_2", "code_3", "code_4", "code_5"]`.
2. Execute `AdvancedScanner.decode_qr()` on 250×250 test image.
3. Count detected codes and verify all 5 codes found.
4. Compare detected set against ground truth set.
5. Assert error rate ≤ 1% specification threshold.
6. Confirm no false positives in detection output.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-12 | Multi-code detection missing codes in mock | FAIL | Mock setup for `detectAndDecodeMulti` not configured properly | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | All 5 ground truth codes detected correctly | PASS | — | — |
| 3 | Jacob | 2025-12-01 | `test_no_missed_codes` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR15 multi-code detection achieving 0% error rate after fixing mock configuration.

---

### TC-SFR16-AUTO-01 — Output Deduplication

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR16-AUTO-01 |
| **Testing Tools Used** | pytest, numpy, set-based deduplication |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create raw detections with duplicates: 3 detections including 1 duplicate.
2. Process through deduplication logic using set operations.
3. Count unique entries in final output.
4. Verify count equals 2 (original 3 minus 1 duplicate).
5. Check final output contains no duplicate QR codes.
6. Assert `unique_detections` contains only `["part_number:PN-001", "serial_number:SN-002"]`.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | Deduplication logic not implemented | FAIL | Duplicate detection removal logic missing | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | Set operations not removing duplicates correctly | FAIL | Set-based deduplication algorithm error | 2025-11-30 by Collin |
| 3 | Collin | 2025-11-30 | Deduplication still allowing some duplicates | FAIL | Remaining edge cases in deduplication logic | 2025-12-01 by Collin |
| 4 | Collin | 2025-12-01 | `test_no_duplicate_outputs` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. SFR16 deduplication working correctly after resolving set operation errors and edge cases.

---

### TC-SFR17-AUTO-01 — Simulation Frame Injection

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR17-AUTO-01 |
| **Testing Tools Used** | pytest, numpy, simulation framework |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Create 50-frame sequence using numpy arrays.
2. Define injection config: `{10: "part_number:PN-SIM-001", 25: "serial_number:SN-SIM-002", 40: "batch_id:BATCH-SIM-003"}`.
3. Execute simulation with synthetic QR injection at specified frames.
4. Process frames and record detection timing.
5. Verify codes detected at frames 10, 25, 40 exactly.
6. Assert detection timing matches injection configuration.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-12 | Simulation injection framework not implemented | FAIL | Synthetic QR injection logic not implemented | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | Frame timing not matching injection config | FAIL | Frame number to injection mapping error | 2025-11-30 by Nathan |
| 3 | Collin | 2025-11-30 | Injection timing working correctly | PASS | — | — |
| 4 | Collin | 2025-12-01 | `test_synthetic_qr_injection` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. SFR17 simulation frame injection working correctly after implementing injection logic and fixing frame timing.

---

### TC-SFR18-AUTO-01 — Simulation Keyboard Pipeline

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR18-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock (keyboard library) |
| **Testing Type** | Automated Unit Test |

**Execution Steps:**
1. Generate events: `[{"field": "part_number", "value": "PN-SIM-123"}, {"field": "serial_number", "value": "SN-SIM-456"}]`.
2. Mock `keyboard.write` and `keyboard.press_and_release` functions.
3. Process through keyboard-emulation pipeline.
4. Capture keystroke log: `["PN-SIM-123", "TAB", "SN-SIM-456", "TAB", "ENTER"]`.
5. Compare against expected sequence with TAB delimiters.
6. Assert mock call counts: `write=2`, `press_and_release=3`.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | Simulation keyboard pipeline not implemented | FAIL | Simulation keystroke flow logic missing | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Mock call counts not matching expected values | FAIL | Mock keyboard call count validation error | 2025-11-30 by Jacob |
| 3 | Jacob | 2025-11-30 | Keystroke sequence validation logic incorrect | FAIL | Sequence validation logic error in test | 2025-12-01 by Jacob |
| 4 | Jacob | 2025-12-01 | `test_simulation_keystroke_flow` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. SFR18 simulation keyboard pipeline working correctly after implementing keystroke flow logic and fixing validation errors.

---

### TC-PPSR2-AUTO-01 — Detection Latency Under Load

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR2-AUTO-01 |
| **Testing Tools Used** | pytest, time.perf_counter, numpy |
| **Testing Type** | Automated Performance Test |

**Execution Steps:**
1. Create 640×480 test image using numpy (white image).
2. Prepare scan input for `AdvancedScanner.decode_qr()`.
3. Execute scan operation with timing measurement.
4. Measure latency using `time.perf_counter()` in milliseconds.
5. Verify latency < 200 ms performance threshold.
6. Assert latency meets real-time processing requirement.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | Detection latency measured at 520 ms | FAIL | QR detection algorithm performance too slow | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Latency improved to 310 ms but still over threshold | FAIL | Processing pipeline still needs optimization | 2025-11-30 by Jacob |
| 3 | Daniel | 2025-11-30 | Latency optimized to 45 ms, under threshold | PASS | — | — |
| 4 | Daniel | 2025-12-01 | `test_detection_latency_threshold` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. PPSR2 latency performance meeting < 200 ms threshold after pipeline optimization (520 ms → 310 ms → 45 ms).

---

### TC-PPSR5-AUTO-01 — 720p Detection Accuracy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR5-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy (720×1280 images) |
| **Testing Type** | Automated Performance Test |

**Execution Steps:**
1. Create 720p dataset (720×1280) with 100 test cases.
2. Mock 95% success rate through `detectAndDecodeMulti`.
3. Execute `AdvancedScanner.decode_qr()` on all test images.
4. Calculate accuracy: successes/total = 95/100 = 95%.
5. Verify accuracy ≥ 95% threshold requirement.
6. Assert error rate ≤ 1% meets specification.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-12 | Detection accuracy only 70% on 720p test cases | FAIL | Detection algorithm not optimized for 720p resolution | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | Accuracy improved to 85%, still below 95% threshold | FAIL | Detection parameters need further tuning | 2025-11-30 by Daniel |
| 3 | Daniel | 2025-11-30 | 90% accuracy achieved, close but not meeting spec | FAIL | Final optimization needed to reach 95% target | 2025-12-01 by Daniel |
| 4 | Daniel | 2025-12-01 | `test_detection_accuracy_target` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. PPSR5 detection accuracy meeting ≥ 95% threshold after iterative optimization (70% → 85% → 90% → 95%).

---

### TC-PDSR1-AUTO-01 — Local-Only Endpoint Verification

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR1-AUTO-01 |
| **Testing Tools Used** | pytest, pattern matching, config inspection |
| **Testing Type** | Automated Security/Compliance Test |

**Execution Steps:**
1. Load config data: `{"database_url": "sqlite:///./data/scans.db", "output_directory": "./outputs"}`.
2. Check for external patterns: `["http://", "https://", ".com", ".net", ".org"]`.
3. Verify local patterns: `["./", "sqlite:///", "file://"]` or numeric values.
4. Assert no external endpoints in any configuration values.
5. Confirm all storage paths are local-only.
6. Validate compliance with local data storage requirement.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | External URL pattern detected in config values | FAIL | External URL references found in configuration | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | Still detecting `.com` patterns in config | FAIL | Pattern matching producing false positives | 2025-11-30 by Collin |
| 3 | Collin | 2025-11-30 | Pattern matching rejecting valid local paths | FAIL | Pattern matching logic error for local paths | 2025-12-01 by Collin |
| 4 | Collin | 2025-12-01 | `test_local_endpoints_only` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. PDSR1 local-only compliance achieved after removing external URL references and fixing pattern matching logic.

---

### TC-PDSR2-AUTO-01 — No Cloud Dependencies in Code

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR2-AUTO-01 |
| **Testing Tools Used** | pytest, module inspection, pattern matching |
| **Testing Type** | Automated Security/Compliance Test |

**Execution Steps:**
1. Import `aibi_cv.advanced_scanner` module for analysis.
2. Search for prohibited patterns: `["aws", "azure", "gcp", "boto3", "requests.post"]`.
3. Inspect module dictionary and source for cloud API references.
4. Verify no cloud service patterns in module source.
5. Assert no prohibited cloud API patterns found.
6. Validate local-only processing compliance.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-12 | Found `requests` import in `advanced_scanner` module | FAIL | Requests and cloud API imports found in module | 2025-11-24 by Daniel |
| 2 | Jacob | 2025-11-24 | No prohibited cloud imports detected | PASS | — | — |
| 3 | Nathan | 2025-12-01 | `test_no_external_api_calls` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PDSR2 no cloud API dependencies found in codebase after removing the `requests` import.

---

### TC-PDSR4-AUTO-01 — Long-Duration Stability

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR4-AUTO-01 |
| **Testing Tools Used** | pytest, simulation framework, stability monitoring |
| **Testing Type** | Automated Stability/Endurance Test |

**Execution Steps:**
1. Initialize continuous scanning simulation loop.
2. Start extended scan simulation (8–24 hours).
3. Monitor for exceptions, crashes, or memory leaks during operation.
4. Track system resource usage and error rates.
5. Analyze stability metrics for memory leaks or performance degradation.
6. Assert stable operation with no crashes throughout test duration.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | System crashed after 2 hours of continuous operation | FAIL | Memory management and exception handling issues | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Memory leak detected after 6 hours | FAIL | Resource cleanup not implemented properly | 2025-11-30 by Jacob |
| 3 | Daniel | 2025-11-30 | 8-hour stability test completed successfully | PASS | — | — |
| 4 | Daniel | 2025-12-01 | 24-hour endurance test passed | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. PDSR4 long-duration stability achieved after fixing memory management issues and implementing proper resource cleanup.

---

### TC-ODSR1-AUTO-01 — Approved Dependencies Only

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-ODSR1-AUTO-01 |
| **Testing Tools Used** | pytest, sys.modules inspection, dependency validation |
| **Testing Type** | Automated Compliance Test |

**Execution Steps:**
1. Inspect `sys.modules` for loaded dependencies.
2. Compare against approved list: `{"opencv-python", "numpy", "pytest", "keyboard", "pyzbar"}`.
3. Check for prohibited commercial libraries with commercial indicators.
4. Verify no unauthorized dependencies in loaded modules.
5. Validate open-source license compliance.
6. Assert all libraries are approved for use.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-11 | Unauthorized commercial library found in dependencies | FAIL | Unauthorized commercial library in dependency list | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | Commercial indicators still present in module names | FAIL | Commercial library references still present | 2025-11-30 by Nathan |
| 3 | Nathan | 2025-11-30 | License validation logic not working correctly | FAIL | License validation algorithm error | 2025-12-01 by Nathan |
| 4 | Nathan | 2025-12-01 | `test_approved_dependencies_only` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. ODSR1 dependency compliance achieved after removing unauthorized libraries and fixing validation logic.

---

### TC-OOSR4-AUTO-01 — Legacy Data Import Parsing

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-OOSR4-AUTO-01 |
| **Testing Tools Used** | pytest, json module, ConfigManager |
| **Testing Type** | Automated Integration Test |

**Execution Steps:**
1. Create test JSON files with legacy `WorkstationConfig` format.
2. Execute `ConfigManager.load_config()` and JSON parsing functions.
3. Verify data loads without parsing errors or exceptions.
4. Validate parsed `WorkstationConfig` structure and `BarcodeField` objects.
5. Check data integrity: `workstation_id`, `barcode_fields`, `camera_index`.
6. Assert successful parsing of legacy configuration formats.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-12 | JSON parsing throwing exceptions on legacy format | FAIL | Legacy JSON format support not implemented | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | Config structure validation rejecting valid configs | FAIL | `WorkstationConfig` validation logic error | 2025-11-30 by Nathan |
| 3 | Collin | 2025-11-30 | Legacy parser working correctly | PASS | — | — |
| 4 | Collin | 2025-12-01 | All legacy JSON formats parsing successfully | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. OOSR4 legacy data import working correctly after implementing legacy format support and fixing validation logic.

---

### TC-EISR3-AUTO-01 — Interoperability Schema Validation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR3-AUTO-01 |
| **Testing Tools Used** | pytest, datetime.fromisoformat, json validation |
| **Testing Type** | Automated Integration Test |

**Execution Steps:**
1. Generate outputs from manufacturing and quality workflows.
2. Validate EISR fields: `workstation_id`, `timestamp`, `barcodes`, `schema_version`.
3. Check timestamp format compliance using `datetime.fromisoformat()`.
4. Verify barcode structure: each dict has `"name"` and `"value"` fields.
5. Validate interoperability schema compliance across workflows.
6. Assert all workflow outputs pass EISR validation requirements.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | EISR schema validation logic not implemented | FAIL | EISR schema validation logic missing | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | Timestamp format not ISO 8601 compliant | FAIL | Timestamp format generation not ISO 8601 compliant | 2025-11-30 by Collin |
| 3 | Collin | 2025-11-30 | Barcode structure missing required fields | FAIL | Barcode object structure validation missing fields | 2025-12-01 by Collin |
| 4 | Collin | 2025-12-01 | `test_interoperability_schema_validation` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. EISR3 interoperability schema compliance achieved after implementing validation logic, fixing ISO 8601 timestamps, and correcting barcode structure.

---

### TC-EISR5-AUTO-01 — Automated MES/ERP Export

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR5-AUTO-01 |
| **Testing Tools Used** | pytest, mock MES/ERP validation |
| **Testing Type** | Automated Integration Test |

**Execution Steps:**
1. Create MES payload: `{"source_system": "AIBI_CV_Scanner", "workstation_id": "workstation_01", "scan_data": {...}}`.
2. Validate payload structure with required MES/ERP fields.
3. Check field correctness: `source_system`, `workstation_id`, `timestamp`, `scan_data`.
4. Verify data types and `scan_data` dictionary structure.
5. Simulate payload acceptance by mock MES/ERP system.
6. Assert export payload meets MES/ERP integration requirements.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | MES payload missing required fields | FAIL | Required MES/ERP payload fields missing | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Field validation rejecting valid data types | FAIL | MES payload field validation logic error | 2025-11-30 by Jacob |
| 3 | Daniel | 2025-11-30 | MES payload structure meets requirements | PASS | — | — |
| 4 | Daniel | 2025-12-01 | `test_mes_payload_structure` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. EISR5 MES/ERP export integration working correctly after adding required payload fields and fixing validation logic.

---

### TC-EISR6-AUTO-01 — Config-Driven Workflow Behavior

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR6-AUTO-01 |
| **Testing Tools Used** | pytest, ConfigManager, WorkstationConfig |
| **Testing Type** | Automated Integration Test |

**Execution Steps:**
1. Create manufacturing config: `part_number`, `serial_number` required.
2. Create quality config: `part_number`, `batch_id`, `inspector_id` required.
3. Process identical scan sequence: `["part_number:PN-001", "serial_number:SN-002", "batch_id:BATCH-003"]`.
4. Analyze required field differences and completion states.
5. Verify config1 != config2 required fields and different completion results.
6. Assert configs produce different, correct workflow behaviors.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | Config differences not affecting workflow behavior | FAIL | Config-driven workflow logic not implemented | 2025-11-24 by Collin |
| 2 | Nathan | 2025-11-24 | Required field logic not working correctly | FAIL | Required field validation logic error | 2025-11-30 by Nathan |
| 3 | Jacob | 2025-11-30 | Completion state validation logic incorrect | FAIL | Workflow completion state checking logic error | 2025-12-01 by Jacob |
| 4 | Daniel | 2025-12-01 | `test_different_config_workflows` PASSED | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 25%. EISR6 config-driven workflow behavior working correctly after implementing config logic, fixing field validation, and correcting completion state checks.

---

## Manual Test Execution Records

---

### TC-SFR1-MAN-01 — Live QR Code Detection

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR1-MAN-01 |
| **Testing Tools Used** | Live camera, printed QR codes, system UI |
| **Testing Type** | Manual Integration Test |

**Execution Steps:**
1. Set up live camera with 720p resolution.
2. Place printed QR codes in camera field of view.
3. Launch AIBI CV scanner application.
4. Observe real-time detection in UI.
5. Verify all visible QR codes are detected and displayed.
6. Count detected codes against physically visible codes.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | Only 1 of 3 QR codes detected | FAIL | Camera focus calibration issue | 2025-11-20 by Nathan |
| 2 | Nathan | 2025-11-28 | All 3 QR codes detected correctly | PASS | — | — |
| 3 | Jacob | 2025-12-01 | Consistent detection across multiple tests | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR1 live camera detection working reliably after hardware calibration adjustment.

---

### TC-SFR2-MAN-01 — Field Mapping Configuration

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR2-MAN-01 |
| **Testing Tools Used** | Configuration UI, printed test QR codes |
| **Testing Type** | Manual Configuration Test |

**Execution Steps:**
1. Access workstation configuration interface.
2. Define field mapping: `part_number`, `serial_number`, `batch_id`.
3. Print test QR codes with known values.
4. Scan codes and verify field assignment in output.
5. Check that values appear in correct JSON fields.
6. Validate no field mismatches occur.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-15 | Configuration UI missing | FAIL | UI component not implemented | 2025-11-22 by Collin |
| 2 | Collin | 2025-11-28 | Fields mapped to correct JSON structure | PASS | — | — |
| 3 | Daniel | 2025-12-01 | All field assignments working correctly | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR2 field mapping configuration functional after implementing the configuration UI component.

---

### TC-SFR4-MAN-01 — JSON Record Generation from Live Scan

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR4-MAN-01 |
| **Testing Tools Used** | Live scanner, file system monitor |
| **Testing Type** | Manual Integration Test |

**Execution Steps:**
1. Perform live scan with multiple QR codes.
2. Monitor outputs directory for JSON file creation.
3. Open generated JSON file and validate structure.
4. Verify presence of `workstation_id`, `timestamp`, `barcodes` array.
5. Check that all scanned data appears in correct format.
6. Confirm metadata integrity and completeness.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-15 | JSON structure invalid, missing required fields | FAIL | JSON schema validation error | 2025-11-18 by Jacob |
| 2 | Jacob | 2025-11-28 | Valid JSON but timestamp field missing | FAIL | Timestamp generation bug | 2025-11-29 by Jacob |
| 3 | Jacob | 2025-12-01 | Complete JSON with all required fields | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 33%. SFR4 JSON generation working correctly after fixing schema definition and timestamp generation.

---

### TC-SFR5-MAN-01 — Keyboard Emulation Output

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR5-MAN-01 |
| **Testing Tools Used** | Live scanner, Notepad application, keyboard monitoring |
| **Testing Type** | Manual Integration Test |

**Execution Steps:**
1. Open Notepad and position cursor in text field.
2. Configure scanner for keyboard emulation mode.
3. Perform live scan with test QR codes.
4. Observe keystroke output in Notepad.
5. Verify correct sequence: value1 → TAB → value2 → TAB → ENTER.
6. Check for accurate data transmission.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-15 | No keystroke output to target application | FAIL | Keyboard library not initialized | 2025-11-19 by Daniel |
| 2 | Daniel | 2025-11-28 | Correct keystroke sequence generated | PASS | — | — |
| 3 | Nathan | 2025-12-01 | TAB delimiters and ENTER working properly | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR5 keyboard emulation functional after initializing the keyboard library.

---

### TC-SFR11-MAN-01 — Offline Persistence and Replay

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR11-MAN-01 |
| **Testing Tools Used** | Live scanner, network disconnect simulation |
| **Testing Type** | Manual Persistence Test |

**Execution Steps:**
1. Disconnect network/downstream system.
2. Perform multiple scan operations while offline.
3. Verify scans are queued/stored locally.
4. Reconnect network/downstream system.
5. Observe automatic replay of queued events.
6. Confirm no data loss or duplicates.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-15 | Scans lost when network disconnected | FAIL | No offline storage mechanism | 2025-11-17 by Collin |
| 2 | Collin | 2025-11-28 | Queue created but data not replaying | FAIL | Replay trigger not working | 2025-11-30 by Collin |
| 3 | Collin | 2025-12-01 | All offline scans replayed successfully | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 33%. SFR11 offline persistence working after implementing the queue mechanism and fixing the replay trigger.

---

### TC-SFR12-MAN-01 — Schema-Documentation Consistency

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR12-MAN-01 |
| **Testing Tools Used** | Documentation review, JSON schema files, sample outputs |
| **Testing Type** | Manual Documentation Test |

**Execution Steps:**
1. Review JSON schema documentation.
2. Generate sample outputs from live system.
3. Validate outputs against documented schema.
4. Check for consistency between docs and implementation.
5. Verify all required fields are documented.
6. Confirm schema version matches implementation.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | Schema docs don't match implementation | FAIL | Documentation version mismatch | 2025-11-16 by Nathan |
| 2 | Jacob | 2025-11-28 | Documentation updated and consistent | PASS | — | — |
| 3 | Daniel | 2025-12-01 | Schema and output fully aligned | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR12 documentation-schema consistency achieved after updating documentation to match the current implementation.

---

### TC-SFR15-MAN-01 — Multi-Code Decoding Under Factory Lighting

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR15-MAN-01 |
| **Testing Tools Used** | Multi-code test sheet, live camera, typical factory lighting |
| **Testing Type** | Manual Detection Test |

**Execution Steps:**
1. Print test sheet with 5 different QR codes.
2. Set up typical factory lighting conditions.
3. Position test sheet in camera field of view.
4. Run live detection and count successful decodes.
5. Verify all 5 codes are detected consistently.
6. Test under various lighting angles.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-15 | Only 3 of 5 QR codes detected under factory lighting | FAIL | Low light detection threshold too high | 2025-11-21 by Collin |
| 2 | Collin | 2025-11-28 | All 5 codes detected consistently | PASS | — | — |
| 3 | Nathan | 2025-12-01 | Reliable detection across lighting conditions | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR15 multi-code detection reliable under factory conditions after adjusting the light detection threshold.

---

### TC-SFR16-MAN-01 — Complete Output for All Visible QR Codes

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR16-MAN-01 |
| **Testing Tools Used** | Live scanner, multiple QR codes, output verification |
| **Testing Type** | Manual Output Verification Test |

**Execution Steps:**
1. Arrange multiple QR codes in camera view.
2. Perform live scan operation.
3. Count physical QR codes visible to camera.
4. Check output JSON for number of detected codes.
5. Verify output count matches visible count.
6. Confirm no codes are missed or duplicated.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-15 | Output shows 2 codes when 3 visible | FAIL | Detection area boundary issue | 2025-11-17 by Jacob |
| 2 | Jacob | 2025-11-28 | Output contains duplicate entries | FAIL | Duplicate filtering not implemented | 2025-11-29 by Jacob |
| 3 | Jacob | 2025-12-01 | Output count matches visible codes exactly | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 33%. SFR16 output accuracy achieved after fixing detection area boundaries and implementing duplicate filtering.

---

### TC-SFR17-MAN-01 — Simulation Mode Execution

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR17-MAN-01 |
| **Testing Tools Used** | Simulation UI, recorded video footage, developer tools |
| **Testing Type** | Manual Simulation Test |

**Execution Steps:**
1. Launch simulation mode interface.
2. Load recorded video footage with known QR codes.
3. Configure synthetic QR injection parameters.
4. Run simulation and observe detection behavior.
5. Verify simulation results match expected outcomes.
6. Check simulation logs for accuracy.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-15 | Simulation interface not available | FAIL | Simulation UI components not developed | 2025-11-22 by Daniel |
| 2 | Daniel | 2025-11-28 | Simulation executing with expected results | PASS | — | — |
| 3 | Collin | 2025-12-01 | Simulation behavior matches live system | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. SFR17 simulation functionality working correctly after implementing the simulation UI components.

---

### TC-SFR18-MAN-01 — Simulation Keyboard Emulation Output

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR18-MAN-01 |
| **Testing Tools Used** | Simulation mode, text editor, keyboard monitoring |
| **Testing Type** | Manual Simulation Integration Test |

**Execution Steps:**
1. Enable simulation mode with keyboard emulation.
2. Open text editor for keystroke capture.
3. Run simulation with known test data.
4. Observe keystroke output in text editor.
5. Verify correct sequence and formatting.
6. Confirm simulation matches live behavior.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | No keystroke output in simulation mode | FAIL | Keyboard emulation not integrated with simulation | 2025-11-22 by Nathan |
| 2 | Nathan | 2025-11-28 | Keystrokes generated in wrong order | FAIL | Keystroke sequence logic error | 2025-11-30 by Nathan |
| 3 | Nathan | 2025-12-01 | Correct keystroke sequence in simulation | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 33%. SFR18 simulation keyboard emulation functional after integrating keyboard emulation with the simulation pipeline and fixing sequence logic.

---

### TC-PUSR1-MAN-01 — New Operator Onboarding Time

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR1-MAN-01 |
| **Testing Tools Used** | New operator, system UI, stopwatch, task checklist |
| **Testing Type** | Manual Usability Test |

**Execution Steps:**
1. Select operator with no prior system experience.
2. Provide basic system overview (5 minutes max).
3. Start timer and begin basic workflow tasks.
4. Monitor operator progress without assistance.
5. Record completion time and error count.
6. Verify completion within 30-minute requirement.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-16 | New operator took 45 minutes to complete tasks | FAIL | UI workflow too complex; added guided tutorial | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-29 | Operator completed workflow in 25 minutes | PASS | — | — |
| 3 | Collin | 2025-12-02 | Different operator finished in 22 minutes | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PUSR1 usability target (≤ 30 min) met after simplifying the UI workflow and adding a guided tutorial.

---

### TC-PUSR2-MAN-01 — UI Tooltip and Guidance Effectiveness

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR2-MAN-01 |
| **Testing Tools Used** | System UI, test users, usability questionnaire |
| **Testing Type** | Manual Usability Test |

**Execution Steps:**
1. Present system UI to test users.
2. Ask users to identify major controls and functions.
3. Evaluate tooltip effectiveness and clarity.
4. Test icon recognition without text labels.
5. Assess overall UI intuitiveness.
6. Record user feedback and success rates.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-16 | Users misidentified 60% of status icons | FAIL | Redesigned icons and improved color contrast | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-29 | 85% correct identification with tooltips | PASS | — | — |
| 3 | Nathan | 2025-12-02 | 95% accurate state recognition | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PUSR2 UI guidance working effectively (95% accuracy) after redesigning icons and improving tooltip clarity.

---

### TC-PUSR3-MAN-01 — Workflow Step Reduction vs. Legacy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR3-MAN-01 |
| **Testing Tools Used** | Legacy system, new system, workflow comparison sheet |
| **Testing Type** | Manual Workflow Comparison Test |

**Execution Steps:**
1. Document current legacy workflow steps.
2. Perform same task using new system.
3. Count manual input steps for each system.
4. Compare time required for task completion.
5. Evaluate reduction in repetitive actions.
6. Verify new system requires fewer steps.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-16 | New system: 8 steps vs. Legacy: 12 steps | PASS | — | — |
| 2 | Jacob | 2025-11-29 | 33% reduction in manual input steps | PASS | — | — |
| 3 | Daniel | 2025-12-02 | Workflow completion time reduced by 40% | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 100%. PUSR3 workflow improvement validated — new system achieves 33% step reduction and 40% time reduction vs. the legacy workflow.

---

### TC-PUSR4-MAN-01 — Touch-Free Operation During Normal Workflow

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR4-MAN-01 |
| **Testing Tools Used** | Live system, operator observation, touch interaction counter |
| **Testing Type** | Manual Touch-Free Operation Test |

**Execution Steps:**
1. Observe operator during typical work cycle.
2. Count number of UI touches/interactions required.
3. Monitor automatic detection and processing.
4. Verify minimal manual intervention needed.
5. Assess hands-free operation effectiveness.
6. Record touch frequency per cycle.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-16 | Operator required 8+ UI interactions per cycle | FAIL | Increased automation and reduced manual steps | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-29 | Reduced to 3 interactions per cycle | PASS | — | — |
| 3 | Jacob | 2025-12-02 | Average 1.5 touches per cycle achieved | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PUSR4 touch-free operation achieved (1.5 avg interactions/cycle) after increasing automation and reducing manual steps.

---

### TC-PUSR5-MAN-01 — Auto-Fill of Repetitive Fields

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR5-MAN-01 |
| **Testing Tools Used** | Live system, consecutive job simulation, auto-fill monitoring |
| **Testing Type** | Manual Automation Test |

**Execution Steps:**
1. Configure system for consecutive similar jobs.
2. Perform first job with full manual input.
3. Execute subsequent jobs and monitor auto-fill.
4. Verify common fields are automatically populated.
5. Check accuracy of auto-filled data.
6. Assess reduction in repetitive input.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-16 | All fields require manual entry each time | FAIL | Implemented auto-fill for common field values | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-29 | Auto-fill working for workstation and batch fields | PASS | — | — |
| 3 | Daniel | 2025-12-02 | 70% reduction in repetitive data entry | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PUSR5 auto-fill functionality reducing manual input by 70% after implementing common field auto-population.

---

### TC-PUSR10-MAN-01 — Icon and Color State Recognition

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR10-MAN-01 |
| **Testing Tools Used** | UI screenshots, test users, icon recognition test |
| **Testing Type** | Manual Visual Design Test |

**Execution Steps:**
1. Prepare screenshots of system status indicators.
2. Present to users without text explanations.
3. Ask users to identify system states (OK/warning/error).
4. Test color-coding effectiveness.
5. Evaluate icon clarity and recognition.
6. Record accuracy of state identification.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-16 | Users misidentifying error states as warnings | FAIL | Improved color coding and icon design | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-29 | Color coding improved, 90% accuracy | PASS | — | — |
| 3 | Nathan | 2025-12-02 | 95% accurate state identification achieved | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PUSR10 visual state indicators effective (95% accuracy) after improving color coding and icon design.

---

### TC-PPSR2-MAN-01 — Real-Time Feedback Perception

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR2-MAN-01 |
| **Testing Tools Used** | Live system, operator feedback, response time monitoring |
| **Testing Type** | Manual Performance Test |

**Execution Steps:**
1. Have operator perform typical scanning tasks.
2. Monitor system response times during operation.
3. Ask operator about perceived delays.
4. Test under normal factory load conditions.
5. Verify "immediate" feedback perception.
6. Record any noticeable delays.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-16 | Operator reported 2–3 second delays | FAIL | Optimized processing pipeline for real-time response | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-29 | Response time under 500 ms, feels immediate | PASS | — | — |
| 3 | Collin | 2025-12-02 | No perceived delays during operation | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PPSR2 real-time performance achieved (< 500 ms response) after optimizing the processing pipeline.

---

### TC-PPSR5-MAN-01 — 720p Camera Hardware Reliability

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR5-MAN-01 |
| **Testing Tools Used** | 720p camera hardware, live testing environment |
| **Testing Type** | Manual Hardware Performance Test |

**Execution Steps:**
1. Set up system with actual 720p camera hardware.
2. Test QR detection accuracy under factory conditions.
3. Compare performance to development environment.
4. Verify no degradation in detection rates.
5. Test various lighting and distance conditions.
6. Record accuracy metrics.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-16 | Detection accuracy dropped to 85% with 720p camera | FAIL | Calibrated detection parameters for 720p resolution | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-29 | 96% accuracy achieved with optimized settings | PASS | — | — |
| 3 | Jacob | 2025-12-02 | Consistent 720p performance across conditions | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PPSR5 720p hardware performance validated (96% accuracy) after calibrating detection parameters for the 720p resolution.

---

### TC-PDSR1-MAN-01 — No Outbound Network Traffic

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR1-MAN-01 |
| **Testing Tools Used** | Network monitoring tools, live system operation |
| **Testing Type** | Manual Security Test |

**Execution Steps:**
1. Set up network traffic monitoring.
2. Run system through complete operational cycle.
3. Monitor all outbound network connections.
4. Verify no external data transmission occurs.
5. Check for any unauthorized network activity.
6. Confirm local-only operation.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-16 | Found telemetry data being sent to external server | FAIL | Removed all external network calls and telemetry | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-29 | No outbound traffic detected during operation | PASS | — | — |
| 3 | Daniel | 2025-12-02 | Local-only operation confirmed over 8-hour test | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PDSR1 local-only operation verified after removing all external network calls and telemetry.

---

### TC-PDSR2-MAN-01 — Fully Offline Operation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR2-MAN-01 |
| **Testing Tools Used** | Network disconnect, live system testing |
| **Testing Type** | Manual Offline Operation Test |

**Execution Steps:**
1. Disconnect system from internet completely.
2. Attempt to run all normal operations.
3. Verify full functionality without network.
4. Test all scanning and processing features.
5. Confirm no degradation in performance.
6. Validate offline operation capability.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-16 | All functions work normally without internet | PASS | — | — |
| 2 | Nathan | 2025-11-29 | No network dependencies detected | PASS | — | — |
| 3 | Collin | 2025-12-02 | Offline operation maintained for 12 hours | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 100%. PDSR2 offline operation validated — full functionality maintained without internet over a 12-hour test period.

---

### TC-PDSR4-MAN-01 — Factory Environment Stability

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR4-MAN-01 |
| **Testing Tools Used** | Factory environment, extended operation monitoring |
| **Testing Type** | Manual Stability Test |

**Execution Steps:**
1. Deploy system in actual factory environment.
2. Run continuous operation for 8+ hours.
3. Monitor for crashes, errors, or performance issues.
4. Test under typical factory conditions (dust, vibration, temperature).
5. Record system stability metrics.
6. Verify acceptable performance throughout test.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-17 | System crashed after 4 hours due to memory leak | FAIL | Fixed memory management and added monitoring | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-30 | 12-hour stable operation achieved | PASS | — | — |
| 3 | Nathan | 2025-12-03 | 24-hour factory deployment successful | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. PDSR4 factory environment stability achieved after fixing memory management issues and adding resource monitoring.

---

### TC-ODSR2-MAN-01 — OSS Component Documentation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-ODSR2-MAN-01 |
| **Testing Tools Used** | Documentation review, dependency analysis tools |
| **Testing Type** | Manual Documentation Test |

**Execution Steps:**
1. Review all project documentation.
2. Identify all open-source components used.
3. Verify each component is properly documented.
4. Check license information is complete.
5. Confirm version numbers are accurate.
6. Validate documentation completeness.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-17 | Missing license info for 3 OSS components | FAIL | Added complete license documentation | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-30 | All OSS components documented with licenses | PASS | — | — |
| 3 | Collin | 2025-12-03 | Documentation complete and up-to-date | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. ODSR2 OSS documentation complete with name, version, and license for all components.

---

### TC-OOSR4-MAN-01 — Legacy Data Import

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-OOSR4-MAN-01 |
| **Testing Tools Used** | Legacy system export files, import functionality |
| **Testing Type** | Manual Data Migration Test |

**Execution Steps:**
1. Obtain actual legacy system export file.
2. Run data import process on real legacy data.
3. Verify all records import correctly.
4. Check data integrity after import.
5. Confirm no manual cleanup required.
6. Validate imported data accuracy.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-17 | Import failed on 15% of legacy records | FAIL | Fixed data format compatibility issues | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-30 | All 500 legacy records imported successfully | PASS | — | — |
| 3 | Daniel | 2025-12-03 | Data integrity validated, no corruption found | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. OOSR4 legacy data import working correctly after resolving format compatibility issues.

---

### TC-EISR4-MAN-01 — JSON Schema Version Control

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR4-MAN-01 |
| **Testing Tools Used** | Repository review, documentation audit, version control |
| **Testing Type** | Manual Documentation Test |

**Execution Steps:**
1. Review repository for JSON schema files.
2. Check version control history for schema changes.
3. Verify documentation matches current schema version.
4. Confirm schema is properly tracked and versioned.
5. Validate documentation completeness.
6. Check for schema-documentation consistency.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-17 | Schema files not under version control | FAIL | Added schema files to git and implemented versioning | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-30 | Schema properly tracked with version tags | PASS | — | — |
| 3 | Jacob | 2025-12-03 | Documentation matches schema v1.2 exactly | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. EISR4 schema version control achieved — schema file tracked in git with documentation matching v1.2.

---

### TC-EISR5-MAN-01 — MES/ERP Export Integration

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR5-MAN-01 |
| **Testing Tools Used** | MES/ERP test instance, live export functionality |
| **Testing Type** | Manual Integration Test |

**Execution Steps:**
1. Set up connection to MES/ERP test instance.
2. Configure export parameters and field mapping.
3. Perform live scan and trigger export.
4. Verify data is received by MES/ERP system.
5. Check field mapping accuracy in received data.
6. Confirm successful integration.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-17 | Connection timeout to MES test server | FAIL | Configured network settings and retry logic | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-30 | Connected but field mapping incorrect | FAIL | Fixed field mapping configuration | 2025-12-01 by Daniel |
| 3 | Daniel | 2025-12-03 | MES integration working, all fields correct | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 33%. EISR5 MES/ERP integration functional after configuring network settings and fixing field mapping.

---

### TC-EISR6-MAN-01 — Config-Driven Workflow Customization

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR6-MAN-01 |
| **Testing Tools Used** | Configuration files, field engineer, test workflow |
| **Testing Type** | Manual Configuration Test |

**Execution Steps:**
1. Have field engineer modify workflow configuration.
2. Change required fields and validation rules.
3. Deploy new configuration without code changes.
4. Test system with modified workflow.
5. Verify new workflow is enforced correctly.
6. Confirm configuration-driven behavior.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-17 | Config changes not reflected in system behavior | FAIL | Implemented dynamic config reload mechanism | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-30 | New workflow enforced after system restart | PASS | — | — |
| 3 | Collin | 2025-12-03 | Field engineer configured 3 workflows successfully | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. EISR6 config-driven workflow customization working correctly after implementing the dynamic config reload mechanism.

---

## Overall Test Execution Summary

| Metric | Value |
|---|---|
| **Total Test Cases** | 46 (26 manual + 20 automated) |
| **Total Executions** | 158 |
| **Final Pass Rate** | 100% (all test cases passing as of final execution) |
| **Average Executions per Test Case** | 3.4 |
| **Test Cases Passing on First Attempt** | 4 (PUSR3, PDSR2-MAN) |
| **Test Cases Requiring 4+ Iterations** | 12 |
| **Unique Defects Found and Resolved** | 42 |
| **Testing Period** | 2025-11-11 through 2025-12-03 |
| **Team Members Involved** | Nathan, Jacob, Collin, Daniel |
