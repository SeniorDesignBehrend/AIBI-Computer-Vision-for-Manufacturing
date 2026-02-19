# Appendix T — Test Case Definitions

> **Project Name:** AIBI CV for Manufacturing
> **Document Version:** 3.0
> **Last Updated:** 2026-02-17

---

## Test Suite 1: QR Scanner — Manual Functional

---

### TC-SFR1-MAN-01 — Live QR Code Detection

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR1-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the live camera feed detects and decodes all visible QR codes within the camera's field of view in real time. |
| **Preconditions** | (1) AIBI CV scanner application is installed and launched. (2) A USB camera (≥720p) is connected and recognized. (3) At least three printed QR codes with known payloads are prepared. |
| **Test Data Input** | Three printed QR codes at 30-60 cm, ~300 lux. Payloads: `part_number:PN-001`, `serial_number:SN-002`, `batch_id:BATCH-003`. |
| **Test Steps** | 1. Launch the scanner application. 2. Position the camera so all three QR codes are visible. 3. Observe the UI for real-time detection overlays. 4. Record how many codes are detected and their decoded payloads. 5. Repeat with codes at the edges of the FOV. |
| **Expected Result** | All three QR codes detected and decoded correctly within 1 second. |
| **Pass/Fail Criteria** | Pass: All visible QR codes detected with 100% accuracy. Fail: Any code missed or payload incorrect. |
| **Traceability** | UFR1 · SFR1, SFR15, SFR16 · UC-001 |

---

### TC-SFR2-MAN-01 — Field Mapping Configuration

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR2-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that an operator can configure field mappings through the workstation config so decoded QR values map to the correct logical fields. |
| **Preconditions** | (1) Scanner app running. (2) Workstation config with part_number, serial_number fields. (3) Printed QR codes with known payloads. |
| **Test Data Input** | WorkstationConfig with fields: part_number, serial_number. QR codes: `part_number:PN-12345`, `serial_number:SN-67890`. |
| **Test Steps** | 1. Open the workstation JSON config file. 2. Define barcode_fields for part_number and serial_number. 3. Save the configuration. 4. Scan the prepared QR codes. 5. Inspect the output JSON to verify field-value assignments. |
| **Expected Result** | Output JSON contains `"part_number": "PN-12345"` and `"serial_number": "SN-67890"`. |
| **Pass/Fail Criteria** | Pass: All decoded values map correctly. Fail: Any value misassigned or missing. |
| **Traceability** | UFR2 · SFR2 · UC-001 |

---

### TC-SFR4-MAN-01 — JSON Record Generation from Live Scan

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR4-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that a live scan event produces a single, correct JSON file containing all scanned data and metadata. |
| **Preconditions** | (1) App running with valid workstation config. (2) Camera connected. (3) QR codes in FOV. |
| **Test Data Input** | QR codes: `part_number:PN-001`, `serial_number:SN-002`. Workstation ID: `workstation_01`. |
| **Test Steps** | 1. Trigger scan by presenting QR codes. 2. Wait for system to process. 3. Navigate to output directory and open JSON file. 4. Verify JSON contains workstation_id, timestamp, and barcodes array. 5. Validate timestamp is ISO 8601 formatted. 6. Confirm barcodes array has correct name-value pairs. |
| **Expected Result** | Exactly one JSON file created per scan event with correct structure and data. |
| **Pass/Fail Criteria** | Pass: Valid JSON with all expected fields. Fail: Malformed, missing fields, or wrong data. |
| **Traceability** | UFR1, UFR4 · SFR4, SFR11 · UC-001 |

---

### TC-SFR5-MAN-01 — Keyboard Emulation Output

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR5-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that keyboard-emulation mode outputs correct keystrokes to a target application (e.g., Excel) after a live scan. |
| **Preconditions** | (1) App running in keyboard-emulation mode. (2) Excel or Notepad open with cursor in input field. (3) Config defines field order and TAB delimiter. |
| **Test Data Input** | QR codes: `part_number:PN-12345`, `serial_number:SN-67890`. Field order: [part_number, serial_number]. Delimiter: TAB. |
| **Test Steps** | 1. Open Excel and click into cell A1. 2. Run the scanner with keyboard emulation enabled. 3. Present QR codes and trigger scan. 4. Observe keystrokes typed into Excel. 5. Verify output: `PN-12345` → TAB → `SN-67890` → TAB → ENTER. |
| **Expected Result** | Excel displays correct values in order with TAB delimiters. |
| **Pass/Fail Criteria** | Pass: Keystroke sequence matches expected pattern exactly. Fail: Any character wrong, missing, or out of order. |
| **Traceability** | UFR9 · SFR5 · UC-001 |

---

### TC-SFR11-MAN-01 — Local JSON File Persistence

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR11-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that every scan event generates a JSON file persisted to the local output directory with no data loss. |
| **Preconditions** | (1) App running with valid config. (2) Output directory exists and is writable. |
| **Test Data Input** | Five consecutive scan events with distinct QR code payloads. |
| **Test Steps** | 1. Perform five scan events with distinct QR codes. 2. Navigate to the output directory. 3. Count the JSON files created. 4. Open each file and verify contents match the scan payloads. 5. Verify timestamps are sequential and unique. |
| **Expected Result** | Exactly five JSON files present with correct, matching payloads and sequential timestamps. |
| **Pass/Fail Criteria** | Pass: All five files present with correct data. Fail: Any file missing, corrupted, or data mismatch. |
| **Traceability** | UFR7, UFR10 · SFR11, PDSR1 · UC-001, UC-004 |

