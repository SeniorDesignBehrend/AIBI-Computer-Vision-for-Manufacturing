# Appendix TE — Test Execution Records

> **Project Name:** AIBI CV for Manufacturing
> **Document Version:** 3.0
> **Last Updated:** 2026-02-18

---

## Automated Test Execution Records

---

### TC-SFR1-AUTO-01 — QR Detection on Static Test Image

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR1-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy, cv2.QRCodeDetector |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Mock cv2.QRCodeDetector to return 3 known QR codes (part_number:PN-001, serial_number:SN-002, batch_id:BATCH-003).
2. Create a 200x200 numpy test image.
3. Call AdvancedScanner.decode_qr() with the test image.
4. Assert returned count equals 3.
5. Compare each decoded payload against the ground truth values.
6. Verify no extra or missing entries in the result.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-11 | decode_qr() returned 2 of 3 codes; third QR code payload truncated due to incorrect buffer handling in mock setup | FAIL | Mock did not simulate multi-code return correctly | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | All 3 codes returned with correct payloads after fixing mock to use detectAndDecodeMulti | PASS | — | — |
| 3 | Jacob | 2025-11-30 | All 3 codes returned, payloads match, no extras or missing entries | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Initial mock configuration did not properly simulate multi-code detection; corrected mock to use detectAndDecodeMulti interface and all subsequent runs passed.

---

### TC-SFR5-AUTO-01 — Keystroke Sequence Builder

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR5-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Create a payload dictionary with part_number="PN-12345" and serial_number="SN-67890".
2. Set field_order to [part_number, serial_number] and delimiter to TAB.
3. Execute the keystroke sequence builder function.
4. Capture the output sequence list.
5. Compare against expected sequence: ["PN-12345", "TAB", "SN-67890", "TAB", "ENTER"].

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | Sequence output was ["PN-12345", "SN-67890", "ENTER"] — TAB delimiters missing between fields | FAIL | Builder did not insert delimiter tokens between field values | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Sequence matched expected: ["PN-12345", "TAB", "SN-67890", "TAB", "ENTER"] | PASS | — | — |
| 3 | Collin | 2025-12-01 | Sequence matched expected output exactly | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Initial implementation omitted delimiter insertion between fields; after adding TAB token injection logic all executions passed.

---

### TC-SFR11-AUTO-01 — JSON File Write/Read Integrity

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR11-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, json |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Create scan data with workstation_id="workstation_01" and barcodes=[{"name": "part_number", "value": "PN-001"}].
2. Write the scan data to a JSON file via OutputData.to_json().
3. Read back the saved JSON file using json.load().
4. Compare the loaded workstation_id against the original value.
5. Compare the loaded barcodes list against the original barcodes.
6. Assert exact equality on all fields.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-13 | JSON file written but read-back failed with KeyError on "barcodes" — field was serialized as "barcode_data" instead | FAIL | OutputData.to_json() used internal field name "barcode_data" instead of "barcodes" | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-25 | Write/read cycle completed; workstation_id and barcodes matched exactly | PASS | — | — |
| 3 | Nathan | 2025-12-01 | All fields matched after round-trip write/read | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Field naming inconsistency between internal model and serialized output was fixed; all subsequent integrity checks passed.

---

### TC-SFR14-AUTO-01 — Process Pickle Save/Load Integrity

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR14-AUTO-01 |
| **Testing Tools Used** | pytest, pickle, numpy |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Create a trained process object with 2 steps ("Install Part A", "Tighten Bolts"), each with computed centroid numpy arrays.
2. Call serialize_process() to produce a pickle byte stream.
3. Call deserialize_process() on the byte stream to reconstruct the process.
4. Compare step names and ordering between original and deserialized process.
5. Compare centroid arrays using np.allclose() to verify numerical equality.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-14 | Deserialization raised UnpicklingError — serialize_process() was writing raw dict instead of using pickle.dumps() | FAIL | serialize_process() wrote JSON-style dict, not pickle format | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | Deserialization succeeded but np.allclose() failed — centroid arrays were converted to lists during serialization, losing dtype | FAIL | Numpy arrays were not preserved through pickle; intermediate list conversion introduced float precision loss | 2025-11-25 by Daniel |
| 3 | Daniel | 2025-11-28 | All step names match, order preserved, np.allclose() returns True for all centroid arrays | PASS | — | — |
| 4 | Nathan | 2025-12-02 | Full round-trip integrity confirmed; step names, order, and centroid arrays all match | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Two iterations required: first to fix serialization format from dict to pickle, second to preserve numpy array dtypes through the round-trip. Final executions confirmed full data integrity.

---

### TC-SFR15-AUTO-01 — Multi-Code Detection Accuracy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR15-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Mock 5 ground truth QR codes with known payloads on a 250x250 image.
2. Execute AdvancedScanner.decode_qr() on the mocked image.
3. Count the number of detected codes.
4. Compare each detected payload against the ground truth set.
5. Calculate the error rate (missed + incorrect / total).
6. Assert error rate is less than or equal to 1%.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-12 | Only 4 of 5 codes detected; fifth code at image edge was missed; error rate = 20% | FAIL | decode_qr() did not handle QR codes near image boundaries correctly | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | All 5 codes detected, payloads match, error rate = 0% | PASS | — | — |
| 3 | Jacob | 2025-12-01 | 5 of 5 detected, 0% error rate | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Boundary handling issue in decode_qr() caused one code to be missed initially; after adjusting detection bounds all codes detected with 0% error rate.

---

### TC-SFR16-AUTO-01 — Output Deduplication

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR16-AUTO-01 |
| **Testing Tools Used** | pytest, numpy, set-based dedup |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Create a raw detections list with 3 items, where 1 is a duplicate (same payload as another).
2. Process the raw detections through the deduplication logic.
3. Count the number of unique entries in the result.
4. Assert exactly 2 unique entries remain.
5. Verify the duplicate entry was removed, not the wrong original.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-13 | Dedup returned 3 entries — duplicate was not removed because comparison used object identity instead of value equality | FAIL | Deduplication compared object references, not payload values | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | Dedup returned 2 unique entries; duplicate correctly removed | PASS | — | — |
| 3 | Daniel | 2025-11-30 | 2 unique entries returned, correct items preserved | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Deduplication logic was comparing object identity rather than payload values; switching to value-based comparison fixed the issue.

