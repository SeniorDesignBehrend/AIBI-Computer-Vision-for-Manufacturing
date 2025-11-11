# DEPRECATED — System_Requirements_from_UFR.md

This file has been merged into `System_Requirements.md` and is deprecated. Please use `Requirements/System_Requirements.md` as the single source of truth for system requirements.

The original contents were a direct mapping from `Unified_Requirements_Analysis.md` and have been consolidated into the master SR document.

---

### SR-1.1: Fixed-station multi-barcode detection
- Requirement: A fixed camera at each workstation shall detect and decode multiple 1D and 2D barcodes present on a paper or object within the camera's field of view; support 5–20 barcodes per capture.
- Derived from: UFR-1.1
- Priority: Critical

### SR-1.2: Per-workstation configurable barcode-to-field mapping
- Requirement: Provide a per-workstation configuration UI to map barcode spatial positions to named data fields (part number, serial number, material batch, spool IDs), supporting positional patterns and ordering rules.
- Derived from: UFR-1.2
- Priority: Critical

### SR-1.3: Etched identifier recognition for non-barcodeable parts
- Requirement: Recognize etched/carved alphanumeric identifiers (short strings) on large parts and mandrels and return recognized text, bounding box, and confidence.
- Derived from: UFR-1.3
- Priority: High

### SR-1.4: Structured JSON scan output and KMD integration support
- Requirement: Aggregate decoded values into structured JSON payloads including timestamps, workstation ID, field mapping metadata, and confidence scores. Provide local API delivery, local DB persistence, and keyboard-emulation output mode for KMD compatibility.
- Derived from: UFR-1.4, UFR-3.1
- Priority: Critical

---

## SFR-2: Process Monitoring and Quality Assurance

### SR-2.1: Manufacturing step detection and sequencing
- Requirement: Detect start and completion events for defined manufacturing steps and validate that steps occur in the configured sequence; flag skipped or out-of-sequence steps.
- Derived from: UFR-2.1
- Priority: High

### SR-2.2: Real-time process feedback and alerts
- Requirement: Provide immediate visual (UI overlay) and audio alerts for process status and sequence violations; display step progress indicators.
- Derived from: UFR-2.2
- Priority: High

### SR-2.3: Simple process training interface
- Requirement: Provide a simple UI for non-technical users to record reference videos, mark step start/end points, label steps, and persist training sessions with metadata.
- Derived from: UFR-2.3
- Priority: Medium

### SR-2.4: Process validation with configurable tolerance
- Requirement: Allow configurable tolerances in process validation to account for worker variation (handedness, micro-variations) and avoid nuisance alerts.
- Derived from: UFR-2.4
- Priority: High

### SR-2.5: Log and notify incorrect/out-of-sequence steps
- Requirement: Log every detected incorrect, skipped, or out-of-sequence manufacturing step with timestamps, image/frame reference, detected step, expected step, and confidence. Provide configurable delivery of these logs/alerts to company local endpoints (local API, syslog, or message queue).
- Details:
	- Persist logs locally with audit metadata; must survive restarts.
	- Notification channels configurable per site; default to local persistent store.
	- No cloud-dependent notifications by default.
- Acceptance criteria:
	- Log records created within 250 ms containing required fields for each incorrect event.
	- Configured local endpoints receive notification payloads; failures are queued and retried.
- Derived from: UFR-2.4, UFR-3.1
- Priority: High
---

## SFR-3: System Integration and Data Management

### SR-3.1: Local API and database for integration
- Requirement: Expose a local REST API for real-time delivery and write scan results to a local database for intermediate persistence and offline recovery.
- Derived from: UFR-3.1, UFR-3.2
- Priority: Critical

### SR-3.2: Intermediate data storage and audit trail
- Requirement: Store scan and event data locally with timestamps, workstation identifiers, and mapping metadata; support replay and synchronization for downstream systems when network is restored.
- Derived from: UFR-3.2
- Priority: Medium

---

## SFR-4: Development and Testing Support

### SR-4.1: Simulated workstation / verification harness
- Requirement: Provide a simulated workstation environment for development/testing that can replay camera feeds, inject synthetic barcodes/etched IDs, and validate API/keyboard-emulation outputs.
- Derived from: UFR-4.1
- Priority: Medium

### SR-4.2: Training dataset capture and management
- Requirement: Provide tools and storage for capturing, tagging, versioning, and exporting training datasets (videos/images and labels) with metadata for model retraining.
- Derived from: UFR-4.2
- Priority: Medium

---

## Cross-cutting Non-Functional System Requirements

### SNFR-1: Usability and hands-free operation
- Requirement: The system shall be usable by factory workers wearing PPE with minimal training; detection should be automatic when objects enter FOV and require minimal physical interaction.
- Derived from: PU-1, PU-2
- Priority: Critical

### SNFR-2: Performance and real-time response
- Requirement: The system shall provide low-latency processing for barcode decoding and step validation; end-to-end API median latency should be documented and meet target thresholds for local deployments.
- Derived from: PP-1
- Priority: Critical

### SNFR-3: Accuracy and robustness

### SNFR-4: Edge-device and low-cost camera support
- Priority: Medium

### SNFR-5: On-premises data sovereignty and security
- Derived from: PD-1
### SNFR-6: Audit trail and compliance logging
- Requirement: Produce an immutable audit trail of scan and process events with timestamps, operator IDs, mapping versions, and integrity checks for compliance.
### SNFR-7: Open-source toolchain preference
- Requirement: Prefer open-source libraries and toolchains (MIT/Apache) for model training and deployment; document license considerations.
- Derived from: OD-1
- Priority: Medium

### SNFR-8: Phased deployment and coexistence with legacy systems
- Requirement: Support phased deployment, pilot modes, and coexistence with existing barcode scanners; provide rollback controls and dual-logging for correlation.
- Derived from: OO-3, EI-1
- Priority: Medium

---

## Traceability

- See `Unified_Requirements_Analysis.md` for original user requirement text and sources. Each SR above includes the UFR it was derived from.

---

Document created from `Unified_Requirements_Analysis.md`.