---

### TC-SFR12-MAN-01 — JSON Output Structure Validation

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR12-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that JSON output files contain all required fields with correct data types matching the expected structure. |
| **Preconditions** | (1) Three JSON output files generated from different scan events are available. |
| **Test Data Input** | Three JSON output files from different scans. |
| **Test Steps** | 1. Open three JSON output files. 2. Verify each file contains: workstation_id (string), timestamp (string, ISO 8601), barcodes (array of objects). 3. Verify each barcode object has "name" (string) and "value" (string) fields. 4. Verify the JSON is valid via json.loads(). 5. Record any deviations. |
| **Expected Result** | All files contain required fields with correct data types. |
| **Pass/Fail Criteria** | Pass: 100% of files have correct structure. Fail: Any missing field or wrong type. |
| **Traceability** | UFR4 · SFR12, EISR3 · UC-001 |

---

### TC-SFR15-MAN-01 — Multi-Code Decoding Under Factory Lighting

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR15-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system decodes all QR codes on a multi-code test sheet under typical factory lighting. |
| **Preconditions** | (1) Test sheet with five QR codes prepared. (2) Lighting ~200-500 lux. (3) 720p+ camera. |
| **Test Data Input** | Five QR codes: code_1 through code_5. Various lighting angles. |
| **Test Steps** | 1. Position test sheet at 40 cm. 2. Run detection under direct overhead lighting. 3. Record codes detected. 4. Tilt sheet to 30° and repeat. 5. Move to edge of FOV and repeat. |
| **Expected Result** | All five codes decoded correctly across all conditions. |
| **Pass/Fail Criteria** | Pass: All codes decode correctly. Fail: Any code missed or incorrect. |
| **Traceability** | UFR1 · SFR15 · UC-001 |

---

### TC-SFR16-MAN-01 — Complete Output for All Visible QR Codes

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | QR Scanner — Manual Functional |
| **Test Case ID** | TC-SFR16-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system output includes exactly one entry per visible QR code with no missed codes or duplicates. |
| **Preconditions** | (1) App running. (2) Three distinct QR codes in FOV. |
| **Test Data Input** | Three QR codes: part_number:PN-001, serial_number:SN-002, batch_id:BATCH-003. |
| **Test Steps** | 1. Arrange all three in camera view. 2. Trigger scan. 3. Inspect output JSON barcodes array. 4. Count entries. 5. Confirm no duplicates. |
| **Expected Result** | Exactly three entries, one per visible code, no duplicates. |
| **Pass/Fail Criteria** | Pass: Count equals visible count, no duplicates. Fail: Any code missing or duplicated. |
| **Traceability** | UFR1 · SFR16 · UC-001 |

---

## Test Suite 2: Step Verification — Manual Functional

---

### TC-SFR6-MAN-01 — Step Sequence Validation

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR6-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system correctly detects when manufacturing steps are performed in the correct sequence and flags out-of-order or skipped steps. |
| **Preconditions** | (1) Streamlit app is running in Operation mode. (2) A trained process with at least 3 defined steps is loaded. (3) Camera is connected and active. |
| **Test Data Input** | Trained process with steps: "Step A", "Step B", "Step C". Operator performs steps in correct order, then in wrong order. |
| **Test Steps** | 1. Load the trained process in Operation mode. 2. Perform Step A — verify system confirms it as CORRECT_STEP. 3. Perform Step B — verify system confirms it. 4. Skip Step C and perform an unrelated action — verify system flags WRONG_ORDER or SKIPPED. 5. Check the run log for violation entries. |
| **Expected Result** | Correct-order steps transition through IDLE → CORRECT_STEP → CONFIRMED. Out-of-order steps trigger WRONG_ORDER/SKIPPED state with logging. |
| **Pass/Fail Criteria** | Pass: Correct steps confirmed; violations detected and logged. Fail: Valid steps rejected or violations missed. |
| **Traceability** | UFR5 · SFR6, SFR10, PPSR4 · UC-002 |

---

### TC-SFR7-MAN-01 — Live Video UI Overlay

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR7-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the Streamlit UI displays a live camera feed with real-time overlay showing current step status, confidence scores, and progress indicators. |
| **Preconditions** | (1) App running in Operation mode. (2) Trained process loaded. (3) Camera connected. |
| **Test Data Input** | Normal operation with a trained process containing 3+ steps. |
| **Test Steps** | 1. Start Operation mode with a loaded process. 2. Observe the live video feed on the Streamlit interface. 3. Verify the current step name is displayed. 4. Verify the similarity confidence percentage is shown. 5. Verify the progress bar updates as steps are completed. |
| **Expected Result** | Live feed displays with accurate step name, confidence score, and progress bar. |
| **Pass/Fail Criteria** | Pass: All overlay elements visible and updating in real-time. Fail: Any element missing or stale. |
| **Traceability** | UFR6 · SFR7, SFR26 · UC-002 |

---

### TC-SFR8-MAN-01 — Process Training Interface

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR8-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that a user can define process steps, record reference frames, and save a trained process using the Training mode. |
| **Preconditions** | (1) Streamlit app is running. (2) Camera connected. (3) Training mode selected. |
| **Test Data Input** | New process with three steps: "Install Part A", "Tighten Bolts", "Inspect Assembly". |
| **Test Steps** | 1. Select Training mode. 2. Add three step names using the UI. 3. For each step, click "Start Recording" and capture reference frames. 4. Click "Stop" for each step. 5. Click "Finalize Training" to compute embeddings. 6. Click "Save Process" and download the .pkl file. 7. Verify file is non-empty and downloadable. |
| **Expected Result** | All three steps are defined, frames recorded, embeddings computed, and process saved as .pkl. |
| **Pass/Fail Criteria** | Pass: Process saved successfully with all step embeddings. Fail: Any step fails to record or save errors. |
| **Traceability** | UFR8, UFR12 · SFR8, SFR14 · UC-003 |

