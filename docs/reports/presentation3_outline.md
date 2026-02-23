# Presentation 3 — AIBI Computer Vision for Manufacturing

**Team 9 | SWENG 481 / CMPSC 485 | February 2026**

> 35 minutes of presentation + live demo. 1 hour total slot.
> Print slides. Follow the rubric.

---

## Slide 1: Title

- **AIBI Computer Vision for Manufacturing**
- Team 9
  - Nathan DiGilio (CS), Jacob Dzikowski (CS), Collin Miller (SWE), Daniel Pora (SWE)
- Course Instructor: Naseem Ibrahim
- Faculty Advisor: Jonathan Liaw
- Industry Sponsor: AIBI Solutions | Industry Mentor: Kevin DiGilio
- Version 3.0 — February 2026

---

## Slide 2: Presentation Outline

1. Problem Statement & Broader Impact
2. Requirements Review (with changes in v3.0)
3. Use Case Diagram & Trace Table
4. Exploratory Studies Update
5. Architectural Design & Design Patterns
6. Structural Design (Class Diagrams)
7. UI Design (Screenshots)
8. Behavioral Design (State & Activity Diagrams)
9. Implementation Progress & Tools
10. Testing & Test Execution Reports
11. Challenges
12. Live Demo
13. Questions

---

## Slide 3: Problem Statement & Broader Impact

**Business Background:**
- AIBI Solutions is the AI-focused sister company of KMD Technology Solutions
- KMD builds project management and workflow optimization tools for manufacturers
- AIBI extends that mission with secure, on-premises AI — no cloud dependencies

**The Problem:**
- Manufacturers under government contracts need full traceability, efficiency, and data security
- Many still rely on manual tracking or outdated barcode systems — slow, error-prone
- Stricter data protection rules make cloud-based AI tools impractical

**Our Solution — Two Subsystems:**
1. **Part & Material Tracking** — QR code scanning at workstations, auto-mapping to data fields, structured JSON output
2. **Worker-Step Verification** — DINOv2 deep learning model monitors that operators perform manufacturing steps in the correct order

**Broader Impact:**
- Demonstrates how AI/CV can bring smart automation to secure, high-stakes manufacturing
- All processing runs locally — full regulatory compliance, no data leaves the facility

---

## Slide 4: Requirements Review — Changes in v3.0

**What changed since Report 2.0/2.5:**
- Updated use cases: Deleted UC-004, clarified training process
- Added UFR13–23 (new user functional requirements for step verification UI)
- Added SFR19–32 (new system functional requirements)
- Split SFR7 into SFR7, SFR26, SFR27 (UI overlay details)
- Split Section 6 into two subsections: 6.1 (Part Tracking) and 6.2 (Step Verification)
- Overhauled test cases — removed redundant, added step verification cases
- Updated all requirement cards and trace table

**Key User Functional Requirements:**
| ID | Requirement |
|----|------------|
| UFR1 | Detect, decode, and process multiple QR codes in camera's field of view |
| UFR5 | Monitor and validate manufacturing steps in correct sequence |
| UFR6 | Provide immediate visual feedback and alerts for process status/violations |
| UFR8 | Provide intuitive UI for non-technical users to train system on processes |
| UFR13 | Show all errors in the process on screen |
| UFR14 | Show all steps for the process on screen |
| UFR15 | Have a visual marker for completed or missed steps |

---

## Slide 5: Use Case Diagram & Trace Table

**Use Cases** (show the Use Case Diagram from Figure 4.1 in report):
- UC-001: Scan Part QR Codes (Factory Operator)
- UC-002: Monitor Manufacturing Steps (Factory Operator) — includes UC-003
- UC-003: Train System on Manufacturing Process (Production Supervisor)
- UC-005: Simulate Workstation Environment (Developer)

**Requirements Trace Table** (show summary from Appendix R):

| User Req | System Req | Use Case | Test Cases |
|----------|-----------|----------|------------|
| UFR1 | SFR1, SFR15, SFR16 | UC-001 | TC-001–003 |
| UFR5 | SFR6, SFR19–22, SFR26 | UC-002 | TC-004–006 |
| UFR8 | SFR8, SFR14 | UC-003 | TC-007–009 |
| UFR11 | SFR13, SFR17, SFR18 | UC-005 | TC-010–012 |

