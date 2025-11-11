# Requirements Analysis - AIBI Computer Vision for Manufacturing
**Meeting Date:** September 19th, 2025  
**Source:** Meeting transcript and discussion

---

## User Functional Requirements

### UFR-1: Part Tracking System

#### UFR-1.1: Barcode/QR Code Detection
- **Requirement:** Detect and decode multiple barcodes/QR codes from a single image or video frame
- **Details:** System must handle various scenarios including:
  - Paper with multiple codes (5-20 barcodes per workstation)
  - Individual part barcodes
  - Mix of traditional barcodes and 2D QR codes
- **Source:** "there might be between 5 and 20 barcodes that they have to scan, depending on what material it is"

#### UFR-1.2: Multi-Code Processing
- **Requirement:** Process all barcodes on a single piece of paper simultaneously
- **Details:** Replace manual barcode scanner workflow where workers scan codes individually
- **Source:** "we believe that if we have a piece of paper that has all the barcodes on it, let's just say there's 20 on there, we believe that we don't need barcode scanners anymore"

#### UFR-1.3: Object Recognition for Non-Barcodeable Items
- **Requirement:** Identify and track parts that cannot have barcodes attached
- **Details:** 
  - Recognize etched identifiers on large parts (mandrels)
  - Handle parts that go through high-temperature processes where barcodes would be destroyed
  - Support carved/etched numbers, letters, or symbols (1, 2, 3 or A, B, C)
- **Source:** "any barcodes, stickers, any of that kind of stuff would just get burnt off in the oven"

#### UFR-1.4: Data Output Format
- **Requirement:** Provide structured data output in JSON format
- **Details:** System must output scanned barcode data in a format compatible with existing KMD software
- **Source:** "it's your job, your guys' job to produce a JSON string"

#### UFR-1.5: Configurable Barcode Ordering
- **Requirement:** Support configurable barcode reading order and assignment
- **Details:** 
  - Allow configuration of which barcode represents which data type
  - Support positional mapping (top-left = part number, etc.)
  - Handle different workstation configurations
- **Source:** "we would need probably some configurable way to teach your system, you know, maybe top left or top down, left to right"

### UFR-2: Human Activity Monitoring

#### UFR-2.1: Process Step Detection
- **Requirement:** Monitor and detect completion of manufacturing process steps
- **Details:**
  - Track multi-step processes at each workstation
  - Detect specific actions (e.g., applying cloth before resin)
  - Recognize when steps are completed correctly
- **Source:** "the camera was able to detect what step he was doing"

#### UFR-2.2: Process Sequence Validation
- **Requirement:** Verify that manufacturing steps are performed in correct order
- **Details:**
  - Ensure prerequisite steps are completed before allowing next steps
  - Example: cloth application must occur before resin application
- **Source:** "You have to put the fabric on first before you apply the resin"

#### UFR-2.3: Real-time Process Feedback
- **Requirement:** Provide immediate visual feedback on process status
- **Details:**
  - Display checkboxes or indicators for each required step
  - Show green checkmarks when steps are completed correctly
  - Update status in real-time as work progresses
- **Source:** "there's maybe a bunch of checkboxes down the right-hand side of the video feed that show the steps that are supposed to happen"

#### UFR-2.4: Error Detection and Alerting
- **Requirement:** Detect and alert when processes are performed out of sequence
- **Details:**
  - Identify when steps are skipped or performed in wrong order
  - Trigger visual and/or audio alerts
  - Allow intervention before process continues
- **Source:** "if something goes out of, you know, goes out of order, then we would want some sort of flashy something, maybe an alarm to go off"

---

## Non-functional Requirements

### Product: Usability Requirements

#### PU-1: Ease of Use
- **Requirement:** Extremely easy to use for factory workers
- **Details:**
  - Work with workers wearing gloves, goggles, hard hats
  - Function on first try without repositioning
  - Minimal training required
- **Source:** "picture yourself, you're this guy working in the factory, you maybe have gloves on, you have equipment on... and you want it to work on the first try"

#### PU-2: Hands-Free Operation
- **Requirement:** Minimize physical interaction requirements
- **Details:** 
  - Automatic detection when paper enters camera view
  - No need to hold paper in specific position
- **Source:** "can we get it so that maybe even the piece of paper is just on a table, and that table is in the view of the camera"

#### PU-3: Fault Tolerance for Human Variations
- **Requirement:** Handle variations in human behavior and environmental conditions
- **Details:**
  - Account for left-handed vs right-handed workers
  - Handle dropped tools, interruptions
  - Work with different camera angles
- **Source:** "some people are going to apply the resin from left to right rather than right to left, left-handed versus right-handed"

### Product: Performance Requirements

#### PP-1: Real-time Processing
- **Requirement:** Process video feeds and provide feedback in real-time
- **Details:** System must respond quickly enough to prevent manufacturing errors
- **Source:** Implied from real-time feedback requirements