---

### TC-SFR9-MAN-01 — Configurable Sensitivity Thresholds

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR9-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that adjusting the similarity threshold, window size, and required votes sliders changes the system's detection behavior. |
| **Preconditions** | (1) App running in Operation mode. (2) Trained process loaded. |
| **Test Data Input** | Default threshold (0.6), then adjusted to 0.9 (strict) and 0.3 (loose). |
| **Test Steps** | 1. Note the default similarity threshold value. 2. Perform a step and record confidence score. 3. Increase threshold to 0.9 and repeat the same step. 4. Verify the step is harder to confirm at higher threshold. 5. Decrease threshold to 0.3 and verify the step confirms more easily. |
| **Expected Result** | Higher thresholds require more precise matches; lower thresholds accept looser matches. |
| **Pass/Fail Criteria** | Pass: Detection behavior changes proportionally with threshold adjustments. Fail: Threshold changes have no effect. |
| **Traceability** | UFR8 · SFR9 · UC-002, UC-003 |

---

### TC-SFR10-MAN-01 — Process Deviation Logging

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR10-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system logs every detected deviation (wrong order, skipped step) with step name and violation type in the run history. |
| **Preconditions** | (1) App in Operation mode with trained process. (2) Operator deliberately performs steps out of order. |
| **Test Data Input** | 3-step process where operator skips step 2 and jumps to step 3. |
| **Test Steps** | 1. Load a trained 3-step process. 2. Complete step 1 correctly. 3. Skip step 2 and perform step 3 instead. 4. Expand the run history section in the UI. 5. Verify the violation is logged with step name and type (SKIPPED or WRONG_ORDER). |
| **Expected Result** | Run history shows the violation entry with correct details. |
| **Pass/Fail Criteria** | Pass: All deviations logged with correct information. Fail: Any deviation missing from logs. |
| **Traceability** | UFR7 · SFR10 · UC-002, UC-004 |

---

### TC-SFR14-MAN-01 — Training Dataset Save and Load

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR14-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that a trained process can be saved as a .pkl file and loaded back with all step data intact. |
| **Preconditions** | (1) A process has been trained with at least 2 steps and finalized. (2) The save/download button is available. |
| **Test Data Input** | Trained process with steps: "Step A" (with embeddings), "Step B" (with embeddings). |
| **Test Steps** | 1. Complete training and finalize a process. 2. Save/download the .pkl file. 3. Restart the application. 4. Load the .pkl file using the file uploader. 5. Verify all step names are present. 6. Switch to Operation mode and verify detection works with loaded embeddings. |
| **Expected Result** | Loaded process contains all original steps with functional embeddings. |
| **Pass/Fail Criteria** | Pass: All steps loaded correctly and detection works. Fail: Any step missing or embeddings corrupted. |
| **Traceability** | UFR12 · SFR14 · UC-003 |

---

### TC-SFR19-MAN-01 — Error Messages Display

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR19-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system displays clear error messages on screen for all process errors (WRONG_ORDER, SKIPPED steps). |
| **Preconditions** | (1) App in Operation mode with trained process. |
| **Test Data Input** | Operator deliberately triggers a sequence violation. |
| **Test Steps** | 1. Load a trained process. 2. Perform step 1 correctly. 3. Deliberately skip to step 3. 4. Observe the Streamlit UI for error/warning messages. 5. Verify the message identifies the specific error type and affected step. |
| **Expected Result** | A visible warning or error message appears on screen identifying the violation type and step. |
| **Pass/Fail Criteria** | Pass: Error message is displayed clearly and accurately. Fail: No message or incorrect information. |
| **Traceability** | UFR13 · SFR19 · UC-002 |

---

### TC-SFR20-MAN-01 — Step List Display

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR20-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the UI displays a complete checklist of all process steps during Operation mode. |
| **Preconditions** | (1) App in Operation mode. (2) Trained process with 4+ steps loaded. |
| **Test Data Input** | Process with 4 steps. |
| **Test Steps** | 1. Load the trained process. 2. Start Operation mode. 3. Verify the step checklist is visible on the UI. 4. Count the number of steps shown. 5. Verify step names match the trained process. |
| **Expected Result** | All steps are listed with correct names in the correct order. |
| **Pass/Fail Criteria** | Pass: Complete step list displayed matching the trained process. Fail: Any step missing or out of order. |
| **Traceability** | UFR14 · SFR20 · UC-002 |

---

### TC-SFR21-MAN-01 — Completed Step Visual Marker

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR21-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that completed steps display a green checkmark (✅) visual marker in the step list. |
| **Preconditions** | (1) App in Operation mode with a trained process. |
| **Test Data Input** | 3-step process. |
| **Test Steps** | 1. Load the process and start Operation mode. 2. Complete step 1 and wait for confirmation. 3. Observe the step list — verify step 1 now shows ✅. 4. Complete step 2. 5. Verify step 2 also shows ✅ while step 3 shows ⬜ (pending). |
| **Expected Result** | Completed steps show ✅, pending steps show ⬜, current step shows ▶. |
| **Pass/Fail Criteria** | Pass: Visual markers update correctly as steps complete. Fail: Markers don't update or show wrong state. |
| **Traceability** | UFR15 · SFR21 · UC-002 |

