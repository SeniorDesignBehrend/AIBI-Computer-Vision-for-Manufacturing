## User Functional Requirements

### UFR-1: Part Tracking and Barcode Management

#### UFR-1.1: Fixed-Station Multi-Barcode Detection
- **Requirement:** Fixed camera at each workstation must detect, decode, and process multiple barcodes (5-20 per paper) from objects presented within the camera's field of view
- **Details:** 
  - Support approximately 12 workstations without conveyor systems
  - Handle paper with multiple barcodes that travels with parts
  - Process traditional 1D barcodes and 2D QR codes simultaneously
  - Function when paper is positioned on table within camera view
- **Priority:** Critical
- **Source:** Sept 19: "there might be between 5 and 20 barcodes that they have to scan"; Oct 2: "Fixed camera at each station to scan paper with multiple barcodes"

#### UFR-1.2: Configurable Barcode Field Mapping
- **Requirement:** Provide configurable mapping system to assign barcode positions to specific data fields (part number, serial number, material batch, spool IDs)
- **Details:**
  - Support per-workstation configuration for different requirements
  - Allow positional mapping (top-left, top-down, left-to-right patterns)
  - Handle varying numbers of required barcodes per station
  - Enable field validation and requirement checking
- **Priority:** Critical
- **Source:** Sept 19: "configurable way to teach your system, you know, maybe top left or top down, left to right"; Oct 2: "configurable system to map barcode positions to data fields"

#### UFR-1.3: Object Recognition for Non-Barcodeable Parts
- **Requirement:** Identify and track large parts that cannot accommodate barcodes due to high-temperature processing or physical constraints
- **Details:**
  - Recognize etched identifiers on mandrels and large components
  - Process carved/etched numbers, letters, or symbols (1, 2, 3 or A, B, C)
  - Handle parts that undergo processes where barcodes would be destroyed
  - Provide same data output format as barcode scanning
- **Priority:** High
- **Source:** Sept 19: "any barcodes, stickers, any of that kind of stuff would just get burnt off in the oven"

#### UFR-1.4: Structured Data Output and Integration
- **Requirement:** Aggregate all decoded values into structured JSON payload for downstream system integration
- **Details:**
  - Include timestamps, workstation ID, and field mapping metadata
  - Provide data in format compatible with KMD software consumption
  - Support both real-time API delivery and intermediate database storage
  - Enable keyboard input emulation for legacy KMD barcode scanner interface
- **Priority:** Critical
- **Source:** Sept 19: "produce a JSON string"; Oct 2: "KMD software currently uses barcode scanners as keyboard input"

### UFR-2: Process Monitoring and Quality Assurance

#### UFR-2.1: Manufacturing Step Detection and Sequencing
- **Requirement:** Monitor and validate that manufacturing steps are performed in correct sequence at each workstation
- **Details:**
  - Detect specific process actions (cloth application, resin application, fiber winding)
  - Recognize step start and completion events
  - Validate prerequisite steps before allowing subsequent operations
  - Focus on process sequence rather than final part quality assessment
- **Priority:** High
- **Source:** Sept 19: "You have to put the fabric on first before you apply the resin"; Oct 2: "AI to detect if steps are performed in correct order"

#### UFR-2.2: Real-time Process Feedback and Alerts
- **Requirement:** Provide immediate visual feedback and alerts for process status and violations
- **Details:**
  - Display step-by-step progress indicators (checkboxes, status lights)
  - Show green checkmarks for completed steps
  - Trigger visual and audio alerts for out-of-sequence operations
  - Update status in real-time during work progress
- **Priority:** High
- **Source:** Sept 19: "bunch of checkboxes down the right-hand side of the video feed"; "flashy something, maybe an alarm to go off"

#### UFR-2.3: Simple Training Interface for Process Steps
- **Requirement:** Provide intuitive UI for non-technical users to train the system on correct manufacturing processes
- **Details:**
  - Allow engineers and operators to capture reference videos
  - Enable marking of step start/end points during training capture
  - Support on-production-floor training with minimal technical assistance
  - Store training data for model retraining and validation
- **Priority:** Medium
- **Source:** Oct 2: "simple UI for training system on correct process steps"; "Capture video of correct process, mark start/end of each step"

#### UFR-2.4: Process Sequence Validation and Error Prevention
- **Requirement:** Prevent manufacturing errors by detecting and alerting on skipped or incorrectly sequenced steps
- **Details:**
  - Identify when critical steps are omitted
  - Allow intervention before process continuation
  - Handle variations in worker behavior (left-handed vs right-handed approaches)
  - Account for natural workflow interruptions and tool drops
- **Priority:** High
- **Source:** Sept 19: "some people are going to apply the resin from left to right rather than right to left"

### UFR-3: System Integration and Data Management