---

### TC-SFR17-AUTO-01 — Simulation Synthetic QR Generation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR17-AUTO-01 |
| **Testing Tools Used** | pytest, simulation_scanner.py |
| **Testing Type** | Automated Functional |

**Execution Steps:**
1. Import and invoke simulation_scanner scenarios programmatically.
2. Run each simulation scenario to generate synthetic QR codes.
3. Capture the detection results from each scenario.
4. Verify that all expected QR codes were generated and detected.
5. Parse field-value pairs from detected codes and compare against expected data.
6. Assert no exceptions were raised during any simulation run.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-14 | Simulation ran but synthetic QR generation produced blank images — qrcode library not generating valid image matrices | FAIL | simulation_scanner.py used incorrect image format for synthetic QR rendering | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | All scenarios produced valid synthetic QR codes; field-value pairs matched expected data | PASS | — | — |
| 3 | Nathan | 2025-12-02 | All simulation scenarios completed successfully with correct parsed output | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Synthetic QR image generation was producing blank frames due to incorrect image format conversion; after fixing the rendering pipeline all simulation scenarios passed.

---

### TC-PPSR2-AUTO-01 — Detection Latency Under Load

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR2-AUTO-01 |
| **Testing Tools Used** | pytest, time.perf_counter, numpy |
| **Testing Type** | Automated Non-Functional |

**Execution Steps:**
1. Create a 640x480 numpy test image with embedded QR code data.
2. Record start time using time.perf_counter().
3. Execute AdvancedScanner.decode_qr() on the test image.
4. Record end time using time.perf_counter().
5. Calculate elapsed time in milliseconds.
6. Assert elapsed time is less than 200 ms.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-11 | Latency measured at 342 ms — exceeded 200 ms threshold due to redundant image preprocessing step | FAIL | decode_qr() performed unnecessary color space conversion on every call | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | Latency measured at 87 ms after removing redundant preprocessing | PASS | — | — |
| 3 | Collin | 2025-11-30 | Latency measured at 91 ms | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Initial latency exceeded threshold due to redundant image preprocessing; removing unnecessary color conversion brought latency well under 200 ms.

---

### TC-PPSR5-AUTO-01 — 720p Detection Accuracy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR5-AUTO-01 |
| **Testing Tools Used** | pytest, unittest.mock, numpy |
| **Testing Type** | Automated Non-Functional |

**Execution Steps:**
1. Create 100 test cases with 720x1280 resolution images.
2. Mock detectAndDecodeMulti to simulate a 95% success rate across test cases.
3. Execute decode_qr() on all 100 test images.
4. Count successful detections.
5. Calculate overall accuracy percentage.
6. Assert accuracy is greater than or equal to 95%.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-13 | Accuracy measured at 88% — mock was returning incorrect dimensions causing 12 false negatives | FAIL | Test harness generated images at wrong resolution (640x480 instead of 720x1280) | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | Accuracy measured at 96% after correcting image dimensions in test harness | PASS | — | — |
| 3 | Jacob | 2025-12-01 | Accuracy measured at 95%, meets threshold | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Test harness was generating images at incorrect resolution, producing misleading accuracy numbers; correcting image dimensions yielded consistent 95%+ accuracy.

---

### TC-EISR3-AUTO-01 — JSON Output Structure Compliance

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR3-AUTO-01 |
| **Testing Tools Used** | pytest, json validation |
| **Testing Type** | Automated Non-Functional |

**Execution Steps:**
1. Generate JSON outputs from multiple scan events.
2. Load each JSON file and validate that the "workstation_id" field exists and is a string.
3. Validate that the "timestamp" field exists and is a string.
4. Validate that the "barcodes" field exists and is a list.
5. For each barcode object, verify it contains "name" (string) and "value" (string) fields.
6. Assert 100% compliance across all output files.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-12 | 2 of 5 outputs failed — "timestamp" field was an integer (Unix epoch) instead of ISO 8601 string | FAIL | OutputData serialized timestamp as int instead of formatted string | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | All 5 outputs passed structure validation; all fields present with correct types | PASS | — | — |
| 3 | Daniel | 2025-12-02 | 100% compliance across all generated outputs | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Timestamp was initially serialized as Unix epoch integer; converting to ISO 8601 string format brought all outputs into compliance.

---

### TC-EISR6-AUTO-01 — Config-Driven Workflow Behavior

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR6-AUTO-01 |
| **Testing Tools Used** | pytest, ConfigManager, WorkstationConfig |
| **Testing Type** | Automated Non-Functional |

**Execution Steps:**
1. Create Config 1 with required fields: part_number, serial_number.
2. Create Config 2 with required fields: part_number, batch_id, inspector_id.
3. Process an identical scan sequence through Config 1 and record required fields and completion state.
4. Process the same scan sequence through Config 2 and record required fields and completion state.
5. Assert that the two configs produce different required field sets.
6. Verify completion states differ when scan data satisfies one config but not the other.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-14 | Both configs returned identical completion states — ConfigManager was hardcoded to always use default field list | FAIL | ConfigManager ignored the loaded config and used hardcoded defaults | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | Config 1 and Config 2 produced different required field sets; completion states differed correctly | PASS | — | — |
| 3 | Nathan | 2025-12-03 | Distinct behavior confirmed for both configs | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. ConfigManager was ignoring loaded configuration files and using hardcoded defaults; after fixing the loader to respect config-driven fields, behavior diverged correctly per config.

---

## Manual Test Execution Records

---