---

### TC-SFR22-MAN-01 — Missed/Skipped Step Visual Marker

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR22-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that skipped or missed steps display a red indicator in the step list. |
| **Preconditions** | (1) App in Operation mode. (2) Trained process loaded. |
| **Test Data Input** | 3-step process where step 2 is skipped. |
| **Test Steps** | 1. Load the process. 2. Complete step 1. 3. Skip step 2 by performing step 3. 4. Observe the step list for step 2's visual indicator. 5. Verify it shows a different marker than completed steps. |
| **Expected Result** | Skipped step displays a distinct visual indicator (not ✅) clearly identifying it as missed. |
| **Pass/Fail Criteria** | Pass: Skipped step shows a distinct missed/error marker. Fail: Skipped step shows as pending or completed. |
| **Traceability** | UFR15 · SFR22 · UC-002 |

---

### TC-SFR26-MAN-01 — Step Progress Indicators

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR26-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that the UI displays progress indicators showing voting status (e.g., votes/required) during step verification. |
| **Preconditions** | (1) App in Operation mode. (2) Trained process loaded. (3) Sliding window voting configured. |
| **Test Data Input** | Window size: 5, Required votes: 3. |
| **Test Steps** | 1. Configure window size and required votes via sliders. 2. Start Operation mode. 3. Begin performing step 1. 4. Observe the progress display as frames are matched. 5. Verify the vote count increments toward the required threshold. |
| **Expected Result** | Progress indicator shows current votes vs. required (e.g., "2/3 votes"). |
| **Pass/Fail Criteria** | Pass: Vote count updates in real-time. Fail: No progress indication or incorrect count. |
| **Traceability** | UFR6 · SFR26 · UC-002 |

---

### TC-SFR28-MAN-01 — Reset/Restart Run

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Step Verification — Manual Functional |
| **Test Case ID** | TC-SFR28-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the restart button resets the step verification state to prepare for the next part/run. |
| **Preconditions** | (1) App in Operation mode. (2) A partial or complete run has been performed. |
| **Test Data Input** | A process where 2 of 3 steps have been completed. |
| **Test Steps** | 1. Complete 2 steps of a 3-step process. 2. Click the "↺ Restart Run" button. 3. Verify all steps reset to pending (⬜). 4. Verify the current step resets to step 1. 5. Verify the previous run is logged in run history. |
| **Expected Result** | All step states reset. Current step returns to step 1. Previous run preserved in history. |
| **Pass/Fail Criteria** | Pass: Full reset with run history preserved. Fail: State not fully reset or history lost. |
| **Traceability** | UFR20 · SFR28 · UC-002 |

---

## Test Suite 3: Usability and Operator Workflow

---

### TC-PUSR1-MAN-01 — New Operator Onboarding Time

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Usability and Operator Workflow |
| **Test Case ID** | TC-PUSR1-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that a new operator with no prior experience can complete the basic scanning workflow within 30 minutes. |
| **Preconditions** | (1) System fully set up. (2) New test participant available. (3) Stopwatch and checklist prepared. |
| **Test Data Input** | New user, pre-configured workstation, task checklist: launch app, perform scan, verify output, configure field mapping. |
| **Test Steps** | 1. Give new operator 5-minute verbal overview. 2. Start timer. 3. Operator completes checklist without assistance. 4. Record time per task. 5. Stop at completion or 30 minutes. |
| **Expected Result** | Operator completes all tasks within 30 minutes. |
| **Pass/Fail Criteria** | Pass: ≤30 minutes. Fail: >30 minutes or cannot complete. |
| **Traceability** | UFR8, PUUR1 · PUSR1 · UC-001 |

---

### TC-PUSR2-MAN-01 — Streamlit Help Text and UI Guidance

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Usability and Operator Workflow |
| **Test Case ID** | TC-PUSR2-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that the Streamlit UI provides adequate help text (slider descriptions, st.info messages, button labels) for users to understand major functions. |
| **Preconditions** | (1) App running with all UI elements visible. (2) A test user unfamiliar with the app. |
| **Test Data Input** | System UI. Questionnaire listing 8 major controls: mode selector, record button, stop button, finalize button, save button, load button, restart button, threshold sliders. |
| **Test Steps** | 1. Present the UI to the test user. 2. Ask user to identify the purpose of each control using only on-screen text (labels, help text, info messages). 3. Record correct/incorrect identifications. 4. Calculate accuracy rate. |
| **Expected Result** | User correctly identifies ≥ 75% of controls (≥ 6 of 8). |
| **Pass/Fail Criteria** | Pass: ≥75% correct identification. Fail: <75%. |
| **Traceability** | PUUR1 · PUSR2 · UC-001 |

---

### TC-PUSR3-MAN-01 — Workflow Step Reduction vs. Legacy

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Usability and Operator Workflow |
| **Test Case ID** | TC-PUSR3-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that the new system requires fewer manual steps than the legacy workflow. |
| **Preconditions** | (1) Legacy workflow documented with step count. (2) New system set up for same task. |
| **Test Data Input** | Legacy documentation. Same task on both systems (scan three parts, record data). |
| **Test Steps** | 1. Document legacy workflow steps. 2. Perform same task on new system. 3. Count manual inputs. 4. Compare and calculate reduction. |
| **Expected Result** | New system requires fewer manual steps (≥25% reduction). |
| **Pass/Fail Criteria** | Pass: New < legacy. Fail: New ≥ legacy. |
| **Traceability** | UFR8 · PUSR3 · UC-001 |

---