> Reference Appendix R in the report for the full trace table.

---

## Slide 6: Exploratory Studies Update

**Part & Material Tracking:**
- QR decoding: pyzbar and ZXing evaluated — pyzbar chosen as primary (multi-barcode), OpenCV as fallback
- Traditional vision methods proved most effective for symbolic barcode tracking

**Worker-Step Verification:**
- Explored OpenCLIP and MobileCLIP for multimodal embeddings
- MobileCLIP couldn't be used (limited research license)
- Settled on DINOv2 (Meta's self-supervised Vision Transformer) via PyTorch Hub
  - 384-dimensional embeddings, no labeled training data needed
  - Cosine similarity on L2-normalized embeddings for step matching
- Edge optimization and model quantization studied for local GPU performance

**Key Packages:**
- OpenCV — video capture, preprocessing, visualization
- PyTorch / DINOv2 — embedding generation and similarity matching
- Streamlit — rapid prototyping of operator UI
- pyzbar — primary QR/barcode decoding
- uv — reproducible Python package management

---

## Slide 7: Architectural Design — Part & Material Tracking (Section 6.1)

> Show the architectural diagram from Section 6.1.1 of the report.

**Data Flow:**
```
Camera Feed → Decode QR (pyzbar → OpenCV fallback) → Parse Fields →
Validate Against Config → Output (Excel auto-entry / JSON file)
```

**Components:**
- Camera module captures frames
- DecodeQr attempts detection with 3-tier fallback (pyzbar → OpenCV multi → OpenCV single)
- Parse extracts field name + value from colon or JSON format
- ConfigManager loads workstation-specific field requirements
- OutputData writes to JSON and/or auto-types into Excel

---

## Slide 8: Architectural Design — Worker-Step Verification (Section 6.2)

> Show the architectural diagram from Section 6.2.1 of the report.

**Two Phases:**

**Training Phase:**
```
Supervisor defines steps → Records video of each step →
DINOv2 extracts embeddings per frame → Average + L2-normalize →
Save centroid per step as .pkl file
```

**Monitoring Phase:**
```
Live camera frame → DINOv2 embedding → Cosine similarity vs. all step centroids →
Sliding window voting → State machine determines status → UI overlay feedback
```

---

## Slide 9: Design Patterns

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Strategy** | Barcode detection fallback chain (pyzbar → OpenCV multi → OpenCV single) | Swappable detection algorithms at runtime |
| **State Machine** | VerificationState enum (IDLE → CORRECT_STEP → CONFIRMED → COMPLETE) | Clean transitions for step verification logic |
| **Observer** | Streamlit session_state reactively updates UI on state changes | Decouples verification logic from UI rendering |
| **Facade** | ProcessManager wraps step management, training, and serialization | Simple interface over complex subsystem |
| **Template Method** | Common camera → preprocess → analyze pipeline, specialized per subsystem | Shared structure, different processing |

---

## Slide 10: Structural Design — Class Diagrams

> Show class diagrams from Sections 6.1.2 and 6.2.2 of the report.

**Part Tracking System:**
- `AdvancedScanner` — orchestrates scanning workflow
- `Camera` — captures frames, coordinates decode/parse/output
- `DecodeQr` — QR/barcode detection logic
- `Parse` — field extraction from barcode data
- `OutputData` — JSON/Excel output generation
- `ConfigManager` / `WorkstationConfig` — per-workstation configuration

**Step Verification System** (refactored into separate modules):
- `ProcessManager` — manages steps, training lifecycle, session state
- `ActionStep` (dataclass) — name, order, centroids, final centroid
- `VerificationState` (enum) — IDLE, CORRECT_STEP, CONFIRMED, WRONG_ORDER, SKIPPED, COMPLETE
- `embeddings.py` — DINOv2 model loading and embedding extraction
- `verification.py` — similarity calculation and state determination
- `serialization.py` — pickle-based save/load of trained processes
- `ui_training.py` / `ui_operation.py` — separated UI rendering

**v3.0 Change:** Split monolithic `app.py` into focused modules for readability and reusability.

---

## Slide 11: UI Design — Screenshots

> Take actual screenshots of both systems running and paste them here.

**Step Validation — Training Mode (Streamlit):**
- Sidebar: add step names, select step, start/stop recording, finalize, save/load .pkl
- Main area: live camera feed showing frame capture count

**Step Validation — Monitoring Mode (Streamlit):**
- Progress bar showing step completion
- Step checklist: green checkmark (done), arrow (current), empty box (pending)
- Live video with color-coded state overlay (green = correct, red = wrong order, blue = idle)
- Confidence percentage display
- Tuning sliders: similarity threshold, window size, required votes

**QR Scanner (OpenCV window):**
- Live camera feed with barcode bounding boxes drawn
- Field status overlay: green check / red X for each configured field
- "READY TO SAVE" banner when all required fields scanned

---

## Slide 12: Behavioral Design — State Diagram

> Show the state diagram from Section 6.2.4 of the report.

**Step Verification State Machine:**

```
                    similarity < threshold
        ┌─────────────────────────────────────┐
        v                                     │
     [IDLE] ──── similarity >= threshold ──→ [CORRECT_STEP]
                                              │         │
                              votes >= required│         │ detected < current
                                              v         v
                                        [CONFIRMED]  [WRONG_ORDER]
                                           │              (anomaly logged)
                               advance to  │
                               next step   │   detected > current
                                           │        │
                                           v        v
                              (last step?) ──→ [COMPLETE]
                                                [SKIPPED]
                                              (anomaly logged)
```

**States explained:**
- **IDLE** — No confident match (below threshold)
- **CORRECT_STEP** — Expected step detected, accumulating votes
- **CONFIRMED** — Consensus reached (e.g., 7/10 frames), advance
- **WRONG_ORDER** — Past step re-detected (anomaly warning)
- **SKIPPED** — Future step detected before current confirmed
- **COMPLETE** — All steps verified successfully

---

## Slide 13: Behavioral Design — Activity Diagram

> Show the activity diagram from Section 6.1.4 / 6.2.4 of the report.

**QR Scanning Activity Flow:**
```
Start → Open Camera → Capture Frame → Attempt Decode (pyzbar) →
  ├─ Success → Parse Field → Check Duplicate → Update Tracker
  └─ Fail → Try OpenCV Multi → Try OpenCV Single
       → All Required Fields? ─ Yes → Auto-Enter to Excel → Save JSON → Reset
                               └─ No → Continue Capturing
```

---

## Slide 14: Implementation Progress

**Tools & Technologies:**
- Python 3.10+, PyTorch, DINOv2 (dinov2_vits14), OpenCV, Streamlit
- pyzbar, Pillow, NumPy, PyGetWindow, keyboard
- uv package manager, pytest, pytest-cov
- Git + GitHub for version control

**Implemented (~60-65%):**

| Feature | Status | SFRs Met |
|---------|--------|----------|
| Multi-QR detection with fallback | Done | SFR1, SFR15, SFR16 |
| Field-based barcode parsing (colon + JSON) | Done | SFR2, SFR4 |
| Workstation config system (JSON) | Done | SFR32 |
| Excel keyboard-emulation auto-entry | Done | SFR5 |
| DINOv2 step training (record, centroids, save/load) | Done | SFR8, SFR14 |
| Real-time step verification with sliding-window voting | Done | SFR6, SFR9 |
| Anomaly detection (wrong order, skipped) | Done | SFR10 |
| Step progress UI with visual markers | Done | SFR19–22, SFR26 |
| Simulation scanner | Done | SFR13, SFR17, SFR18 |
| Refactored step_validation into modular classes | Done | — |

**Still to implement:**
- Local API connector for KMD workflow integration (EISR1)
- Audio alerts for violations (SFR27)
- Admin functionality for in-site capture tool (SFR24)
- Click step to view recorded footage (SFR23)
- Command line control (SFR25)
- Reset button for next part (SFR28)
- QR count/direction/character configuration (SFR29–31)
- Deployment packaging and user manual

---

## Slide 15: Testing

**Test Automation Framework:**
- pytest + pytest-cov
- Run: `uv run python run_sfr_tests.py` or `uv run python run_sfr_tests.py --coverage`

**Test Suites:**

| Suite | Type | Focus |
|-------|------|-------|
| test_comprehensive.py | SFR Compliance | Full system functional requirement validation |
| test_unit_requirements.py | Unit | Individual function correctness |
| test_config_manager.py | Unit | Workstation configuration CRUD |
| test_barcode_parsing.py | Unit | Field parsing logic |
| test_qr_detection.py | Unit | QR/barcode detection |
| test_integration.py | Integration | End-to-end scan workflows |
| test_simulation_scanner.py | Integration | Simulated workstation environment |

**Test Execution Reports:**
- Show screenshot of recent test run with pass/fail counts
- Reference Appendix T (test case designs) and Appendix TE (execution reports)

> Run tests live or show a recent screenshot: `uv run python run_sfr_tests.py`

---

## Slide 16: Challenges

| Challenge | How We Solved It |
|-----------|-----------------|
| DINOv2 model loading latency (~5s) | Pre-load model at app startup with Streamlit caching |
| Pickle serialization errors when saving trained processes | Fixed data structure serialization; added delete button for corrupted saves |
| Barcode detection unreliability with poor lighting/angles | 3-tier fallback strategy: pyzbar → OpenCV multi → OpenCV single |
| Real-time jitter in step detection (flickering states) | Sliding-window voting — requires 7/10 frame consensus to confirm |
| Excel automation fragility (window not found) | JSON fallback output when Excel unavailable |
| Monolithic app.py difficult to maintain and test | Refactored into separate modules (models, state, embeddings, verification, UI) |
| Report noted OpenCLIP/MobileCLIP explored but MobileCLIP license restricted | Pivoted to DINOv2 — similar capability, fully open-source |

---

## Slide 17: Live Demo

> Transition slide — switch to live demo.

**What we will show:**
1. QR/Barcode Scanner — scanning pre-printed codes, field tracking, JSON output
2. Step Validation — training on a simple process, then real-time monitoring with anomaly detection

---

## Slide 18: Questions

---

---

# Demo Plan

## Setup Checklist (do before the presentation)

- [ ] Print QR codes with your field format (e.g., `part_number:PN-12345`, `serial_number:SN-67890`)
- [ ] Pre-train a backup .pkl file with 3-4 simple steps — in case live training takes too long
- [ ] Verify camera works on the presentation laptop
- [ ] Run `uv run python run_sfr_tests.py` and screenshot the results for the testing slide
- [ ] Have good lighting in the room for the step validation camera
- [ ] Print your slides

## Demo 1: QR/Barcode Scanner (~5 min)

1. **Show the config file** — briefly open `configs/workstation_01.json` to show the field setup
2. **Run the scanner** — `uv run python -m aibi_cv.advanced_scanner`
3. **Hold QR codes in front of camera** one at a time
   - Show the field status overlay updating (green checks appear)
   - Point out the bounding boxes drawn around detected codes
4. **Scan all required fields** — show the "READY TO SAVE" state
5. **Show JSON output** — open the generated file in `outputs/`
6. *(Optional)* If Excel is open, show the auto-typing feature

## Demo 2: Step Validation (~8 min)

1. **Launch** — `uv run streamlit run src/step_validation/app.py`
2. **Training Phase:**
   - Add 3-4 simple steps: "Pick up pen", "Open notebook", "Write on page", "Close notebook"
   - Record each step for 3-5 seconds — show frame count incrementing
   - Click "Finalize Training" — explain centroids are being computed
   - *(Or load the pre-trained .pkl backup to save time)*
3. **Monitoring Phase:**
   - Start monitoring — point out the sidebar tuning parameters
   - **Perform steps in order** — show:
     - IDLE → CORRECT_STEP → CONFIRMED advancing through checklist
     - Progress bar filling up
     - Green checkmarks appearing
   - **Deliberately do a step out of order** — show WRONG_ORDER anomaly
   - Complete the full sequence — show COMPLETE state
4. **Show tuning** — adjust similarity threshold in sidebar, explain how it affects sensitivity

## Demo Tips

- Use **simple, visually distinct objects** (pen, book, cup, phone) — don't pick things that look similar
- **Practice the step sequence** 2-3 times beforehand so it's smooth
- If training is slow, **load the .pkl backup** — nobody will judge you for having a save file ready
- Keep a **terminal open** showing the Streamlit logs in case someone asks technical questions
- **Have the report PDF open** on another screen to reference diagrams if asked