### TC-SFR1-MAN-01 — Live QR Code Detection

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR1-MAN-01 |
| **Testing Tools Used** | Live 720p USB camera, printed QR codes, AIBI CV scanner UI |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Launch the scanner application with a 720p USB camera connected.
2. Position the camera so all three printed QR codes are visible in the field of view.
3. Observe the UI for real-time detection overlays on each QR code.
4. Record how many codes are detected and verify decoded payloads.
5. Repeat with codes positioned at the edges of the field of view.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-11 | Only 2 of 3 QR codes detected — third code at bottom-right corner of FOV was consistently missed | FAIL | Camera FOV too narrow at default resolution; edge detection threshold too strict | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | All 3 codes detected after adjusting detection sweep to cover full frame area | PASS | — | — |
| 3 | Daniel | 2025-11-30 | All 3 codes detected correctly including edge positions; payloads match expected values | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Edge-of-frame QR codes were initially missed due to overly strict detection boundaries; expanding the sweep area resolved the issue.

---

### TC-SFR2-MAN-01 — Field Mapping Configuration

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR2-MAN-01 |
| **Testing Tools Used** | Configuration files, printed test QR codes, JSON editor |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Open the workstation JSON configuration file.
2. Define barcode_fields mappings for part_number and serial_number.
3. Save the configuration file.
4. Scan the prepared QR codes containing part_number:PN-12345 and serial_number:SN-67890.
5. Inspect the output JSON to verify field-value assignments match the configured mappings.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-12 | Output JSON had "part_number": "SN-67890" and "serial_number": "PN-12345" — fields swapped | FAIL | Field mapping applied in alphabetical order instead of config-defined order | 2025-11-24 by Jacob |
| 2 | Jacob | 2025-11-24 | Field mappings correct: "part_number": "PN-12345", "serial_number": "SN-67890" | PASS | — | — |
| 3 | Collin | 2025-12-01 | Mappings verified correct for both fields | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Field mapping was applying values in alphabetical key order rather than config-specified order; fixing the mapping logic to respect config ordering resolved the swap.

---

### TC-SFR4-MAN-01 — JSON Record Generation from Live Scan

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR4-MAN-01 |
| **Testing Tools Used** | Live scanner, file system monitor |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Trigger a scan event by presenting QR codes to the camera.
2. Wait for the system to process the scan.
3. Navigate to the output directory and locate the generated JSON file.
4. Open the JSON file and verify it contains workstation_id, timestamp, and barcodes array.
5. Validate the timestamp is in ISO 8601 format.
6. Confirm the barcodes array contains correct name-value pairs.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-11 | JSON file created but timestamp was in Unix epoch format (integer), not ISO 8601 string | FAIL | Timestamp serialization used time.time() integer instead of datetime.isoformat() | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | JSON file generated with correct ISO 8601 timestamp, valid structure, and matching barcodes | PASS | — | — |
| 3 | Nathan | 2025-11-29 | JSON output verified: workstation_id, ISO timestamp, and barcodes all correct | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Timestamp format was Unix epoch integer instead of ISO 8601; switching serialization to datetime.isoformat() resolved the issue.

---

### TC-SFR5-MAN-01 — Keyboard Emulation Output

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR5-MAN-01 |
| **Testing Tools Used** | Live scanner, Microsoft Excel, keyboard monitoring |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Open Microsoft Excel and click into cell A1.
2. Configure the scanner application for keyboard-emulation mode with TAB delimiter.
3. Present QR codes (part_number:PN-12345, serial_number:SN-67890) and trigger the scan.
4. Observe the keystrokes typed into Excel.
5. Verify the output sequence: PN-12345 in A1, SN-67890 in B1 (TAB moved to next cell), then ENTER moved to next row.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-12 | PN-12345 typed correctly but TAB keystroke was not sent — both values appeared in cell A1 concatenated | FAIL | Keyboard emulation did not send TAB virtual key code between fields | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | PN-12345 in A1, TAB moved cursor, SN-67890 in B1, ENTER advanced to next row | PASS | — | — |
| 3 | Jacob | 2025-12-01 | Keystroke sequence matched expected pattern exactly in Excel | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. TAB virtual key was not being sent between field values; implementing proper VK_TAB keystroke injection resolved the issue.

---

### TC-SFR11-MAN-01 — Local JSON File Persistence

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR11-MAN-01 |
| **Testing Tools Used** | Live scanner, output directory, file explorer |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Perform five scan events with distinct QR code payloads.
2. Navigate to the output directory after all scans are complete.
3. Count the number of JSON files created (should be 5).
4. Open each file and verify contents match the scanned payloads.
5. Check that timestamps across the five files are sequential and unique.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-13 | Only 3 JSON files found after 5 scan events — files 2 and 4 were overwritten because filenames used second-level timestamp granularity and two scans happened within the same second | FAIL | File naming used timestamp with 1-second granularity, causing overwrites for rapid scans | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | All 5 JSON files present after switching to millisecond-precision filenames; contents match payloads | PASS | — | — |
| 3 | Collin | 2025-12-02 | 5 files present, all payloads correct, timestamps sequential and unique | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Filename timestamp granularity caused overwrites during rapid scanning; switching to millisecond precision eliminated collisions.

---

### TC-SFR12-MAN-01 — JSON Output Structure Validation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR12-MAN-01 |
| **Testing Tools Used** | JSON output files, manual inspection, json.loads() |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Open three JSON output files generated from different scan events.
2. Verify each file contains a workstation_id field of type string.
3. Verify each file contains a timestamp field as an ISO 8601 formatted string.
4. Verify each file contains a barcodes field that is an array of objects.
5. Verify each barcode object has "name" (string) and "value" (string) fields.
6. Run json.loads() on each file to confirm valid JSON syntax.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-14 | File 2 had barcodes as a flat list of strings instead of array of {name, value} objects | FAIL | Certain scan paths serialized barcodes as string list instead of object array | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | All 3 files have correct structure: workstation_id (str), timestamp (ISO 8601 str), barcodes (array of {name, value} objects) | PASS | — | — |
| 3 | Daniel | 2025-12-01 | All 3 files validated via json.loads() and manual inspection; 100% compliant | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. One serialization path produced flat string arrays for barcodes instead of structured objects; unifying the serialization format fixed the inconsistency.

---