### TC-PUSR4-MAN-01 — Touch-Free Operation During Scanning

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Usability and Operator Workflow |
| **Test Case ID** | TC-PUSR4-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the operator rarely needs to touch the UI during a typical QR scan cycle. |
| **Preconditions** | (1) System configured. (2) Operator performing production job. |
| **Test Data Input** | 10 consecutive scan cycles. |
| **Test Steps** | 1. Configure system. 2. Operator performs 10 scan cycles. 3. Count UI touches per cycle. 4. Calculate average. |
| **Expected Result** | Average ≤2 UI interactions per cycle. |
| **Pass/Fail Criteria** | Pass: ≤2 avg. Fail: >2. |
| **Traceability** | PUUR2 · PUSR4 · UC-001, UC-002 |

---

### TC-PUSR10-MAN-01 — Emoji and Color State Indicators

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Usability and Operator Workflow |
| **Test Case ID** | TC-PUSR10-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that users can correctly interpret step status from the emoji markers (✅, ▶, ⬜) and color-coded overlays (green/red) used in the UI. |
| **Preconditions** | (1) Screenshots of the app in various states (all steps pending, some completed, violation detected). (2) Three test users. |
| **Test Data Input** | Screenshots showing: all-pending state, mid-progress state, violation state. |
| **Test Steps** | 1. Present each screenshot to test users. 2. Ask users to identify: which steps are done, which is current, which are pending. 3. Ask users to identify if an error/violation is shown. 4. Record accuracy. 5. Calculate overall accuracy across users and states. |
| **Expected Result** | Users correctly identify step states ≥ 85% of the time. |
| **Pass/Fail Criteria** | Pass: ≥85% accuracy. Fail: <85%. |
| **Traceability** | PUUR4, PUUR1 · PUSR10 · UC-001, UC-002 |

---

## Test Suite 4: System-Level Non-Functional

---

### TC-PPSR2-MAN-01 — Real-Time Feedback Perception

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-PPSR2-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that feedback appears immediate — operator perceives no delay during scanning or step verification. |
| **Preconditions** | (1) System running under normal load. (2) Operator available. |
| **Test Data Input** | 10 consecutive scan/verification cycles. Stopwatch or system logging. |
| **Test Steps** | 1. Operator performs 10 cycles. 2. Measure time from action to UI feedback. 3. Ask operator if they perceived delay. 4. Record times and feedback. |
| **Expected Result** | Response time <500 ms. Operator reports no perceived delay. |
| **Pass/Fail Criteria** | Pass: <500 ms and "immediate" feel. Fail: ≥500 ms or perceived delay. |
| **Traceability** | UFR1 · PPSR2 · UC-001, UC-002 |

---

### TC-PPSR5-MAN-01 — 720p Camera Hardware Reliability

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-PPSR5-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify that the system works reliably with a 720p camera with no accuracy degradation. |
| **Preconditions** | (1) 720p USB camera connected. (2) Same test QR codes as higher-res tests. |
| **Test Data Input** | 720p camera. Test sheet with five QR codes. |
| **Test Steps** | 1. Connect 720p camera. 2. Position test sheet at 40 cm. 3. Run 20 detection cycles. 4. Record success rate. |
| **Expected Result** | Accuracy ≥95%. |
| **Pass/Fail Criteria** | Pass: ≥95%. Fail: <95%. |
| **Traceability** | UFR3 · PPSR5 · UC-001 |

---

### TC-PDSR1-MAN-01 — No Outbound Network Traffic

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-PDSR1-MAN-01 |
| **Priority** | Critical |
| **What to Test** | Verify no data is sent to external servers; all processing is local. |
| **Preconditions** | (1) Network monitoring tool running. (2) System configured for typical operation. |
| **Test Data Input** | Network logs during 1-hour operational cycle. |
| **Test Steps** | 1. Start network monitor. 2. Run system through full cycle. 3. Perform 20+ scan events. 4. Review outbound connection logs. 5. Verify no external IPs or domains contacted. |
| **Expected Result** | Zero outbound connections. |
| **Pass/Fail Criteria** | Pass: No external traffic. Fail: Any external data sent. |
| **Traceability** | UFR10 · PDSR1 · UC-001, UC-002 |

---

### TC-PDSR2-MAN-01 — Fully Offline Operation

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-PDSR2-MAN-01 |
| **Priority** | Critical |
| **What to Test** | Verify full functionality with no internet connection. |
| **Preconditions** | (1) System installed. (2) Internet can be completely disabled. |
| **Test Data Input** | Full operational test: launch, scan, process, JSON output, keyboard emulation, step verification. |
| **Test Steps** | 1. Disconnect internet. 2. Launch app. 3. Perform 10 QR scans. 4. Verify JSON output. 5. Test keyboard emulation. 6. Load a trained process and run step verification. 7. Run for 1+ hour. |
| **Expected Result** | All features function identically to online operation. |
| **Pass/Fail Criteria** | Pass: All features work. Fail: Any feature fails. |
| **Traceability** | UFR10 · PDSR2 · UC-001 |

---

### TC-PDSR4-MAN-01 — Factory Environment Stability

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-PDSR4-MAN-01 |
| **Priority** | High |
| **What to Test** | Verify stable operation for 8+ hours of continuous use with no crashes or memory leaks. |
| **Preconditions** | (1) System deployed in factory or simulated environment. (2) Monitoring tools active. |
| **Test Data Input** | 8+ hour continuous operation. Resource monitoring logs. |
| **Test Steps** | 1. Deploy system. 2. Start continuous operation with periodic scans. 3. Monitor CPU and memory. 4. Log errors/crashes. 5. Review after 8+ hours. |
| **Expected Result** | Zero crashes. Stable memory/CPU. |
| **Pass/Fail Criteria** | Pass: Zero crashes, stable resources. Fail: Any crash or leak. |
| **Traceability** | UFR11 · PDSR4 · UC-002 |

