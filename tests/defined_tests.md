Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR1-MAN-01
What to Test	Verify that the live camera feed detects and decodes all visible QR codes within the camera's field of view in real time.
Test Data Input	Printed QR codes placed in camera FOV.
Expected
Result	All visible codes appear in UI/output.
Traceability	Relevant User Req.(s)	UFR1
	Relevant System Req.(s)	SFR1, SFR15, SFR16
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR2-MAN-01
What to Test	Verify that an admin can configure options through the workstation config so decoded QR values map to the correct logical fields.
Test Data Input	Workstation config with fields: "workstation_id": "workstation_11",  "expected_qr_count": 6,  "scan_direction": "row-major",  "append_key": "None",  "camera_index": 0
Expected
Result	Output JSON contains "workstation_id": "workstation_11",  "expected_qr_count": 6,  "scan_direction": "row-major",  "append_key": "None",  "camera_index": 0
Traceability	Relevant User Req.(s)	UFR2
	Relevant System Req.(s)	SFR2
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR4-MAN-01
What to Test	Verify that a live scan event produces a single, correct JSON file containing all scanned data and metadata.
Test Data Input	QR Codes. Config file.
Expected
Result	One JSON record created with all data and metadata.
Traceability	Relevant User Req.(s)	UFR1, UFR4
	Relevant System Req.(s)	SFR4, SFR11
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR5-MAN-01
What to Test	Verify that keyboard-emulation mode outputs correct keystrokes to a target application (e.g., Excel) after a live scan.
Test Data Input	Live scan and excel field in focus.
Expected
Result	Excel displays correct values in order with configured delimiters.
Traceability	Relevant User Req.(s)	UFR9
	Relevant System Req.(s)	SFR5, SFR18
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR11-MAN-01
What to Test	Verify that every scan event generates a JSON file persisted to the local output directory with no data loss.
Test Data Input	Five consecutive scan events with distinct QR code payloads.
Expected
Result	Exactly five JSON files present with correct, matching payloads and sequential timestamps.
Traceability	Relevant User Req.(s)	UFR7
	Relevant System Req.(s)	SFR11, PDSR1 
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR12-MAN-01
What to Test	Verify that JSON output files contain all required fields with correct data types matching the expected structure.
Test Data Input	Three JSON output files from different scans.
Expected
Result	All files contain required fields with correct data types.
Traceability	Relevant User Req.(s)	UFR4
	Relevant System Req.(s)	SFR12, EISR3 
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR15-MAN-01
What to Test	Verify that the system decodes all QR codes on a multi-code test sheet under typical factory lighting.
Test Data Input	Printed QR sheet with known values
Expected
Result	All five codes decoded correctly across all conditions.
Traceability	Relevant User Req.(s)	UFR1
	Relevant System Req.(s)	SFR15
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	QR Scanner Manual Functional
Test Case ID	TC-SFR16-MAN-01
What to Test	Verify that the system output includes exactly one entry per visible QR code with no missed codes or duplicates.
Test Data Input	Live multi-code scan.
Expected
Result	Exactly three entries, one per visible code, no duplicates.
Traceability	Relevant User Req.(s)	UFR1
	Relevant System Req.(s)	SFR16
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	System/Manual Functional
Test Case ID	TC-SFR18-MAN-01
What to Test	Simulation produces correct keyboard-emulation output.
Test Data Input	Simulation scenario and sandbox text field.
Expected
Result	Typed text matches expected sequence.
Traceability	Relevant User Req.(s)	UFR11
	Relevant System Req.(s)	SFR18
	Relevant Use Case.(s)	UC-005

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR6-MAN-01
What to Test	Verify that the system correctly detects when manufacturing steps are performed in the correct sequence and flags out-of-order or skipped steps.
Test Data Input	Trained process with steps: "Step A", "Step B", "Step C". Operator performs steps in correct order, then in wrong order.
Expected
Result	Correct-order steps transition through IDLE → CORRECT_STEP → CONFIRMED. Out-of-order steps trigger WRONG_ORDER/SKIPPED state with logging.
Traceability	Relevant User Req.(s)	UFR5
	Relevant System Req.(s)	SFR6, SFR10, PPSR4
	Relevant Use Case.(s)	UC-002





Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR7-MAN-01
What to Test	Verify that the Streamlit UI displays a live camera feed with real-time overlay showing current step status, confidence scores, and progress indicators.
Test Data Input	Normal operation with a trained process containing 3+ steps.
Expected
Result	Live feed displays with accurate step name, confidence score, and progress bar.
Traceability	Relevant User Req.(s)	UFR6 
	Relevant System Req.(s)	SFR7, SFR26
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR8-MAN-01
What to Test	Verify that a user can define process steps, record reference frames, and save a trained process using the Training mode.
Test Data Input	New process with three steps
Expected
Result	All three steps are defined, frames recorded, embeddings computed, and process saved as .pkl.
Traceability	Relevant User Req.(s)	UFR8, UFR12 
	Relevant System Req.(s)	SFR8, SFR14
	Relevant Use Case.(s)	UC-003

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR9-MAN-01
What to Test	Verify that adjusting the similarity threshold, window size, and required votes sliders changes the system's detection behavior.
Test Data Input	Default threshold (0.75), then adjusted to 0.9 (strict) and 0.3 (loose).
Expected
Result	Higher thresholds require more precise matches; lower thresholds accept looser matches.
Traceability	Relevant User Req.(s)	UFR8
	Relevant System Req.(s)	SFR9
	Relevant Use Case.(s)	UC-002, UNC-003

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR10-MAN-01
What to Test	Verify that the system logs every detected deviation (wrong order, skipped step) with step name and violation type in the run history.
Test Data Input	3-step process where operator skips step 2 and jumps to step 3.
Expected
Result	Run history shows the violation entry with correct details.
Traceability	Relevant User Req.(s)	UFR7
	Relevant System Req.(s)	SFR10
	Relevant Use Case.(s)	UC-002


Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR14-MAN-01
What to Test	Verify that a trained process can be saved as a .pkl file and loaded back with all step data intact.
Test Data Input	Trained process with steps: "Step A" (with embeddings), "Step B" (with embeddings).
Expected
Result	Loaded process contains all original steps with functional embeddings.
Traceability	Relevant User Req.(s)	UFR12
	Relevant System Req.(s)	SFR14
	Relevant Use Case.(s)	UC-003

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR19-MAN-01
What to Test	Verify that the system displays clear error messages on screen for all process errors (WRONG_ORDER, SKIPPED steps).
Test Data Input	Operator deliberately triggers a sequence violation.
Expected
Result	A visible warning or error message appears on screen identifying the violation type and step.
Traceability	Relevant User Req.(s)	UFR13
	Relevant System Req.(s)	SFR19
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR20-MAN-01
What to Test	Verify that the UI displays a complete checklist of all process steps during Operation mode.
Test Data Input	Process with 4 steps.
Expected
Result	All steps are listed with correct names in the correct order.
Traceability	Relevant User Req.(s)	UFR14
	Relevant System Req.(s)	SFR20
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR21-MAN-01
What to Test	Verify that completed steps display a green checkmark visual marker in the step list.
Test Data Input	3-step process.
Expected
Result	Correct visual indicators are shown
Traceability	Relevant User Req.(s)	UFR15
	Relevant System Req.(s)	SFR21
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR22-MAN-01
What to Test	Verify that skipped or missed steps display a red indicator in the step list.
Test Data Input	3-step process where step 2 is skipped.
Expected
Result	Skipped step displays a distinct visual indicator clearly identifying it as missed.
Traceability	Relevant User Req.(s)	UFR15
	Relevant System Req.(s)	SFR22
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR26-MAN-01
What to Test	Verify that the UI displays progress indicators showing voting status (e.g., votes/required) during step verification.
Test Data Input	Window size: 5, Required votes: 3.
Expected
Result	Progress indicator shows current votes vs. required (e.g., "2/3 votes").
Traceability	Relevant User Req.(s)	UFR6
	Relevant System Req.(s)	SFR26
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Step Verification Manual Functional
Test Case ID	TC-SFR28-MAN-01
What to Test	Verify that the restart button resets the step verification state to prepare for the next part/run.
Test Data Input	A process where 2 of 3 steps have been completed.
Expected
Result	All step states reset. Current step returns to step 1. Previous run preserved in history.
Traceability	Relevant User Req.(s)	UFR20
	Relevant System Req.(s)	SFR28
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Usability and Operator Workflow
Test Case ID	TC-PUSR1-MAN-01
What to Test	Verify that a new operator with no prior experience can complete the basic scanning workflow within 30 minutes.
Test Data Input	New user, pre-configured workstation, task checklist: launch app, perform scan, verify output, configure field mapping.
Expected
Result	Operator completes all tasks within 30 minutes.
Traceability	Relevant User Req.(s)	UFR8
	Relevant System Req.(s)	PUUR1 · PUSR1
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Usability and Operator Workflow
Test Case ID	TC-PUSR2-MAN-01
What to Test	Verify that the Streamlit UI provides adequate help text (slider descriptions, st.info messages, button labels) for users to understand major functions.
Test Data Input	System UI. Questionnaire listing 8 major controls: mode selector, record button, stop button, finalize button, save button, load button, restart button, threshold sliders.
Expected
Result	User correctly identifies ≥ 75% of controls (≥ 6 of 8).
Traceability	Relevant User Req.(s)	PUUR1
	Relevant System Req.(s)	PUSR2
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Usability and Operator Workflow
Test Case ID	TC-PUSR3-MAN-01
What to Test	Verify that the new system requires fewer manual steps than the legacy workflow.
Test Data Input	Legacy documentation. Same task on both systems (scan three parts, record data).
Expected
Result	New system requires fewer manual steps (≥25% reduction).
Traceability	Relevant User Req.(s)	UFR8
	Relevant System Req.(s)	PUSR3
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Usability and Operator Workflow
Test Case ID	TC-PUSR4-MAN-01
What to Test	Verify that the operator rarely needs to touch the UI during a typical QR scan cycle.
Test Data Input	10 consecutive scan cycles.
Expected
Result	Average ≤ 2 UI interactions per cycle.
Traceability	Relevant User Req.(s)	PUUR2
	Relevant System Req.(s)	PUSR4 
	Relevant Use Case.(s)	UC-001, UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Usability and Operator Workflow