#### PP-2: High Accuracy
- **Requirement:** High accuracy in barcode detection and process monitoring
- **Details:** Must be reliable enough for quality control in aerospace manufacturing
- **Source:** "we have to keep track of how long it was at each station, was it in the oven long enough, did it get sanded properly"

#### PP-3: Video Quality Tolerance
- **Requirement:** Function with lower-quality video feeds
- **Details:** 
  - Reduce bandwidth and cost requirements
  - Work with "pretty low level cheap camera"
- **Source:** "it'd be cool if it didn't need to be top of the line video... if we can use a pretty low level cheap camera"

#### PP-4: Multi-Workstation Processing
- **Requirement:** Process video feeds from multiple cameras simultaneously
- **Details:** Handle feeds from 15+ workstations with proper identification
- **Source:** "let's say there's 15 different workstations in the factory that this thing's going to go to"

### Product: Dependability/Reliability/Security

#### PD-1: Data Security
- **Requirement:** Maintain strict data security for proprietary manufacturing information
- **Details:** Handle government and military contractor compliance requirements
- **Source:** "if you're really trying to protect your IP, you know, your secret sauce or your inventions"

#### PD-2: On-Premise Data Processing
- **Requirement:** All processing must occur on-premises with no cloud dependency
- **Details:**
  - Deploy on Ubuntu server with Python
  - No data leaves the facility
- **Source:** "we need an on-prem AI solution... once your data leaves your facility, you can't really get it back"

#### PD-3: System Reliability
- **Requirement:** Reliable operation in manufacturing environment
- **Details:** Must function consistently in factory conditions with minimal downtime
- **Source:** Implied from manufacturing quality control requirements

### Organizational: Development Requirements

#### OD-1: Documentation Standards
- **Requirement:** Comprehensive documentation for deployment and maintenance
- **Details:** 
  - 200-300 page documentation expected
  - Easy deployment in factory environments
- **Source:** "Emphasis on thorough documentation (200-300 pages expected)"

#### OD-2: Technology Stack Constraints
- **Requirement:** Use specified technology stack for development
- **Details:**
  - Python programming language
  - Ubuntu server deployment
  - Computer vision libraries and models
- **Source:** "It's probably going to be some kind of Python running on Ubuntu"

#### OD-3: Training Data Requirements
- **Requirement:** Support training with customer-provided data sources
- **Details:** 
  - Work with customer-provided video samples
  - Adapt to different part types and processes
- **Source:** "we'll be able to give you as many photos... of that A etched piece of metal as you need"

### Organizational: Operational Requirements

#### OO-1: Cost Effectiveness
- **Requirement:** Minimize hardware and deployment costs
- **Details:**
  - Use inexpensive cameras where possible
  - Consider Raspberry Pi vs centralized processing trade-offs
- **Source:** "cost is very important to all these people. The less we cost, the more money we can save them"

#### OO-2: Configurability
- **Requirement:** System must be easily configurable for different workstation setups
- **Details:** 
  - Adapt to varying manufacturing processes
  - Support different camera positions and angles
- **Source:** "creating a configurable system to adapt to different workstation setups"

### Organizational: Environmental Requirements

#### OE-1: Factory Floor Conditions
- **Requirement:** Operate reliably in industrial manufacturing environment
- **Details:**
  - Function in presence of heat, dust, noise
  - Work with varying lighting conditions
  - Handle physical space limitations for camera placement
- **Source:** Implied from factory deployment context

#### OE-2: Network Environment
- **Requirement:** Function within existing network infrastructure
- **Details:**
  - Work with limited bandwidth
  - Handle network latency and reliability issues
- **Source:** "I've also heard them complain about network speeds"

### External: Legislative Requirements on Safety/Security

### External: Cultural and Social Requirements

#### EC-1: Multi-Language Workforce Support
- **Requirement:** Support workers who may not speak English as primary language
- **Details:** System must be intuitive enough for diverse workforce
- **Source:** "they sometimes don't speak our language"

#### EC-2: Temporary Worker Accommodation
- **Requirement:** Design for workers with varying skill levels and tenure
- **Details:** 
  - Account for workers from temp agencies
  - Minimize training requirements for new employees
- **Source:** "these folks that get hired, they come from temp agencies"

### External: Interoperability Requirements

#### EI-1: KMD Software Integration
- **Requirement:** Interface with existing KMD Technology Solutions software
- **Details:** Provide data in format compatible with current workflow management system
- **Source:** "we're going to feed that into KMD somewhere to actually capture the data"

#### EI-2: Legacy System Compatibility
- **Requirement:** Work alongside existing barcode scanning systems during transition
- **Details:** Allow gradual implementation without disrupting current operations
- **Source:** Implied from existing barcode scanner workflow

---
