## System Requirements (SR) for AIBI Computer Vision for Manufacturing

This document maps the user-level requirements into testable system requirements. It follows the same structure and presentation style as `Unified_Requirements_Analysis.md` so engineers and stakeholders can review SRs by category.

---

## System Functional Requirements

### SFR-1: Part Tracking and Barcode Management

#### SR-1.1: Multi-barcode detection and decoding (SR-1)
- Requirement: Fixed-station camera shall detect, decode, and output all 1D and 2D barcodes (e.g., Code128, EAN, QR) visible in a single frame, supporting 5–20 barcodes per capture.
- Details:
  - Support ~12 independent workstations (no conveyor assumed).
  - Handle paper with multiple barcodes presented within camera FOV.
  - Process 1D and 2D barcodes simultaneously.
  - Function when paper lies on table within camera view.
- Acceptance criteria:
  - Detects and decodes 5–20 barcodes per image with >=95% accuracy in controlled lighting and >=90% in representative factory lighting for target hardware.
  - Each decoded record contains barcode type, raw value, bounding box, confidence, timestamp, and workstation ID.
- Priority: Critical
- Source: Derived from UFR-1.1

#### SR-1.2: Configurable barcode field mapping (SR-2)
- Requirement: Provide per-workstation configurable mapping to assign barcode spatial positions to named data fields (part number, serial number, material batch, spool IDs).
- Details:
  - Support labeled zones (top-left/top-right), left-to-right or top-to-bottom ordering, and anchor point selection.
  - Persist mapping per workstation and version mappings.
  - Validate required fields and report missing fields.
- Acceptance criteria:
  - Mapping UI supports labeled zones, ordering rules, and anchor points.
  - Mapping applied to test images maps barcodes to fields per configuration in >=98% of cases.
- Priority: Critical
- Source: Derived from UFR-1.2

#### SR-1.3: Etched / visual identifier recognition (SR-3)
- Requirement: Recognize and extract etched/carved alphanumeric identifiers on large parts (mandrels) and return identifier, bounding box, and confidence.
- Details:
  - Support short codes (1–8 characters) containing numbers and uppercase letters.
  - Return an "unreadable" flag when confidence below threshold.
- Acceptance criteria:
  - Recognition accuracy >=92% on provided etched dataset under representative conditions.
- Priority: High
- Source: Derived from UFR-1.3

#### SR-1.4: Structured scan payload output (SR-4)
- Requirement: Aggregate decoded and recognized values into a structured JSON document per scan event containing timestamps, workstation ID, per-field values, mapping metadata, confidences, and image reference.
- Details:
  - Provide JSON schema and examples.
  - Include mapping version and processing status.
- Acceptance criteria:
  - JSON schema validates sample outputs with no errors.
- Priority: Critical
- Source: Derived from UFR-1.4, EI-2

#### SR-1.5: Real-time delivery and keyboard-emulation (SR-5)
- Requirement: Support real-time delivery via local REST API, local DB persistence, and keyboard-emulation mode for legacy KMD integration.
- Details:
  - Configurable per-workstation delivery mode.
  - Keyboard-emulation emits configured field sequence to focused input target.
- Acceptance criteria:
  - API median latency <100 ms for single-scan operations on local network.
  - DB write completes <250 ms under normal conditions.
  - Keyboard-emulation produces configured keystroke sequence reliably.
- Priority: Critical
- Source: Derived from UFR-1.4, UFR-3.1, EI-1

---

### SFR-2: Process Monitoring and Quality Assurance

#### SR-2.1: Manufacturing step detection & sequencing (SR-6)
- Requirement: Detect and report start/completion of defined manufacturing steps and validate configured sequence; flag skipped or out-of-sequence steps.
- Details:
  - Detect actions like cloth application, resin application, fiber winding.
  - Support per-process step definitions and temporal constraints.
- Acceptance criteria:
  - Step timestamps within +/-2s of human-annotated ground truth on validation videos.
  - Sequence violation alert triggered within 1s of detection; false positive rate <=3% on validation set.
- Priority: High
- Source: Derived from UFR-2.1, UFR-2.4

#### SR-2.2: Real-time operator feedback and alerts (SR-7)
- Requirement: Provide per-workstation UI overlay with live video, step progress indicators, visual status (green check/red alert), and optional audio alerts for violations.
- Details:
  - Visual indicators should be readable with PPE (gloves, goggles).
  - Audio alerts configurable and local to the workstation.