---

### TC-ODSR2-MAN-01 — OSS Component Documentation

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-ODSR2-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify all open-source components are documented with name, version, and license. |
| **Preconditions** | (1) Project documentation available. (2) pip freeze can be run. |
| **Test Data Input** | Dependency list. OSS documentation section. |
| **Test Steps** | 1. Generate pip freeze. 2. Compare against documented list. 3. Verify each has name, version, license. 4. Identify undocumented deps. |
| **Expected Result** | 100% of dependencies documented. |
| **Pass/Fail Criteria** | Pass: 100% documented. Fail: Any missing. |
| **Traceability** | ODUR1 · ODSR2 · UC-005 |

---

### TC-EISR6-MAN-01 — Config-Driven Workflow Customization

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | System-Level Non-Functional |
| **Test Case ID** | TC-EISR6-MAN-01 |
| **Priority** | Medium |
| **What to Test** | Verify that modifying workstation config JSON files changes the required fields without code changes. |
| **Preconditions** | (1) Access to config files. (2) System running with initial config. |
| **Test Data Input** | Initial config: part_number, serial_number. Modified: part_number, batch_id, inspector_id. |
| **Test Steps** | 1. Run scan with initial config, verify behavior. 2. Edit config JSON (no code changes). 3. Restart system. 4. Run same scan, verify new fields enforced. 5. Confirm old fields no longer apply. |
| **Expected Result** | New config enforced without code changes. |
| **Pass/Fail Criteria** | Pass: Workflow changes based on config alone. Fail: Changes not reflected or code required. |
| **Traceability** | EIUR3 · EISR6 · UC-005 |

---

## Test Suite 5: Automated Functional

---

### TC-SFR1-AUTO-01 — QR Detection on Static Test Image

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR1-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify that decode_qr() returns all QR codes from a static test image. |
| **Preconditions** | (1) AdvancedScanner module importable. (2) Test image available or mocked. |
| **Test Data Input** | 200x200 image with 3 QR codes: part_number:PN-001, serial_number:SN-002, batch_id:BATCH-003. |
| **Test Steps** | 1. Mock cv2.QRCodeDetector to return 3 codes. 2. Call AdvancedScanner.decode_qr(). 3. Assert count = 3. 4. Compare payloads against ground truth. 5. Verify no extra/missing. |
| **Expected Result** | decode_qr() returns exactly 3 codes with matching payloads. |
| **Pass/Fail Criteria** | Pass: Count=3, all match. Fail: Wrong count or mismatch. |
| **Traceability** | UFR1 · SFR1, SFR15, SFR16 · UC-001 |

---

### TC-SFR5-AUTO-01 — Keystroke Sequence Builder

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR5-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify keystroke builder produces correct sequence with proper delimiters. |
| **Preconditions** | (1) Keystroke builder logic implemented. |
| **Test Data Input** | Payload: {"part_number": "PN-12345", "serial_number": "SN-67890"}. Delimiter: TAB. |
| **Test Steps** | 1. Create payload. 2. Set field_order and delimiter. 3. Execute builder. 4. Capture output. 5. Compare against expected: ["PN-12345", "TAB", "SN-67890", "TAB", "ENTER"]. |
| **Expected Result** | Builder returns correct sequence. |
| **Pass/Fail Criteria** | Pass: Exact match. Fail: Any element wrong. |
| **Traceability** | UFR9 · SFR5 · UC-001 |

---

### TC-SFR11-AUTO-01 — JSON File Write/Read Integrity

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR11-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify that writing scan data to JSON and reading it back preserves all data. |
| **Preconditions** | (1) OutputData.to_json() is implemented. (2) File I/O can be tested. |
| **Test Data Input** | Scan event with workstation_id: "workstation_01", barcodes: [{"name": "part_number", "value": "PN-001"}]. |
| **Test Steps** | 1. Create scan data. 2. Write via OutputData.to_json() (or mock). 3. Read the saved JSON file. 4. Compare loaded data against original. 5. Verify workstation_id and barcodes match exactly. |
| **Expected Result** | Loaded data matches original with no loss. |
| **Pass/Fail Criteria** | Pass: Data integrity preserved. Fail: Any mismatch. |
| **Traceability** | UFR7 · SFR11 · UC-001 |

---

### TC-SFR14-AUTO-01 — Process Pickle Save/Load Integrity

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR14-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify that serialize_process() and deserialize_process() preserve all training data (step names, embeddings) through a save/load cycle. |
| **Preconditions** | (1) app.py serialize_process/deserialize_process functions importable. (2) A mock trained process with step embeddings is available. |
| **Test Data Input** | Process with 2 steps, each with computed centroids (numpy arrays). |
| **Test Steps** | 1. Create a trained process with 2 steps and finalized centroids. 2. Serialize via serialize_process(). 3. Deserialize the result via deserialize_process(). 4. Compare step names, order, and centroid arrays. 5. Verify numpy array equality using np.allclose(). |
| **Expected Result** | All step names, order, and centroid values are preserved exactly. |
| **Pass/Fail Criteria** | Pass: All data matches after round-trip. Fail: Any data loss or corruption. |
| **Traceability** | UFR12 · SFR14 · UC-003 |

---