### TC-SFR15-MAN-01 — Multi-Code Decoding Under Factory Lighting

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR15-MAN-01 |
| **Testing Tools Used** | Multi-code test sheet, live 720p camera, factory lighting (~200-500 lux) |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Position the 5-QR-code test sheet at approximately 40 cm from the camera.
2. Run detection under direct overhead factory lighting (~300 lux).
3. Record which codes are detected and their decoded payloads.
4. Tilt the test sheet to approximately 30 degrees and repeat detection.
5. Move the test sheet to the edge of the field of view and repeat.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-11 | 4 of 5 codes detected under overhead lighting; code_3 at center was washed out by glare at ~450 lux | FAIL | No glare compensation in image preprocessing pipeline | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | All 5 codes detected after adding adaptive histogram equalization; 30-degree tilt also passed | PASS | — | — |
| 3 | Daniel | 2025-11-29 | All 5 codes decoded correctly across all lighting conditions and angles | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Glare from overhead factory lighting washed out one QR code; adding adaptive histogram equalization to the preprocessing pipeline resolved the issue.

---

### TC-SFR16-MAN-01 — Complete Output for All Visible QR Codes

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR16-MAN-01 |
| **Testing Tools Used** | Live scanner, 3 distinct printed QR codes |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Arrange all three distinct QR codes (part_number:PN-001, serial_number:SN-002, batch_id:BATCH-003) in the camera's field of view.
2. Trigger a scan event.
3. Inspect the output JSON barcodes array.
4. Count the number of entries in the barcodes array.
5. Confirm no duplicate entries exist and each visible code has exactly one entry.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-13 | Barcodes array contained 4 entries — PN-001 appeared twice due to multi-frame accumulation without dedup | FAIL | Scan accumulated detections across multiple frames without deduplication | 2025-11-24 by Daniel |
| 2 | Daniel | 2025-11-24 | Barcodes array contained exactly 3 entries, no duplicates, all payloads correct | PASS | — | — |
| 3 | Jacob | 2025-12-01 | 3 entries, no duplicates, all correct | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Multi-frame accumulation was including duplicate detections; adding deduplication before output generation resolved the duplicate entries.

---

### TC-SFR6-MAN-01 — Step Sequence Validation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR6-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 3-step process, USB camera |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load the trained 3-step process ("Step A", "Step B", "Step C") in Operation mode.
2. Perform Step A in front of the camera and verify the system transitions to CORRECT_STEP then CONFIRMED.
3. Perform Step B and verify it is also confirmed in correct order.
4. Skip Step C and perform an unrelated action — verify the system flags WRONG_ORDER or SKIPPED.
5. Expand the run log and check for violation entries.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | Steps A and B confirmed correctly, but skipping to an unrelated action did not trigger any violation flag — system remained in IDLE state instead of detecting a skip | FAIL | Sequence validator did not track expected-vs-actual step progression; skip detection was not implemented | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | Steps A and B confirmed; skipping C triggered WRONG_ORDER flag but no log entry was written to run history | FAIL | Violation detection worked but logging to run history was not wired up | 2025-11-28 by Nathan |
| 3 | Nathan | 2025-11-28 | All steps confirmed correctly in order; skip detected, flagged, and logged in run history with step name and violation type | PASS | — | — |
| 4 | Jacob | 2025-12-02 | Correct-order steps confirmed, out-of-order detected and logged properly | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Required two fix cycles: first to implement skip/out-of-order detection logic, then to wire violation logging into run history. Final executions confirmed full sequence validation functionality.

---

### TC-SFR7-MAN-01 — Live Video UI Overlay

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR7-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained process, USB camera |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Start Operation mode with a loaded trained process containing 3 or more steps.
2. Observe the live video feed displayed on the Streamlit interface.
3. Verify the current step name is displayed as a text overlay or UI element.
4. Verify the similarity confidence percentage is shown and updates in real time.
5. Complete a step and verify the progress bar updates to reflect completion.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-15 | Live video feed displayed but no step name or confidence score shown — overlay elements were not rendering | FAIL | Streamlit st.image() call was overwriting the overlay div; overlay placement logic missing | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | Step name and confidence score now visible; progress bar present but did not update when step completed | FAIL | Progress bar was reading initial step count but not subscribing to state updates | 2025-11-28 by Collin |
| 3 | Collin | 2025-11-28 | All overlay elements visible: step name, confidence percentage, and progress bar all updating in real time | PASS | — | — |
| 4 | Nathan | 2025-12-02 | Full overlay functionality confirmed across multiple steps | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Two iterations needed: first to add overlay rendering alongside the video feed, second to make the progress bar reactive to state changes. All elements functional in final runs.

---

### TC-SFR8-MAN-01 — Process Training Interface

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR8-MAN-01 |
| **Testing Tools Used** | Streamlit app, USB camera |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Select Training mode from the Streamlit app mode selector.
2. Add three step names using the UI: "Install Part A", "Tighten Bolts", "Inspect Assembly".
3. For each step, click "Start Recording" and capture reference frames from the camera.
4. Click "Stop" to end recording for each step.
5. Click "Finalize Training" to compute DINOv2 embeddings for all recorded frames.
6. Click "Save Process" and download the resulting .pkl file.
7. Verify the downloaded .pkl file is non-empty.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-16 | Step names added and frames recorded, but "Finalize Training" raised RuntimeError — DINOv2 model not loaded at training time | FAIL | DINOv2 model was only initialized in Operation mode, not in Training mode | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | Training finalized and .pkl file downloaded, but file size was 0 bytes | FAIL | serialize_process() returned empty bytes when called before session state was fully committed | 2025-11-28 by Daniel |
| 3 | Daniel | 2025-11-28 | Full training workflow completed: 3 steps defined, frames recorded, embeddings computed, .pkl file downloaded (42 KB) | PASS | — | — |
| 4 | Collin | 2025-12-02 | Training workflow verified end-to-end; .pkl file non-empty and downloadable | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Two defects addressed: DINOv2 model not being available in Training mode, and serialization producing empty files. Both fixed by ensuring model pre-loading and proper session state management.

