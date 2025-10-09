# Requirements Analysis - CompositeFlex / AIBI Computer Vision for Manufacturing
**Meeting Date:** October 2nd, 2025
**Source:** October 2 meeting notes (summary & transcript)

---

## User Functional Requirements

### UFR-1: Part Tracking (Barcode Scanning)

#### UFR-1.1: Fixed-station Barcode Scanning
- **Requirement:** Fixed camera at each workstation must detect and read multiple barcodes from a paper or object that is presented within the camera's view.
- **Details:** There are ~12 workstations (no conveyor); the paper travels with the part and will be shown to the fixed camera when the part arrives at a station.
- **Source:** "Fixed camera at each station to scan paper with multiple barcodes" (Oct 2 summary)

#### UFR-1.2: Barcode Field Mapping
- **Requirement:** Provide a configurable mapping from barcode positions on the paper (or positional detection) to data fields (part number, serial number, material batch fields, spool IDs, etc.).
- **Details:** The system should allow per-workstation configuration to determine which barcodes are required/expected at that station and how to map them into the target system fields.
- **Source:** "Need to develop configurable system to map barcode positions to data fields" (Oct 2 summary)

#### UFR-1.3: Multi-barcode Aggregation Output
- **Requirement:** Aggregate all decoded barcode values into a single structured payload (JSON) for integration with KMD or other downstream systems.
- **Details:** Include timestamps, workstation ID, and field mapping metadata.
- **Source:** "Output likely JSON string with scanned data to integrate with KMD software" (Oct 2 summary)

### UFR-2: Process Monitoring (Human Activity Monitoring)

#### UFR-2.1: Step Detection and Sequencing
- **Requirement:** Detect if manufacturing steps are performed in the correct order for each workstation (e.g., cloth wrapping, resin application, fiber winding).
- **Details:** Focus on steps and process sequence—not necessarily final part quality. Detect start/end of each step.
- **Source:** "AI to detect if steps are performed in correct order" (Oct 2 summary)

#### UFR-2.2: Simple Training UI for Process Steps
- **Requirement:** Provide a simple UI that allows non-technical users (engineers, operators) to capture a video of correct process and mark start/end of steps to train the system.
- **Details:** Should allow training on the production floor with engineering assistance as needed.
- **Source:** "Need simple UI for training system on correct process steps" (Oct 2 summary)

#### UFR-2.3: Real-time Alerts and UI Feedback
- **Requirement:** Provide real-time feedback (visual indicators/alerts) when a step is skipped or performed out of order.
- **Details:** Minimal UI showing current step, completed steps, and alerts for out-of-sequence operations.
- **Source:** Implied from Oct 2 discussion and Oct 19 notes

### UFR-3: Integration and Data Flow

#### UFR-3.1: Local API / Network Integration with KMD
- **Requirement:** Provide an on-prem API or network-based method to deliver scanned data to KMD software or an intermediate database table for KMD to consume.
- **Details:** KMD currently accepts keyboard-style barcode input; system must either emulate that input or provide an API endpoint/local database that KMD can read.
- **Source:** "KMD software currently uses barcode scanners as keyboard input; Need to develop API or local network communication" (Oct 2 summary)

#### UFR-3.2: Data Persistence / Intermediate Storage
- **Requirement:** Optionally write scan results to an intermediate store (database table) to decouple CV processing and KMD reads.
- **Details:** Include timestamps, station id, serial/part references, and mapped field indicators.
- **Source:** "Consider database table for intermediate data storage" (Oct 2 summary)

### UFR-4: Testing and Training Environment

#### UFR-4.1: Simulated Testing Workstation
- **Requirement:** Provide a simulated workstation environment for initial testing and validation before production floor testing (since CompositeFlex has no dedicated test environment).
- **Details:** Simple setup that mimics camera view and KMD fields for iterative development.
- **Source:** "No dedicated test environment at CompositeFlex; Team should create simulated workstation for initial testing" (Oct 2 summary)

---

## Non-functional Requirements

### Product: Usability Requirements

#### PU-1: Non-technical Training Interface
- **Requirement:** Training UI must be easy to use by non-technical staff to capture and label process steps.
- **Details:** Minimal clicks, clear step labeling, and in-situ capture capability.
- **Source:** "Develop easy-to-use interface for non-technical workers to train system" (Oct 2 summary)

#### PU-2: Minimal Operator Burden
- **Requirement:** Minimize additional work for operators during normal production; the system should integrate into existing flow with little extra action.
- **Source:** "We will try to work with them to see what kind of movement they're doing naturally" (Oct 2 transcript)

### Product: Performance Requirements

#### PP-1: Low-cost Camera Tolerance
- **Requirement:** Tolerate lower-quality (Raspberry Pi-like) cameras when cost demands it; adapt to bandwidth/cost tradeoffs.
- **Source:** "Considering Raspberry Pi cameras at each workstation" (Oct 2 summary)

### Product: Dependability/Reliability/Security

#### PD-1: On-premise Processing & Data Residency
- **Requirement:** All processing and data storage must remain on-premises (no cloud) to satisfy IP and government concerns.
- **Source:** "Everything on-prem. No cloud services" (Oct 2 transcript)

### Organizational: Development Requirements

#### OD-1: Open Source Preference
- **Requirement:** Prefer open-source libraries (MIT/Apache) for computer vision components to avoid licensing costs.
- **Source:** "Preference for open source software (MIT/Apache license) to avoid costs" (Oct 2 summary)

#### OD-2: Training Dataset Capture & Storage
- **Requirement:** Provide tooling to capture representative video samples and organize them for model training and retraining.
- **Source:** "Capture video of correct process, mark start/end of each step" (Oct 2 summary)

### Organizational: Operational Requirements

#### OO-1: Cost Controls
- **Requirement:** Minimize hardware costs (cameras, edge devices) and prefer centralized server processing when cost-effective.
- **Source:** "Cost is important; consider Raspberry Pi vs server" (Oct 2 summary)

#### OO-2: Deployment & Integration Plan
- **Requirement:** Provide a phased deployment plan (simulated testing -> pilot on production floor -> full rollout) and integration approach with KMD.
- **Source:** "Team should create simulated workstation for initial testing; schedule time on production floor for final testing" (Oct 2 summary)

### Organizational: Environmental Requirements

#### OE-1: Factory Floor Conditions
- **Requirement:** System must operate under typical factory conditions such as variable lighting, dust, and heat; cameras and mounts must accommodate these conditions.
- **Source:** Implied by factory environment discussion

#### OE-2: Network Constraints
- **Requirement:** Adaptive behavior for limited network bandwidth and potential latency between stations and server.
- **Source:** "Handle limited bandwidth; no cloud" (Oct 2 summary)

### External: Cultural and Social Requirements

#### EC-1: Diverse Workforce Considerations
- **Requirement:** Design UI and alerts so they are understandable by workers with varying language skills and tech literacy.
- **Source:** Inferred from Oct 19 notes about temp agencies and language

### External: Interoperability Requirements

#### EI-1: Provide Clear Data Schema
- **Requirement:** Publish a clear JSON schema for scan results so integration points (KMD or middleware) can reliably consume the data.
- **Source:** Implied by "Output likely JSON string with scanned data"