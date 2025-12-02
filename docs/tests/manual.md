| Test Case ID | What to Test | Test Data Input | Expected Result | Relevant Requirements | Relevant Use Case(s) |
|--------------|--------------|-----------------|------------------|------------------------|------------------------|
| TC-SFR1-MAN-01 | Live camera detects all visible QR codes. | Printed QR codes placed in camera FOV. | All visible codes appear in UI/output. | SFR1, SFR15, SFR16 | UC-001 |
| TC-SFR2-MAN-01 | Operator configures field mapping correctly. | Mapping config UI + known printed QRs. | Output places values into correct fields. | SFR2 | UC-001 |
| TC-SFR4-MAN-01 | Real scan produces correct JSON record. | Live scan event with known QRs. | One JSON record created with all data + metadata. | SFR4, SFR11 | UC-001 |
| TC-SFR5-MAN-01 | Keyboard-emulation outputs correct text to target app. | Live scan + Notepad field in focus. | Exactly correct keystroke output appears. | SFR5, SFR18 | UC-001 |
| TC-SFR11-MAN-01 | Persistence & replay after downstream outage. | Perform scans while downstream offline, then reconnect. | All offline events replay once with no loss or duplicates. | SFR11 | UC-002, UC-004 |
| TC-SFR12-MAN-01 | Documentation matches schema & outputs. | JSON schema doc + sample outputs. | Documentation consistent with schema/output. | SFR12 | UC-001 |
| TC-SFR15-MAN-01 | Live multi-code decoding in typical lighting. | Printed QR sheet with known values. | All codes decode correctly. | SFR15 | UC-001 |
| TC-SFR16-MAN-01 | Output includes all visible QRs. | Live multi-code scan. | Output matches count & content of visible QRs. | SFR16 | UC-001 |
| TC-SFR17-MAN-01 | Developer runs simulation scenario via UI. | Simulation UI + recorded footage. | Results mimic live scan behavior; logs produced. | SFR17 | UC-005 |
| TC-SFR18-MAN-01 | Simulation produces correct keyboard-emulation output. | Simulation scenario + sandbox text field. | Typed text matches expected sequence. | SFR18 | UC-005 |
| TC-PUSR1-MAN-01 | New operator completes basic workflow in <30 min. | New user + system UI + stopwatch. | Operator completes tasks without help in ≤30 min. | PUSR1 | UC-001 |
| TC-PUSR2-MAN-01 | UI tooltips/guidance allow correct interpretation. | UI + test user. | User identifies major controls based on guidance. | PUSR2 | UC-001 |
| TC-PUSR3-MAN-01 | Workflow requires fewer steps than legacy. | Legacy workflow vs. new workflow comparison. | New system uses fewer steps or requires less manual input. | PUSR3 | UC-001 |
| TC-PUSR4-MAN-01 | Touch-free operation of normal workflow. | Operator performing job with system. | Operator rarely or never touches UI during typical cycle. | PUSR4 | UC-002 |
| TC-PUSR5-MAN-01 | Automation reduces repetitive manual input. | Several consecutive jobs. | Common fields auto-filled correctly. | PUSR5 | UC-001, UC-002 |
| TC-PUSR10-MAN-01 | Users interpret icons/colors without text. | Screenshots presented to users. | Users correctly identify states (OK/warn/error). | PUSR10 | UC-001 |
| TC-PPSR2-MAN-01 | Real-time feedback is “immediate”. | Live tasks monitored by operator. | Operator does not perceive delay. | PPSR2 | UC-001 |
| TC-PPSR5-MAN-01 | System works reliably with real 720p camera. | Real 720p hardware test. | No noticeable accuracy degradation. | PPSR5 | UC-001 |
| TC-PDSR1-MAN-01 | No outbound network traffic during operation. | Network monitor during typical shift. | No data sent externally. | PDSR1 | UC-001, UC-002 |
| TC-PDSR2-MAN-01 | System operates with no internet. | Disconnect internet; run system. | Full operation continues normally. | PDSR2 | UC-001 |
| TC-PDSR4-MAN-01 | Stable operation under factory conditions. | Pilot deployment in factory. | No crashes; acceptable performance. | PDSR4 | UC-002 |
| TC-QDSR2-MAN-01 | All OSS components documented. | Documentation review. | Each installed library listed with name/version/license. | QDSR2 | UC-005 |
| TC-QDSR4-MAN-01 | Legacy data imports correctly in real scenario. | Actual legacy system export file. | Records appear correctly with no manual cleanup. | QDSR4 | UC-004 |
| TC-ETSR4-MAN-01 | JSON schema version-controlled + documented. | Repo review + documentation. | Schema file tracked; docs match version. | ETSR4 | UC-005 |
| TC-ETSR5-MAN-01 | Export to actual MES/ERP test instance. | Test instance connected; live export. | Data received and fields mapped correctly. | ETSR5 | UC-002 |
| TC-ETSR6-MAN-01 | Field engineer configures workflow via config. | Field engineer + config files + test job. | System enforces new workflow correctly without code changes. | ETSR6 | UC-005 |