---

### TC-SFR9-MAN-01 — Configurable Sensitivity Thresholds

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR9-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Note the default similarity threshold value (0.6) displayed on the slider.
2. Perform a step at default threshold and observe confirmation behavior.
3. Increase the threshold to 0.9 (stricter) and repeat the same step — observe that it becomes harder to confirm.
4. Decrease the threshold to 0.3 (looser) and repeat the same step — observe that it confirms more easily.
5. Verify that each threshold change produces a measurably different detection behavior.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-16 | Slider moved but behavior did not change — threshold value was read once at startup and not re-read per frame | FAIL | Threshold was cached at initialization instead of being read dynamically from slider state | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | Threshold changes now affect detection: 0.9 required near-exact match, 0.3 accepted loose match | PASS | — | — |
| 3 | Jacob | 2025-12-01 | Behavior differences confirmed at all three threshold levels | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Threshold was being cached at startup rather than read dynamically from the Streamlit slider; making the read per-frame resolved the issue.

---

### TC-SFR10-MAN-01 — Process Deviation Logging

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR10-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 3-step process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load a trained 3-step process in Operation mode.
2. Complete step 1 correctly and wait for confirmation.
3. Skip step 2 and perform step 3 instead.
4. Expand the run history section in the Streamlit UI.
5. Verify the violation is logged with the step name and violation type (SKIPPED or WRONG_ORDER).

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-16 | Step 1 completed, step 2 skipped, step 3 performed — but run history section showed no violation entry; only completed steps were logged | FAIL | Logging only recorded CONFIRMED transitions, not violation events | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | Violation logged in run history with step name "Step B" and type "SKIPPED" | PASS | — | — |
| 3 | Collin | 2025-12-01 | Violation correctly logged; step name and type both accurate | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Logging was initially limited to successful step confirmations and did not capture violations; extending the logger to record SKIPPED and WRONG_ORDER events resolved the issue.

---

### TC-SFR14-MAN-01 — Training Dataset Save and Load

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR14-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained process, file uploader |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Complete a training session with at least 2 steps and finalize the process.
2. Click "Save Process" to download the .pkl file.
3. Close and restart the Streamlit application.
4. Use the file uploader widget to load the saved .pkl file.
5. Verify all step names from the original training are present in the loaded process.
6. Switch to Operation mode and verify step detection works with the loaded embeddings.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-17 | .pkl file loaded but step names displayed as empty strings — step name field was not included in serialization | FAIL | serialize_process() omitted step_name attribute from the serialized dictionary | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | Step names present after load; Operation mode started but detection threw ValueError on centroid shape mismatch | FAIL | Centroid arrays were flattened during serialization, losing their 2D shape | 2025-11-28 by Daniel |
| 3 | Daniel | 2025-11-28 | Full save/load cycle successful: step names present, detection functional in Operation mode | PASS | — | — |
| 4 | Collin | 2025-12-03 | Save, restart, load, and detection all verified working end-to-end | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Two defects required fixing: step names omitted from serialization, and centroid array shape lost during pickling. Both resolved for full round-trip integrity.

---

### TC-SFR19-MAN-01 — Error Messages Display

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR19-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load a trained process in Operation mode.
2. Perform step 1 correctly and wait for confirmation.
3. Deliberately skip step 2 and perform step 3.
4. Observe the Streamlit UI for any error or warning messages.
5. Verify the displayed message identifies the violation type and the affected step name.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-16 | Violation detected internally (confirmed via logs) but no visual error message appeared in the Streamlit UI | FAIL | Violation state was logged to console but st.warning()/st.error() calls were not implemented | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-25 | st.warning() message displayed identifying violation type as "SKIPPED" and step name "Step B" | PASS | — | — |
| 3 | Nathan | 2025-12-01 | Error message displayed clearly with correct violation type and step name | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Violations were detected and logged to console but not surfaced to the UI; adding st.warning() calls to render violations on screen resolved the issue.

---

### TC-SFR20-MAN-01 — Step List Display

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR20-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 4-step process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load a trained process with 4 steps in Operation mode.
2. Start Operation mode.
3. Verify the step checklist is visible on the Streamlit UI.
4. Count the number of steps shown in the checklist.
5. Verify each step name matches the names defined during training.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-17 | Step checklist visible but only showed 3 of 4 steps — last step was truncated due to rendering logic using range(len-1) | FAIL | Loop iterated steps[0:n-1] instead of steps[0:n], cutting off the last step | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | All 4 steps displayed in checklist with correct names matching the trained process | PASS | — | — |
| 3 | Jacob | 2025-12-02 | 4 steps visible, names match, correct order | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Off-by-one error in the step list rendering loop truncated the last step; correcting the loop range to include all steps resolved the issue.

---

### TC-SFR21-MAN-01 — Completed Step Visual Marker

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR21-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 3-step process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load the trained process and start Operation mode.
2. Complete step 1 and wait for the system to confirm it.
3. Observe the step list — verify step 1 now shows a green checkmark (checkmark marker).
4. Complete step 2 and verify it also shows the completed marker.
5. Verify step 3 still shows the pending marker (empty box).

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-17 | Step 1 completed but marker did not change from pending to completed — UI did not refresh step list after state transition | FAIL | Step list was rendered once on load and not re-rendered on state changes | 2025-11-28 by Nathan |
| 2 | Nathan | 2025-11-28 | Step 1 shows completed marker after completion; step 2 shows completed after completion; step 3 shows pending | PASS | — | — |
| 3 | Collin | 2025-12-02 | All markers update correctly as steps are completed | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Step list was not re-rendering on state changes; adding Streamlit rerun triggers after state transitions ensured markers update in real time.

---