- Acceptance criteria:
  - UI updates <250 ms after event detection; audio alert plays <500 ms after trigger.
- Priority: High
- Source: Derived from UFR-2.2, PU-1, PU-2

#### SR-2.3: Training capture and annotation tool (SR-8)
- Requirement: Provide an in-situ capture tool for non-technical users to record reference video, mark step start/end, label steps, and save training sessions with metadata.
- Details:
  - Simple UI with preview playback and annotation controls.
  - Save metadata: workstation, part type, lighting, operator notes.
- Acceptance criteria:
  - Non-technical user completes capture + annotation + save within 3 minutes with no documentation.
- Priority: Medium
- Source: Derived from UFR-2.3

#### SR-2.4: Process validation tolerance and configurable sensitivity (SR-9, SR-17)
- Requirement: Models must tolerate natural worker variations (handedness, micro-variations) and provide configurable sensitivity per step to reduce nuisance alerts.
- Details:
  - Per-step sensitivity parameters and thresholds.
  - Retraining pipeline uses collected labeled data.
- Acceptance criteria:
  - Configurable tolerance reduces false positives by >=30% vs fixed threshold baseline while maintaining detection power for true skips.
- Priority: High
- Source: Derived from UFR-2.4, OD-1

---

### SFR-3: System Integration and Data Management

#### SR-3.1: Local intermediate storage and offline resilience (SR-10)
- Requirement: Persist scan and event data locally with audit metadata and support replay/synchronization when downstream systems are unavailable.
- Details:
  - Durable local storage with synchronization queue.
  - Recovery across restarts and power cycles.
- Acceptance criteria:
  - Local write latency <250 ms; queued records survive restarts and synchronize automatically on network restore.
- Priority: Medium
- Source: Derived from UFR-3.2

#### SR-3.2: JSON schema and data contract publication (SR-13)
- Requirement: Publish stable JSON schema and human-readable documentation for scan and event payloads including examples and required fields.
- Details:
  - Use a standard JSON Schema (draft-07 or later).
  - Provide example payloads and mapping metadata description.
- Acceptance criteria:
  - Schema file validates example payloads and is stored in repo/documentation.
- Priority: High
- Source: Derived from EI-2, UFR-3.1

#### SR-3.3: Verification harness / simulated workstation (SR-14)
- Requirement: Provide a simulated workstation environment to replay camera feeds, inject synthetic barcodes/etched IDs, and verify API/keyboard-emulation outputs before production deployment.
- Details:
  - Test scenarios and pass/fail reporting for critical flows.
- Acceptance criteria:
  - Harness can run test scenarios for multi-barcode decode, mapping, keyboard-emulation and produce pass/fail results.
- Priority: Medium
- Source: Derived from UFR-4.1

#### SR-3.4: Training dataset management & export (SR-15)
- Requirement: Provide tools and storage to capture, tag, version, and export labeled datasets for model training, including metadata (workstation, part type, lighting).
- Details:
  - Dataset manifests, versioning, exportable archives (tar/zip).
- Acceptance criteria:
  - Labeled datasets exportable with manifest and support simple queries by workstation/part.
- Priority: Medium
- Source: Derived from UFR-4.2

---

### SFR-4: Development, Deployment and Coexistence

#### SR-4.1: Legacy coexistence and phased deployment (SR-18)
- Requirement: Support phased deployment modes running in parallel with existing barcode scanners and provide rollback controls; pilot mode logs both KMD input and system output for correlation.
- Details:
  - Per-workstation enable/disable controls; pilot logging mode.
- Acceptance criteria:
  - Enable/disable per workstation with no data loss; pilot mode captures correlation logs.
- Priority: Medium
- Source: Derived from OO-3, EI-3

#### SR-4.2: Operator UI simplicity & internationalization (SR-19)
- Requirement: UI shall use simple iconography, color coding, and minimal text to accommodate diverse language proficiencies and provide clear workflows for non-technical staff.
- Details:
  - Localizable resources and icon sets.
  - Minimal text and clear steps for common tasks (mapping, capture).
- Acceptance criteria:
  - Non-technical users complete core tasks in UAT with minimal instruction.
- Priority: Medium
- Source: Derived from PU-3, PU-4

---

## System Non-Functional Requirements

These entries capture performance, reliability, security, and operational constraints.