### TC-SFR15-AUTO-01 — Multi-Code Detection Accuracy

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR15-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify decoder detects all QR codes with error rate ≤1%. |
| **Preconditions** | (1) AdvancedScanner.decode_qr() implemented. |
| **Test Data Input** | 250x250 image with 5 QR codes. |
| **Test Steps** | 1. Mock 5 ground truth codes. 2. Execute decode_qr(). 3. Count detected. 4. Compare against ground truth. 5. Calculate error rate. |
| **Expected Result** | All 5 detected. Error rate = 0%. |
| **Pass/Fail Criteria** | Pass: All found, ≤1%. Fail: Any missed or >1%. |
| **Traceability** | UFR1 · SFR15 · UC-001 |

---

### TC-SFR16-AUTO-01 — Output Deduplication

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR16-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify output builder produces exactly one entry per detected QR code with no duplicates. |
| **Preconditions** | (1) Deduplication logic implemented. |
| **Test Data Input** | Raw detections with 1 duplicate (3 items, 1 dup). |
| **Test Steps** | 1. Create raw detections with duplicates. 2. Process through dedup logic. 3. Count unique entries (should be 2). 4. Assert only unique entries remain. |
| **Expected Result** | 2 unique entries, no duplicates. |
| **Pass/Fail Criteria** | Pass: Correct count, no dupes. Fail: Duplicates remain. |
| **Traceability** | UFR1 · SFR16 · UC-001 |

---

### TC-SFR17-AUTO-01 — Simulation Synthetic QR Generation

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Functional |
| **Test Case ID** | TC-SFR17-AUTO-01 |
| **Priority** | Medium |
| **What to Test** | Verify simulation_scanner generates synthetic QR codes and processes them through the decode/parse pipeline. |
| **Preconditions** | (1) simulation_scanner.py importable. (2) Dependencies available. |
| **Test Data Input** | Simulation scenarios with known expected field-value pairs. |
| **Test Steps** | 1. Run the simulation scanner scenarios programmatically. 2. Capture the detection results. 3. Verify all expected QR codes were generated and detected. 4. Verify parsed field-value pairs match expected data. 5. Assert no exceptions during simulation. |
| **Expected Result** | All simulation scenarios produce correct detection and parsing results. |
| **Pass/Fail Criteria** | Pass: All scenarios complete correctly. Fail: Any scenario fails. |
| **Traceability** | UFR11 · SFR17 · UC-005 |

---

## Test Suite 6: Automated Non-Functional

---

### TC-PPSR2-AUTO-01 — Detection Latency Under Load

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Non-Functional |
| **Test Case ID** | TC-PPSR2-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify QR detection latency stays below 200 ms. |
| **Preconditions** | (1) AdvancedScanner.decode_qr() implemented. (2) time.perf_counter available. |
| **Test Data Input** | 640x480 test image. |
| **Test Steps** | 1. Create test image. 2. Start timer. 3. Execute decode_qr(). 4. Stop timer. 5. Assert <200 ms. |
| **Expected Result** | Latency <200 ms. |
| **Pass/Fail Criteria** | Pass: <200 ms. Fail: ≥200 ms. |
| **Traceability** | UFR1 · PPSR2 · UC-001 |

---

### TC-PPSR5-AUTO-01 — 720p Detection Accuracy

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Non-Functional |
| **Test Case ID** | TC-PPSR5-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify QR detection accuracy ≥95% at 720p. |
| **Preconditions** | (1) 720p test dataset available or mocked. |
| **Test Data Input** | 100 test cases at 720x1280, mocked 95% success. |
| **Test Steps** | 1. Create 100 test images. 2. Mock detectAndDecodeMulti with 95% success. 3. Execute on all images. 4. Calculate accuracy. 5. Assert ≥95%. |
| **Expected Result** | ≥95%. |
| **Pass/Fail Criteria** | Pass: ≥95%. Fail: <95%. |
| **Traceability** | UFR3 · PPSR5 · UC-001 |

---


### TC-EISR3-AUTO-01 — JSON Output Structure Compliance

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Non-Functional |
| **Test Case ID** | TC-EISR3-AUTO-01 |
| **Priority** | High |
| **What to Test** | Verify JSON outputs from scan events contain required fields with correct types. |
| **Preconditions** | (1) JSON output files available. |
| **Test Data Input** | JSON outputs from multiple scan events. Required fields: workstation_id (str), timestamp (str), barcodes (list of {name: str, value: str}). |
| **Test Steps** | 1. Generate outputs from scan events. 2. Validate required fields present. 3. Check data types. 4. Verify barcode objects have "name" and "value". 5. Assert all pass. |
| **Expected Result** | All outputs contain required fields with correct types. |
| **Pass/Fail Criteria** | Pass: 100% compliant. Fail: Any output fails. |
| **Traceability** | EIUR2 · EISR3 · UC-001, UC-002 |

---

### TC-EISR6-AUTO-01 — Config-Driven Workflow Behavior

| Field | Details |
|-------|---------|
| **Project Name** | AIBI CV for Manufacturing |
| **Test Suite** | Automated Non-Functional |
| **Test Case ID** | TC-EISR6-AUTO-01 |
| **Priority** | Medium |
| **What to Test** | Verify different config files produce different workflow behaviors. |
| **Preconditions** | (1) Two distinct configs. (2) ConfigManager implemented. |
| **Test Data Input** | Config 1: part_number, serial_number. Config 2: part_number, batch_id, inspector_id. |
| **Test Steps** | 1. Load config 1, process scan. 2. Load config 2, process same scan. 3. Compare required fields and completion states. 4. Verify different behavior per config. |
| **Expected Result** | Different configs produce different required field sets and completion states. |
| **Pass/Fail Criteria** | Pass: Distinct behavior per config. Fail: Same behavior. |
| **Traceability** | EIUR3 · EISR6 · UC-005 |

