| Test Case ID | What to Test | Test Data Input | Expected Result | Relevant Requirements | Relevant Use Case(s) |
|--------------|--------------|-----------------|------------------|------------------------|------------------------|
| TC-SFR1-AUTO-01 | QR detection returns all codes in a static image. | Multi-QR test image with N known codes. | detect_qr_codes() returns N codes; payloads match ground truth. | SFR1, SFR15, SFR16; UFR1 | UC-001 |
| TC-SFR2-AUTO-01 | Field mapping assigns decoded values to logical fields. | Decoded QR list + workstation mapping config. | Mapped JSON contains correct field-value assignments. | SFR2, SFR4 | UC-001 |
| TC-SFR4-AUTO-01 | JSON builder aggregates decoded values + metadata. | Scan data object with decoded codes + metadata. | One valid JSON object produced and schema-compliant. | SFR4, SFR11, SFR12 | UC-001 |
| TC-SFR5-AUTO-01 | Keyboard emulation builder outputs correct keystrokes. | Sample scan payload; delimiter config. | Correct keystroke sequence returned. | SFR5 | UC-001, UC-005 |
| TC-SFR11-AUTO-01 | Persistence stores and reloads events with metadata. | Sample event object. | save_event() then load_event() returns identical data + audit metadata. | SFR11 | UC-002, UC-004 |
| TC-SFR12-AUTO-01 | JSON output matches published schema. | JSON outputs from multiple workflows. | All outputs validate against schema. | SFR12, ETSR3 | UC-001 |
| TC-SFR15-AUTO-01 | Decoder decodes all QRs in multi-code test image. | Multi-code image with ground truth payloads. | All codes decoded; error rate ≤ spec. | SFR15 | UC-001 |
| TC-SFR16-AUTO-01 | Output builder includes one entry per detected QR. | N detections from detection module. | Output contains N entries, no duplicates. | SFR16 | UC-001 |
| TC-SFR17-AUTO-01 | Simulation injects synthetic QR codes into frames. | Recorded video + synthetic injection config. | Detection pipeline sees synthetic codes at correct frames. | SFR17 | UC-005 |
| TC-SFR18-AUTO-01 | Simulation events pass through keyboard-emulation pipeline. | Simulated scan events + mock buffer. | Output keystroke sequence matches expected simulation values. | SFR18 | UC-005 |
| TC-PPSR2-AUTO-01 | Real-time latency under system load. | Synthetic CPU/GPU load; scan input. | Latency stays below threshold (e.g., <200 ms). | PPSR2 | UC-001 |
| TC-PPSR5-AUTO-01 | QR detection accuracy at 720p resolution. | 720p dataset with ground truth. | Detection accuracy meets required threshold. | PPSR5 | UC-001 |
| TC-PDSR1-AUTO-01 | System stores data locally (no external endpoints). | Config inspection script. | All endpoints local; no external URLs. | PDSR1 | UC-002 |
| TC-PDSR2-AUTO-01 | No cloud dependencies in codebase. | Static code analysis. | No cloud APIs referenced. | PDSR2 | UC-001, UC-002 |
| TC-PDSR4-AUTO-01 | Long-duration stability test. | 8–24 hour continuous scan simulation. | No crashes; stable memory/CPU profile. | PDSR4 | UC-002 |
| TC-QDSR1-AUTO-01 | Only approved OSS/commercial libraries used. | Dependency audit script. | All libraries approved; no unauthorized deps. | QDSR1 | UC-005 |
| TC-QDSR4-AUTO-01 | Legacy data imports successfully. | Legacy JSON/CSV files. | Data loads without parsing errors. | QDSR4 | UC-004 |
| TC-ETSR3-AUTO-01 | Interoperability schema validation. | JSON outputs from all workflows. | All validate against ETSR schema. | ETSR3 | UC-001, UC-002 |
| TC-ETSR5-AUTO-01 | Automated export to MES/ERP. | Mock MES/ERP endpoint + sample payload. | Payload accepted; fields correct. | ETSR5 | UC-002 |
| TC-ETSR6-AUTO-01 | Config-driven workflow control. | Two distinct config files; same scan sequence. | Workflow behavior changes correctly based on config. | ETSR6 | UC-005 |