### TC-SFR22-MAN-01 — Missed/Skipped Step Visual Marker

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR22-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 3-step process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Load a trained 3-step process in Operation mode.
2. Complete step 1 and wait for confirmation.
3. Skip step 2 by performing step 3 instead.
4. Observe the step list and verify step 2 shows a distinct missed/skipped indicator (not a completed marker).
5. Verify the missed indicator is visually different from both completed and pending markers.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-17 | Step 2 still showed pending marker after being skipped — no distinct skipped marker was implemented | FAIL | Only CONFIRMED and PENDING states had visual markers; SKIPPED state fell through to default pending marker | 2025-11-28 by Jacob |
| 2 | Jacob | 2025-11-28 | Step 2 now shows a distinct red marker when skipped, clearly different from completed and pending | PASS | — | — |
| 3 | Daniel | 2025-12-02 | Skipped step marker is visually distinct and clearly identifies the missed step | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. No visual marker existed for the SKIPPED state; implementing a distinct red indicator for skipped steps resolved the issue.

---

### TC-SFR26-MAN-01 — Step Progress Indicators

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR26-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained process, sliding window configuration |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Configure the sliding window size to 5 and required votes to 3 using the UI sliders.
2. Start Operation mode with a loaded trained process.
3. Begin performing step 1 in front of the camera.
4. Observe the progress display as frames are matched against the step reference.
5. Verify the vote count increments toward the required threshold (e.g., "2/3 votes").

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-17 | Vote count displayed as "0/3" and never incremented even though frames were matching — vote accumulation logic was not connected to the display | FAIL | Voting counter was computed internally but the UI label was hardcoded to show "0/{required}" | 2025-11-28 by Collin |
| 2 | Collin | 2025-11-28 | Vote count increments correctly: observed "1/3", "2/3", "3/3" before step confirmation | PASS | — | — |
| 3 | Nathan | 2025-12-02 | Progress indicator updates in real time showing accurate vote counts | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. UI label was hardcoded instead of reading from the live vote counter; binding the display to the actual voting state resolved the issue.

---

### TC-SFR28-MAN-01 — Reset/Restart Run

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-SFR28-MAN-01 |
| **Testing Tools Used** | Streamlit app, trained 3-step process |
| **Testing Type** | Manual Functional |

**Execution Steps:**
1. Complete 2 of 3 steps in a trained process during Operation mode.
2. Click the "Restart Run" button.
3. Verify all steps reset to pending state (empty box markers).
4. Verify the current step indicator resets to step 1.
5. Verify the previous run is logged in the run history section.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-17 | Clicking restart reset step markers to pending but current step remained at step 3 — step pointer was not reset | FAIL | Restart logic cleared step statuses but did not reset the current_step_index to 0 | 2025-11-28 by Daniel |
| 2 | Daniel | 2025-11-28 | All steps reset to pending, current step resets to step 1, but previous run was not saved to history | FAIL | Restart did not call the run history append function before clearing state | 2025-11-30 by Daniel |
| 3 | Daniel | 2025-11-30 | Full reset: all steps pending, current step at 1, previous run logged in history with timestamps and results | PASS | — | — |
| 4 | Nathan | 2025-12-03 | Restart verified: state fully reset, history preserved | PASS | — | — |

**Execution Summary:** Total executions: 4. Pass rate: 50%. Two issues fixed: current step index not resetting on restart, and previous run not being archived before clearing state. Both resolved for full restart functionality.

---

### TC-PUSR1-MAN-01 — New Operator Onboarding Time

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR1-MAN-01 |
| **Testing Tools Used** | System UI, stopwatch, task checklist |
| **Testing Type** | Manual Usability |

**Execution Steps:**
1. Recruit a new operator with no prior experience with the system.
2. Give a 5-minute verbal overview of the system.
3. Start a stopwatch timer.
4. Operator completes the task checklist without assistance: launch app, perform scan, verify output, configure field mapping.
5. Record time per task and total time.
6. Stop timer at completion or at 30-minute mark.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-14 | Operator completed in 38 minutes — spent 12 minutes on field mapping configuration due to unclear UI labels | FAIL | Configuration UI lacked descriptive labels and help text for field mapping | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-28 | Operator completed in 22 minutes after adding help text to configuration fields | PASS | — | — |
| 3 | Nathan | 2025-12-01 | New operator completed all tasks in 19 minutes | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Initial onboarding exceeded 30 minutes due to unclear field mapping UI; adding descriptive help text reduced onboarding time to under 25 minutes consistently.

---

### TC-PUSR2-MAN-01 — Streamlit Help Text and UI Guidance

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR2-MAN-01 |
| **Testing Tools Used** | Streamlit app, test users, questionnaire |
| **Testing Type** | Manual Usability |

**Execution Steps:**
1. Present the Streamlit UI to a test user unfamiliar with the application.
2. Ask the user to identify the purpose of 8 major controls using only on-screen text: mode selector, record button, stop button, finalize button, save button, load button, restart button, threshold sliders.
3. Record correct and incorrect identifications for each control.
4. Calculate the accuracy rate (correct / total).
5. Repeat with additional test users.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | User identified 4 of 8 controls correctly (50%) — finalize, save, load, and threshold sliders were unclear | FAIL | Buttons lacked descriptive labels; sliders had no help_text parameter set | 2025-11-25 by Jacob |
| 2 | Jacob | 2025-11-25 | User identified 6 of 8 controls correctly (75%) after adding st.help_text to sliders and renaming buttons | PASS | — | — |
| 3 | Daniel | 2025-12-01 | User identified 7 of 8 controls correctly (87.5%) | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Initial UI lacked adequate help text on sliders and descriptive button labels; adding st.help_text parameters and more descriptive labels improved identification accuracy from 50% to 87.5%.

---

### TC-PUSR3-MAN-01 — Workflow Step Reduction vs. Legacy

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR3-MAN-01 |
| **Testing Tools Used** | Legacy system documentation, new system, comparison sheet |
| **Testing Type** | Manual Usability |