Test Case ID	TC-PUSR10-MAN-01
What to Test	Verify that users can correctly interpret step status from the emoji markers and color-coded overlays (green/red) used in the UI.
Test Data Input	Screenshots showing: all-pending state, mid-progress state, violation state.
Expected
Result	Users correctly identify step states ≥ 85% of the time.
Traceability	Relevant User Req.(s)	PUUR4, PUUR1
	Relevant System Req.(s)	PUSR10
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-PPSR2-MAN-01
What to Test	Verify that feedback appears immediate, operator perceives no delay during scanning or step verification.
Test Data Input	10 consecutive scan/verification cycles. Stopwatch or system logging.
Expected
Result	Response time <500 ms. Operator reports no perceived delay.
Traceability	Relevant User Req.(s)	UFR1 
	Relevant System Req.(s)	PPSR2
	Relevant Use Case.(s)	UC-001, UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-PPSR5-MAN-01
What to Test	Verify that the system works reliably with a 720p camera with no accuracy degradation.
Test Data Input	720p camera. Test sheet with five QR codes.
Expected
Result	Accuracy ≥95%.
Traceability	Relevant User Req.(s)	UFR3
	Relevant System Req.(s)	PPSR5
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-PDSR1-MAN-01
What to Test	Verify no data is sent to external servers; all processing is local.
Test Data Input	Network logs during 1-hour operational cycle.
Expected
Result	Zero outbound connections.
Traceability	Relevant User Req.(s)	UFR10
	Relevant System Req.(s)	PDSR1
	Relevant Use Case.(s)	UC-001, UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-PDSR2-MAN-01