#### UFR-3.1: KMD Software Integration
- **Requirement:** Seamless integration with existing KMD Technology Solutions workflow management system
- **Details:**
  - Provide local API or network communication method
  - Support both keyboard input emulation and database integration approaches
  - Ensure data format compatibility with current KMD data structures
  - Enable gradual implementation without disrupting existing operations
- **Priority:** Critical
- **Source:** Sept 19: "feed that into KMD somewhere"; Oct 2: "develop API or local network communication"

#### UFR-3.2: Intermediate Data Storage and Persistence
- **Requirement:** Implement intermediate data storage to decouple computer vision processing from KMD data consumption
- **Details:**
  - Write scan results to local database with timestamps and station identifiers
  - Include part/serial references and mapped field indicators
  - Support data recovery and audit trail requirements
  - Enable offline operation during network issues
- **Priority:** Medium
- **Source:** Oct 2: "Consider database table for intermediate data storage"

### UFR-4: Development and Testing Support

#### UFR-4.1: Simulated Testing Environment
- **Requirement:** Provide simulated workstation environment for development and validation before production deployment
- **Details:**
  - Create test environment that mimics camera views and KMD field interactions
  - Support iterative development without production floor disruption
  - Enable comprehensive testing of multi-workstation scenarios
  - Include representative manufacturing process simulations
- **Priority:** Medium
- **Source:** Oct 2: "No dedicated test environment at CompositeFlex; Team should create simulated workstation for initial testing"

#### UFR-4.2: Training Dataset Management
- **Requirement:** Provide tools for capturing, organizing, and managing training datasets for model development
- **Details:**
  - Support video sample capture from production environments
  - Organize datasets by part type, process, and workstation
  - Enable model retraining with new data sources
  - Support various lighting and environmental conditions
- **Priority:** Medium
- **Source:** Sept 19: "we'll be able to give you as many photos... of that A etched piece of metal as you need"

---

## Non-functional Requirements

### Product: Usability Requirements

#### PU-1: Factory Worker Ease of Use
- **Requirement:** System must be extremely easy to use for manufacturing workers with minimal training
- **Details:**
  - Function reliably with workers wearing gloves, goggles, and hard hats
  - Work consistently on first attempt without repositioning requirements
  - Provide clear, intuitive visual feedback and status indicators
  - Minimize cognitive load during normal manufacturing operations
- **Priority:** Critical
- **Source:** Sept 19: "picture yourself, you're this guy working in the factory, you maybe have gloves on"

#### PU-2: Hands-Free and Minimal Interaction Operation
- **Requirement:** Minimize physical interaction requirements during normal operation
- **Details:**
  - Automatic detection when objects enter camera field of view
  - No requirement to hold papers in specific positions
  - Integrate seamlessly into existing natural workflow movements
  - Reduce additional operator burden during production
- **Priority:** High
- **Source:** Sept 19: "can we get it so that maybe even the piece of paper is just on a table"; Oct 2: "Minimize additional work for operators"

#### PU-3: Non-Technical Training Interface
- **Requirement:** Training and configuration interfaces must be accessible to non-technical staff
- **Details:**
  - Minimal clicks and clear step labeling for process training
  - In-situ capture capability for production floor use
  - Intuitive configuration for barcode mapping and field assignment
  - Clear visual feedback during training and setup procedures
- **Priority:** Medium
- **Source:** Oct 2: "Develop easy-to-use interface for non-technical workers to train system"

#### PU-4: Diverse Workforce Accommodation
- **Requirement:** Design system to accommodate workers with varying language skills and technical literacy
- **Details:**
  - Visual indicators that transcend language barriers
  - Intuitive symbols and color coding for status communication
  - Support for temporary workers with minimal training
  - Account for varying skill levels and tenure
- **Priority:** Medium
- **Source:** Sept 19: "they sometimes don't speak our language"; "these folks that get hired, they come from temp agencies"

### Product: Performance Requirements

#### PP-1: Real-time Processing and Response
- **Requirement:** Process video feeds and provide feedback with minimal latency to prevent manufacturing errors
- **Details:**
  - Real-time barcode detection and decoding
  - Immediate process step validation and feedback
  - Low-latency alerts for out-of-sequence operations
  - Smooth video processing without noticeable delays
- **Priority:** Critical
- **Source:** Sept 19: Implied from real-time feedback requirements; Oct 2: Real-time alerts requirement

#### PP-2: High Accuracy Requirements
- **Requirement:** Maintain high accuracy in both barcode detection and process monitoring for aerospace quality standards
- **Details:**
  - Reliable barcode reading across various lighting conditions
  - Accurate process step detection with minimal false positives/negatives
  - Consistent performance across different part types and processes
  - Meet quality control requirements for aerospace manufacturing
- **Priority:** Critical
- **Source:** Sept 19: "we have to keep track of how long it was at each station, was it in the oven long enough"