### SNFR-P: Performance & Latency

#### SR-P1: Real-time processing and response (SNFR) (SR-5, SR-16)
- Requirement: Provide real-time barcode/process detection and feedback with low latency to prevent manufacturing errors.
- Details:
  - End-to-end median latencies for API and UI updates documented per hardware tier.
- Acceptance criteria:
  - API median latency <100 ms for single-scan operations on local network; UI update <250 ms after event detection.
- Priority: Critical
 - Source: Derived from PP-1, PP-2

#### SR-P2: Low-cost camera tolerance (SNFR) (SR-12)
- Requirement: Operate on low-cost cameras and constrained edge devices with documented hardware profiles and fallbacks.
- Details:
  - Minimum supported camera resolutions and recommended lighting guidelines.
- Acceptance criteria:
  - System runs at >=5 FPS on documented low-cost hardware with usable detection performance.
- Priority: Medium
 - Source: Derived from PP-3, OO-1

### SNFR-S: Security, Data Sovereignty & Audit

#### SR-S1: On-premise deployment and data security (SNFR) (SR-11)
- Requirement: All processing and storage shall remain on-premises by default; telemetry/external calls disabled unless explicitly enabled by an admin.
- Details:
  - Documented administrative controls for enabling external integrations.
- Acceptance criteria:
  - No outbound cloud connections in default configuration; any external interface requires explicit admin toggle and documented risks.
- Priority: Critical
 - Source: Derived from PD-1

#### SR-S2: Audit trail and compliance logging (SNFR) (SR-20)
- Requirement: Produce an immutable audit trail of scan and process events with timestamps, operator ID (if available), mapping versions, and integrity checks.
- Details:
  - Append-only logs or DB with cryptographic checksums or write-once semantics.
- Acceptance criteria:
  - Audit trail contains required fields and can be exported; logs retain integrity across restarts and backups.
- Priority: High
 - Source: Derived from PD-1, UFR-3.2

### SNFR-O: Operational & Organizational

#### SR-O1: Open-source toolchain & retraining pipeline (SNFR) (SR-17)
- Requirement: Use open-source toolchains where practical and provide a documented retraining pipeline for model updates using collected labeled data.
- Details:
  - Reproducible pipeline for producing model artifacts and deployment instructions.
- Acceptance criteria:
  - Pipeline documented and produces reproducible artifacts using open-source tools.
- Priority: Medium
 - Source: Derived from OD-1, UFR-2.3

#### SR-O2: Cost optimization and deployment flexibility (SNFR) (SR-12, SR-18)
- Requirement: Provide deployment options that balance edge vs. centralized processing for cost optimization and flexible workstation configurations.
- Details:
  - Hardware tiers, recommended configurations, and trade-offs.
- Priority: Medium
 - Source: Derived from OO-1, OO-3

---

## Traceability (UFR -> SR)

- UFR-1.1 -> SR-1.1
- UFR-1.2 -> SR-1.2
- UFR-1.3 -> SR-1.3
- UFR-1.4 -> SR-1.4, SR-1.5
- UFR-2.1 -> SR-2.1
- UFR-2.2 -> SR-2.2
- UFR-2.3 -> SR-2.3, SR-O1
- UFR-2.4 -> SR-2.1, SR-2.4
- UFR-3.1 -> SR-1.5, SR-3.2
- UFR-3.2 -> SR-3.1, SR-S2
- UFR-4.1 -> SR-3.3
- UFR-4.2 -> SR-3.4

## Assumptions

- System will be deployed on-premises (customer network) and primary processing is Python-based (Ubuntu servers or supported edge devices), per UFR guidance.
- Target cameras include low-cost USB or Raspberry Pi camera modules; recommended camera specs will be documented separately.
- KMD integration uses keyboard-emulation or local API; KMD changes are not assumed.

## Next steps / Recommendations

1. Add short, runnable acceptance test definitions and test-data descriptions for each SR (todo-2).
2. Create a JSON Schema stub for the scan/event payload (SR-1.4 / SR-3.2).
3. Implement a small verification harness (SR-3.3) to exercise SFR critical flows.
4. Produce operator UI mockups and quick training capture demo for UAT.

---

Document updated to Unified-style SR presentation. If you want, I can now: (A) add the per-SR concise acceptance tests, or (B) create the JSON Schema file next. Tell me which to do first.