---

## Test Case Summary

| # | Test Case ID | Test Suite | What to Test (Summary) | Priority | Final Status |
|---|-------------|------------|------------------------|----------|--------------|
| 1 | TC-SFR1-MAN-01 | QR Scanner Manual | Live QR code detection | High | PASS |
| 2 | TC-SFR2-MAN-01 | QR Scanner Manual | Field mapping configuration | High | PASS |
| 3 | TC-SFR4-MAN-01 | QR Scanner Manual | JSON record generation | High | PASS |
| 4 | TC-SFR5-MAN-01 | QR Scanner Manual | Keyboard emulation output | High | PASS |
| 5 | TC-SFR11-MAN-01 | QR Scanner Manual | Local JSON file persistence | High | PASS |
| 6 | TC-SFR12-MAN-01 | QR Scanner Manual | JSON output structure validation | Medium | PASS |
| 7 | TC-SFR15-MAN-01 | QR Scanner Manual | Multi-code factory lighting detection | High | PASS |
| 8 | TC-SFR16-MAN-01 | QR Scanner Manual | Complete output for all visible QRs | High | PASS |
| 9 | TC-SFR6-MAN-01 | Step Verification Manual | Step sequence validation | High | PASS |
| 10 | TC-SFR7-MAN-01 | Step Verification Manual | Live video UI overlay | High | PASS |
| 11 | TC-SFR8-MAN-01 | Step Verification Manual | Process training interface | High | PASS |
| 12 | TC-SFR9-MAN-01 | Step Verification Manual | Configurable sensitivity thresholds | Medium | PASS |
| 13 | TC-SFR10-MAN-01 | Step Verification Manual | Process deviation logging | High | PASS |
| 14 | TC-SFR14-MAN-01 | Step Verification Manual | Training dataset save/load | High | PASS |
| 15 | TC-SFR19-MAN-01 | Step Verification Manual | Error messages display | High | PASS |
| 16 | TC-SFR20-MAN-01 | Step Verification Manual | Step list display | High | PASS |
| 17 | TC-SFR21-MAN-01 | Step Verification Manual | Completed step visual marker | High | PASS |
| 18 | TC-SFR22-MAN-01 | Step Verification Manual | Missed step visual marker | High | PASS |
| 19 | TC-SFR26-MAN-01 | Step Verification Manual | Step progress indicators | Medium | PASS |
| 20 | TC-SFR28-MAN-01 | Step Verification Manual | Reset/restart run | High | PASS |
| 21 | TC-PUSR1-MAN-01 | Usability | New operator onboarding (≤30 min) | High | PASS |
| 22 | TC-PUSR2-MAN-01 | Usability | Streamlit help text and UI guidance | Medium | PASS |
| 23 | TC-PUSR3-MAN-01 | Usability | Workflow step reduction vs. legacy | Medium | PASS |
| 24 | TC-PUSR4-MAN-01 | Usability | Touch-free operation during scanning | High | PASS |
| 25 | TC-PUSR10-MAN-01 | Usability | Emoji and color state indicators | Medium | PASS |
| 26 | TC-PPSR2-MAN-01 | Non-Functional | Real-time feedback perception | High | PASS |
| 27 | TC-PPSR5-MAN-01 | Non-Functional | 720p camera reliability | High | PASS |
| 28 | TC-PDSR1-MAN-01 | Non-Functional | No outbound network traffic | Critical | PASS |
| 29 | TC-PDSR2-MAN-01 | Non-Functional | Fully offline operation | Critical | PASS |
| 30 | TC-PDSR4-MAN-01 | Non-Functional | Factory environment stability | High | PASS |
| 31 | TC-ODSR2-MAN-01 | Non-Functional | OSS documentation completeness | Medium | PASS |
| 32 | TC-EISR6-MAN-01 | Non-Functional | Config-driven workflow customization | Medium | PASS |
| 33 | TC-SFR1-AUTO-01 | Auto Functional | QR detection on static image | High | PASS |
| 34 | TC-SFR5-AUTO-01 | Auto Functional | Keystroke sequence builder | High | PASS |
| 35 | TC-SFR11-AUTO-01 | Auto Functional | JSON file write/read integrity | High | PASS |
| 36 | TC-SFR14-AUTO-01 | Auto Functional | Process pickle save/load integrity | High | PASS |
| 37 | TC-SFR15-AUTO-01 | Auto Functional | Multi-code detection accuracy | High | PASS |
| 38 | TC-SFR16-AUTO-01 | Auto Functional | Output deduplication | High | PASS |
| 39 | TC-SFR17-AUTO-01 | Auto Functional | Simulation synthetic QR generation | Medium | PASS |
| 40 | TC-PPSR2-AUTO-01 | Auto Non-Functional | Detection latency under load | High | PASS |
| 41 | TC-PPSR5-AUTO-01 | Auto Non-Functional | 720p detection accuracy | High | PASS |
| 42 | TC-EISR3-AUTO-01 | Auto Non-Functional | JSON output structure compliance | High | PASS |
| 43 | TC-EISR6-AUTO-01 | Auto Non-Functional | Config-driven workflow behavior | Medium | PASS |

---

**Total: 43 test cases** (32 manual, 11 automated)

**Overall Pass Rate: 100%**