What to Test	TC-PDSR2-MAN-01
Test Data Input	Full operational test: launch, scan, process, JSON output, keyboard emulation, step verification.
Expected
Result	All features function identically to online operation.
Traceability	Relevant User Req.(s)	UFR10
	Relevant System Req.(s)	PDSR2
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-PDSR4-MAN-01
What to Test	Verify stable operation for 8+ hours of continuous use with no crashes or memory leaks.
Test Data Input	8+ hour continuous operation. Resource monitoring logs.
Expected
Result	Zero crashes. Stable memory/CPU.
Traceability	Relevant User Req.(s)	UFR11
	Relevant System Req.(s)	PDSR4
	Relevant Use Case.(s)	UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-ODSR2-MAN-01
What to Test	Verify all open-source components are documented with name, version, and license.
Test Data Input	Dependency list. OSS documentation section.
Expected
Result	100% of dependencies documented.
Traceability	Relevant User Req.(s)	ODUR1 
	Relevant System Req.(s)	ODSR2
	Relevant Use Case.(s)	UC-005

Project Name	AIBI CV for Manufacturing
Test Suite	System-Level Non-Functional
Test Case ID	TC-EISR6-MAN-01
What to Test	Verify that modifying workstation config JSON files changes the required fields without code changes.
Test Data Input	Initial config: part_number, serial_number. Modified: part_number, batch_id, inspector_id.
Expected
Result	New config enforced without code changes.
Traceability	Relevant User Req.(s)	EIUR3 
	Relevant System Req.(s)	EISR6 
	Relevant Use Case.(s)	UC-005

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR1-AUTO-01
What to Test	Verify that decode_qr() returns all QR codes from a static test image.
Test Data Input	200x200 image with 3 QR codes: part_number:PN-001, serial_number:SN-002, batch_id:BATCH-003.
Expected
Result	decode_qr() returns exactly 3 codes with matching payloads.
Traceability	Relevant User Req.(s)	UFR1 
	Relevant System Req.(s)	SFR1, SFR15, SFR16
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR5-AUTO-01
What to Test	Verify keystroke builder produces correct sequence with proper delimiters.
Test Data Input	Payload: {"part_number": "PN-12345", "serial_number": "SN-67890"}. Delimiter: TAB.
Expected
Result	Builder returns correct sequence.
Traceability	Relevant User Req.(s)	UFR9
	Relevant System Req.(s)	SFR5
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR11-AUTO-01
What to Test	Verify that writing scan data to JSON and reading it back preserves all data.
Test Data Input	Scan event with workstation_id: "workstation_01", barcodes: [{"name": "part_number", "value": "PN-001"}].
Expected
Result	Loaded data matches original with no loss.
Traceability	Relevant User Req.(s)	UFR7
	Relevant System Req.(s)	SFR11
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR14-AUTO-01
What to Test	Verify that serialize_process() and deserialize_process() preserve all training data (step names, embeddings) through a save/load cycle.
Test Data Input	Process with 2 steps, each with computed centroids (numpy arrays).
Expected
Result	All step names, order, and centroid values are preserved exactly.
Traceability	Relevant User Req.(s)	UFR12
	Relevant System Req.(s)	SFR14
	Relevant Use Case.(s)	UC-003

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR15-AUTO-01
What to Test	Verify decoder detects all QR codes with error rate ≤1%.
Test Data Input	250x250 image with 5 QR codes.
Expected
Result	All 5 detected. Error rate = 0%.
Traceability	Relevant User Req.(s)	UFR1
	Relevant System Req.(s)	SFR15
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR16-AUTO-01
What to Test	Verify output builder produces exactly one entry per detected QR code with no duplicates.
Test Data Input	Raw detections with 1 duplicate (3 items, 1 dup).
Expected
Result	2 unique entries, no duplicates.
Traceability	Relevant User Req.(s)	UFR1 
	Relevant System Req.(s)	SFR16
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Functional
Test Case ID	TC-SFR17-AUTO-01
What to Test	Verify simulation_scanner generates synthetic QR codes and processes them through the decode/parse pipeline.
Test Data Input	Simulation scenarios with known expected field-value pairs.
Expected
Result	All simulation scenarios produce correct detection and parsing results.
Traceability	Relevant User Req.(s)	UFR11
	Relevant System Req.(s)	SFR17
	Relevant Use Case.(s)	UC-005

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Non-Functional
Test Case ID	TC-PPSR2-AUTO-01
What to Test	Verify QR detection latency stays below 200 ms.
Test Data Input	640x480 test image.
Expected
Result	Latency <200 ms.
Traceability	Relevant User Req.(s)	UFR1
	Relevant System Req.(s)	PPSR2
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Non-Functional
Test Case ID	TC-PPSR5-AUTO-01
What to Test	Verify QR detection accuracy ≥95% at 720p.
Test Data Input	100 test cases at 720x1280, mocked 95% success.
Expected
Result	≥95%.
Traceability	Relevant User Req.(s)	UFR3 
	Relevant System Req.(s)	PPSR5
	Relevant Use Case.(s)	UC-001

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Non-Functional
Test Case ID	TC-EISR3-AUTO-01
What to Test	Verify JSON outputs from scan events contain required fields with correct types.
Test Data Input	JSON outputs from multiple scan events. Required fields: workstation_id (str), timestamp (str), barcodes (list of {name: str, value: str}).
Expected
Result	All outputs contain required fields with correct types.
Traceability	Relevant User Req.(s)	EIUR2
	Relevant System Req.(s)	EISR3
	Relevant Use Case.(s)	UC-001, UC-002

Project Name	AIBI CV for Manufacturing
Test Suite	Automated Non-Functional
Test Case ID	TC-EISR6-AUTO-01
What to Test	Automated export to MES/ERP.
Test Data Input	Config 1: part_number, serial_number. Config 2: part_number, batch_id, inspector_id.
Expected
Result	Different configs produce different required field sets and completion states.
Traceability	Relevant User Req.(s)	EIUR3
	Relevant System Req.(s)	EISR6
	Relevant Use Case.(s)	UC-005