#### PP-3: Low-Cost Camera Tolerance
- **Requirement:** Function effectively with lower-quality, cost-effective camera equipment
- **Details:**
  - Work with "pretty low level cheap camera" hardware
  - Adapt to bandwidth limitations and cost constraints
  - Consider Raspberry Pi camera compatibility
  - Balance cost versus performance requirements
- **Priority:** Medium
- **Source:** Sept 19: "if we can use a pretty low level cheap camera"; Oct 2: "Considering Raspberry Pi cameras at each workstation"

### Product: Dependability/Reliability/Security

#### PD-1: Strict On-Premises Data Security
- **Requirement:** All processing and data storage must remain on-premises with no cloud dependencies
- **Details:**
  - Deploy on Ubuntu server with Python-based processing
  - Ensure no data transmission outside facility network
  - Meet government and military contractor compliance requirements
  - Protect proprietary manufacturing information and intellectual property
- **Priority:** Critical
- **Source:** Sept 19: "once your data leaves your facility, you can't really get it back"; Oct 2: "Everything on-prem. No cloud services"

#### PD-2: Manufacturing Environment Reliability
- **Requirement:** Reliable operation in industrial factory conditions with minimal downtime
- **Details:**
  - Function consistently in presence of heat, dust, and noise
  - Handle varying lighting conditions throughout production shifts
  - Operate reliably with physical space limitations for camera placement
  - Maintain performance during network latency and connectivity issues
- **Priority:** High
- **Source:** Sept 19: Implied from factory deployment context; Sept 19: "I've also heard them complain about network speeds"

### Organizational: Development Requirements

#### OD-1: Open Source Technology Preference
- **Requirement:** Utilize open-source libraries and frameworks to minimize licensing costs
- **Details:**
  - Prefer MIT and Apache licensed computer vision libraries
  - Avoid proprietary software dependencies where possible
  - Document all license requirements and compliance considerations
  - Enable cost-effective deployment and maintenance
- **Priority:** Medium
- **Source:** Oct 2: "Preference for open source software (MIT/Apache license) to avoid costs"

### Organizational: Operational Requirements

#### OO-1: Cost Optimization
- **Requirement:** Minimize hardware and deployment costs while meeting performance requirements
- **Details:**
  - Use cost-effective cameras and edge devices where appropriate
  - Consider Raspberry Pi versus centralized server processing trade-offs
  - Optimize bandwidth usage and network infrastructure requirements
  - Balance performance requirements with cost constraints
- **Priority:** High
- **Source:** Sept 19: "cost is very important to all these people. The less we cost, the more money we can save them"; Oct 2: "Cost is important; consider Raspberry Pi vs server"

#### OO-2: Configurable Deployment Architecture
- **Requirement:** Support flexible deployment configurations for different workstation setups
- **Details:**
  - Adapt to varying manufacturing processes and requirements
  - Support different camera positions, angles, and mounting configurations
  - Enable per-workstation customization of detection and validation rules
  - Allow for future expansion and modification of station configurations
- **Priority:** Medium
- **Source:** Sept 19: "creating a configurable system to adapt to different workstation setups"

#### OO-3: Phased Deployment Strategy
- **Requirement:** Support gradual implementation with minimal disruption to existing operations
- **Details:**
  - Enable coexistence with current barcode scanning systems during transition
  - Support pilot deployment on selected workstations before full rollout
  - Provide rollback capabilities during deployment phases
  - Include training and change management considerations
- **Priority:** Medium
- **Source:** Oct 2: "phased deployment plan (simulated testing -> pilot on production floor -> full rollout)"

### External: Interoperability Requirements

#### EI-1: KMD Software Compatibility
- **Requirement:** Maintain compatibility with existing KMD Technology Solutions software interfaces
- **Details:**
  - Support current keyboard input barcode scanner interface
  - Provide structured data output compatible with KMD data consumption
  - Enable API integration without requiring KMD software modifications
  - Maintain backward compatibility during system transitions
- **Priority:** Critical
- **Source:** Sept 19: "we're going to feed that into KMD somewhere"; Oct 2: "KMD software currently uses barcode scanners as keyboard input"

#### EI-2: Clear Data Schema Definition
- **Requirement:** Publish comprehensive JSON schema for scan results and system outputs
- **Details:**
  - Define standard data formats for barcode scanning results
  - Specify metadata fields for timestamps, station identifiers, and validation status
  - Document API endpoints and data exchange protocols
  - Enable reliable integration with middleware and downstream systems
- **Priority:** High
- **Source:** Oct 2: "Publish a clear JSON schema for scan results"

#### EI-3: Legacy System Integration
- **Requirement:** Support integration with existing manufacturing systems and processes
- **Details:**
  - Work alongside current quality control and tracking systems
  - Support existing part numbering and identification schemes
  - Enable data export to other manufacturing execution systems
  - Maintain audit trail compatibility with existing compliance requirements
- **Priority:** Medium
- **Source:** Sept 19: Implied from existing barcode scanner workflow integration