**Execution Steps:**
1. Document the legacy workflow steps for scanning three parts and recording data.
2. Perform the same task on the new system.
3. Count the number of manual inputs required on each system.
4. Compare the step counts and calculate the percentage reduction.
5. Verify the new system achieves at least 25% reduction in manual steps.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-14 | Legacy: 12 steps. New system: 5 steps. Reduction: 58%. Exceeds 25% threshold | PASS | — | — |
| 2 | Daniel | 2025-11-29 | Legacy: 12 steps. New system: 4 steps. Reduction: 67% | PASS | — | — |
| 3 | Collin | 2025-12-01 | Legacy: 12 steps. New system: 5 steps. Reduction: 58% | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 100%. New system consistently achieved 58-67% reduction in manual steps compared to the legacy workflow, well exceeding the 25% threshold.

---

### TC-PUSR4-MAN-01 — Touch-Free Operation During Scanning

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR4-MAN-01 |
| **Testing Tools Used** | Live system, operator observation |
| **Testing Type** | Manual Usability |

**Execution Steps:**
1. Configure the system for a standard scanning workflow.
2. Operator performs 10 consecutive scan cycles.
3. An observer counts the number of UI touches (mouse clicks, keyboard presses) per scan cycle.
4. Calculate the average number of UI interactions per cycle.
5. Verify the average is 2 or fewer.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-15 | Average 3.2 UI touches per cycle — operator had to click "confirm" button after each scan event | FAIL | Scan confirmation required an explicit button click instead of auto-confirming on successful detection | 2025-11-25 by Nathan |
| 2 | Nathan | 2025-11-25 | Average 1.4 UI touches per cycle after removing manual confirmation step | PASS | — | — |
| 3 | Collin | 2025-12-01 | Average 1.2 UI touches per cycle | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Manual confirmation button was adding unnecessary UI interactions; removing the explicit confirm step and auto-confirming on successful detection brought the average well under 2.

---

### TC-PUSR10-MAN-01 — Emoji and Color State Indicators

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PUSR10-MAN-01 |
| **Testing Tools Used** | UI screenshots, 3 test users |
| **Testing Type** | Manual Usability |

**Execution Steps:**
1. Capture screenshots of the app in three states: all-pending (all empty box markers), mid-progress (mix of completed, current, and pending markers), and violation detected (red overlay/marker).
2. Present each screenshot to 3 test users.
3. Ask users to identify: which steps are done, which is current, which are pending, and whether an error/violation is shown.
4. Record accuracy for each user across all states.
5. Calculate overall accuracy (need at least 85%).

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-16 | Average accuracy 70% across 3 users — users confused current step marker with pending marker because both looked similar in small text | FAIL | Current step marker was too small and not color-differentiated from pending | 2025-11-28 by Jacob |
| 2 | Jacob | 2025-11-28 | Average accuracy 88% after enlarging current step marker and adding blue color highlighting for current step | PASS | — | — |
| 3 | Collin | 2025-12-02 | Average accuracy 92% across 3 users | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Users initially confused the current step marker with the pending marker; enlarging the current step indicator and adding color differentiation improved recognition accuracy from 70% to 92%.

---

### TC-PPSR2-MAN-01 — Real-Time Feedback Perception

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR2-MAN-01 |
| **Testing Tools Used** | Live system, operator, response time monitoring |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Set up the system under normal operating load.
2. Operator performs 10 consecutive scan/verification cycles.
3. Measure the time from operator action to visible UI feedback for each cycle.
4. Ask the operator whether they perceived any delay.
5. Record all response times and operator feedback.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-14 | Average response time 620 ms; operator reported noticeable lag between scan and result display | FAIL | UI was waiting for full JSON write to complete before showing detection result | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | Average response time 180 ms after making JSON write asynchronous; operator reported "immediate" feel | PASS | — | — |
| 3 | Nathan | 2025-12-01 | Average response time 195 ms; operator reported no perceived delay | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. UI was blocking on file I/O before displaying results; making JSON write asynchronous reduced perceived response time from 620 ms to under 200 ms.

---

### TC-PPSR5-MAN-01 — 720p Camera Hardware Reliability

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PPSR5-MAN-01 |
| **Testing Tools Used** | 720p USB camera, test QR sheet, live testing |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Connect a 720p USB camera to the system.
2. Position the 5-QR-code test sheet at 40 cm from the camera.
3. Run 20 detection cycles.
4. Record the success rate (cycles where all codes were correctly detected).
5. Verify the success rate is at least 95%.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-13 | 17 of 20 cycles successful (85%) — 3 cycles had partial detections due to camera auto-focus hunting at 720p | FAIL | Auto-focus instability at 720p caused intermittent blur during detection window | 2025-11-24 by Collin |
| 2 | Collin | 2025-11-24 | 19 of 20 cycles successful (95%) after adding frame stability check before detection | PASS | — | — |
| 3 | Jacob | 2025-11-30 | 20 of 20 cycles successful (100%) | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Auto-focus hunting at 720p caused intermittent detection failures; adding a frame stability check before running detection eliminated the issue.

---

### TC-PDSR1-MAN-01 — No Outbound Network Traffic

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR1-MAN-01 |
| **Testing Tools Used** | Network monitoring tools (Wireshark), live system |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Start Wireshark or equivalent network monitoring tool on the host machine.
2. Launch the AIBI CV application and run it through a full operational cycle.
3. Perform 20 or more scan events over a 1-hour period.
4. Stop the network capture.
5. Review all outbound connection logs and verify zero connections to external IP addresses or domains.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Nathan | 2025-11-12 | Wireshark captured 2 outbound HTTPS requests to pypi.org during application startup — pip check was running at launch | FAIL | requirements check script triggered outbound pip queries on startup | 2025-11-24 by Nathan |
| 2 | Nathan | 2025-11-24 | Zero outbound connections during full 1-hour test after removing startup pip check | PASS | — | — |
| 3 | Daniel | 2025-12-01 | Zero external connections across 25 scan events over 1 hour | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. A startup pip check was triggering outbound network requests; removing the startup dependency check eliminated all external traffic.

---

### TC-PDSR2-MAN-01 — Fully Offline Operation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR2-MAN-01 |
| **Testing Tools Used** | Network disconnect, live system |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Disconnect all internet connections (Ethernet and Wi-Fi) from the host machine.
2. Launch the AIBI CV application.
3. Perform 10 QR scan events and verify JSON output files are created.
4. Test keyboard emulation mode and verify keystrokes are sent correctly.
5. Load a trained process via file uploader and run step verification.
6. Continue operating for at least 1 hour.
7. Verify all features function identically to online operation.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-13 | All features functional offline: 10 scans produced valid JSON, keyboard emulation worked, step verification operated normally for 1+ hour | PASS | — | — |
| 2 | Collin | 2025-11-29 | Full offline operation confirmed across all features for 1.5 hours | PASS | — | — |
| 3 | Nathan | 2025-12-01 | All features verified offline; no degradation observed | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 100%. System operated fully offline with no feature degradation across all test runs. All processing is local as designed.

---

### TC-PDSR4-MAN-01 — Factory Environment Stability

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-PDSR4-MAN-01 |
| **Testing Tools Used** | Factory deployment environment, CPU/memory monitoring tools |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Deploy the system in the factory or simulated factory environment.
2. Start continuous operation with periodic scan events (approximately every 5 minutes).
3. Monitor CPU and memory usage throughout the test period.
4. Log any errors, crashes, or anomalies.
5. Review monitoring data after 8 or more hours of continuous operation.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Daniel | 2025-11-15 | System crashed at 5.5 hours — memory usage climbed from 250 MB to 1.8 GB due to frame buffer not being cleared between scans | FAIL | Frame buffer accumulated raw frames without cleanup, causing memory growth | 2025-11-25 by Daniel |
| 2 | Daniel | 2025-11-25 | System ran for 8.5 hours with stable memory (250-320 MB range); zero crashes after adding frame buffer cleanup | PASS | — | — |
| 3 | Collin | 2025-12-03 | 9 hours continuous operation; CPU stable at 15-25%, memory stable at 280-310 MB, zero crashes | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Memory leak from uncleaned frame buffer caused a crash at 5.5 hours; implementing frame buffer cleanup between scans stabilized memory usage for 8+ hour operation.

---

### TC-ODSR2-MAN-01 — OSS Component Documentation

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-ODSR2-MAN-01 |
| **Testing Tools Used** | Documentation review, pip freeze output |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Run pip freeze to generate the full list of installed dependencies.
2. Compare the pip freeze output against the documented OSS component list.
3. Verify each documented component has name, version, and license information.
4. Identify any undocumented dependencies present in pip freeze but missing from documentation.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Jacob | 2025-11-14 | pip freeze showed 28 packages; documentation listed 22 — 6 transitive dependencies (e.g., Pillow, urllib3) were undocumented | FAIL | Transitive dependencies were not included in the OSS documentation | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-25 | All 28 packages documented with name, version, and license after adding missing transitive deps | PASS | — | — |
| 3 | Nathan | 2025-12-01 | 100% of pip freeze packages documented with complete information | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. Six transitive dependencies were missing from OSS documentation; auditing and adding all transitive packages with their license information brought documentation to 100% coverage.

---

### TC-EISR6-MAN-01 — Config-Driven Workflow Customization

| Field | Details |
|---|---|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Case ID** | TC-EISR6-MAN-01 |
| **Testing Tools Used** | Configuration JSON files, field engineer |
| **Testing Type** | Manual Non-Functional |

**Execution Steps:**
1. Run a scan with the initial configuration (part_number, serial_number fields).
2. Verify the system enforces those fields in the output.
3. Edit the workstation config JSON to change required fields to part_number, batch_id, inspector_id (no code changes).
4. Restart the system.
5. Run the same scan and verify the new fields are enforced and old fields no longer apply.

**Test Execution Records:**

| # | Tester | Test Date | Actual Result | Status | Defect | Correction |
|---|---|---|---|---|---|---|
| 1 | Collin | 2025-11-15 | Initial config worked; edited config to add batch_id and inspector_id, restarted, but system still enforced old fields — config was cached in memory and not reloaded | FAIL | ConfigManager cached config at first load and did not re-read from disk on restart | 2025-11-25 by Collin |
| 2 | Collin | 2025-11-25 | Config changes reflected after restart; new fields enforced, old serial_number field no longer required | PASS | — | — |
| 3 | Daniel | 2025-12-03 | Config-driven customization verified: editing JSON and restarting changes workflow without code modifications | PASS | — | — |

**Execution Summary:** Total executions: 3. Pass rate: 67%. ConfigManager was caching the config in memory and not re-reading on application restart; fixing the loader to read from disk on each startup resolved the issue.

---

## Overall Test Execution Summary

| Metric | Value |
|---|---|
| **Total Test Cases** | 43 (32 manual + 11 automated) |
| **Total Executions** | 141 |
| **Final Pass Rate** | 100% |
| **Average Executions per Test Case** | 3.3 |
| **Test Cases Passing on First Attempt** | 2 (TC-PUSR3-MAN-01, TC-PDSR2-MAN-01) |
| **Test Cases Requiring 4 Executions** | 6 (TC-SFR14-AUTO-01, TC-SFR6-MAN-01, TC-SFR7-MAN-01, TC-SFR8-MAN-01, TC-SFR14-MAN-01, TC-SFR28-MAN-01) |
| **Testing Period** | 2025-11-11 through 2025-12-03 |
| **Team Members** | Nathan, Jacob, Collin, Daniel |

| Phase | Date Range | Description |
|---|---|---|
| Initial Testing | 2025-11-11 – 2025-11-17 | First execution of all 43 test cases; majority failed revealing implementation gaps |
| Defect Correction | 2025-11-24 – 2025-11-25 | Bug fixes applied based on initial test failures |
| Retesting | 2025-11-28 – 2025-11-30 | Second/third executions to verify fixes; some tests required additional corrections |
| Final Validation | 2025-12-01 – 2025-12-03 | Final pass confirming all 43 test cases at PASS status |

| Team Member | Test Cases Led | Total Executions Conducted |
|---|---|---|
| Nathan | 12 | 38 |
| Jacob | 11 | 34 |
| Collin | 11 | 36 |
| Daniel | 9 | 33 |
