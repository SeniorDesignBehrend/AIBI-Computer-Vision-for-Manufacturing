4.1.4.1 Product: Usability Requirements
PUUR1 – Ease of Use

User Requirement:
System must be extremely easy to use for manufacturing workers with minimal training; needs to be easier than what is currently being done.

System Requirements:

SR1.1: The user interface shall be intuitive and require no more than 30 minutes of training for first-time users.

SR1.2: The system shall provide clear on-screen guidance and tooltips for all major functions.

SR1.3: The user interface shall minimize the number of actions required to complete common tasks compared to the existing process.

PUUR2 – Minimized Physical Interaction

User Requirement:
Minimize physical interaction requirements during normal operation.

System Requirements:

SR2.1: The system shall support touch-free operation through automatic detection and feedback mechanisms where possible.

SR2.2: The system shall automate common workflow steps to reduce manual input from operators.

SR2.3: The interface shall allow key actions to be performed using minimal clicks or gestures.

PUUR3 – Accessibility of Training and Configuration

User Requirement:
Training and configuration interfaces must be accessible to non-technical staff.

System Requirements:

SR3.1: The configuration interface shall use plain-language prompts and visual menus, avoiding technical jargon.

SR3.2: The system shall include guided setup and tutorial modes for initial configuration.

SR3.3: The system shall allow non-administrative users to modify basic settings without needing programming knowledge.

PUUR4 – Accessibility and Inclusivity

User Requirement:
Design system to accommodate workers with varying technical skills and possible disabilities.

System Requirements:

SR4.1: The system shall comply with accessibility standards (e.g., WCAG 2.1 AA).

SR4.2: The interface shall include support for large text and high-contrast display options.

SR4.3: The system shall support both mouse and keyboard input for inclusivity.

4.1.4.2 Product: Performance Requirements
PPUR1 – Real-Time Feedback

User Requirement:
Process video feeds and provide feedback with minimal latency to prevent manufacturing errors.

System Requirements:

SR5.1: The system shall process video input and deliver analysis feedback within 200 milliseconds.

SR5.2: The system shall prioritize real-time operations over background tasks to minimize latency.

PPUR2 – High Accuracy

User Requirement:
Maintain high accuracy in both barcode detection and process monitoring for aerospace quality standards.

System Requirements:

SR6.1: The system shall achieve a barcode detection accuracy of at least 99%.

SR6.2: The system shall detect and report process deviations with an error margin of less than 1%.

SR6.3: The system shall log all detections and results for audit and quality verification purposes.

PPUR3 – Performance with Low-Cost Equipment

User Requirement:
Function effectively with lower-quality, cost-effective camera equipment.

System Requirements:

SR7.1: The system shall maintain required accuracy levels using cameras with resolutions as low as 720p.

SR7.2: The system shall automatically adjust detection parameters for varying camera quality and lighting conditions.

4.1.4.3 Product: Dependability / Reliability / Security
PDUR1 – On-Premises Processing and Storage

User Requirement:
All processing and data storage must remain on-premises with no cloud dependencies.

System Requirements:

SR8.1: The system shall store all data on local servers within the facility.

SR8.2: The system shall perform all processing operations using on-premises hardware without cloud reliance.

SR8.3: The system shall operate without requiring internet connectivity for normal operation.

PDUR2 – Industrial Reliability

User Requirement:
Reliable operation in industrial factory conditions with minimal downtime.

System Requirements:

SR9.1: The system shall maintain a minimum uptime of 99% during operational hours.

SR9.2: The system shall be tested for stable operation under factory environmental conditions (temperature, dust, vibration).

SR9.3: The system shall include fault detection and automatic recovery mechanisms.

4.1.4.4 Organizational: Development Requirements
ODUR1 – Open-Source Development

User Requirement:
Utilize open-source libraries and frameworks to minimize licensing costs.

System Requirements:

SR10.1: The system shall use open-source libraries or frameworks unless a commercial dependency is explicitly approved.

SR10.2: All open-source components shall be documented, including their licenses and version numbers.

4.1.4.5 Organizational: Operational Requirements
OOUR1 – Cost-Efficient Performance

User Requirement:
Minimize hardware and deployment costs while meeting performance requirements.

System Requirements:

SR11.1: The system shall run on standard workstation hardware without specialized components.

SR11.2: The system shall maintain performance benchmarks (response time under 1 second) on standard hardware.

OOUR2 – Flexible Deployment

User Requirement:
Support flexible deployment configurations for different workstation setups.

System Requirements:

SR12.1: The system shall support both single-user and multi-user workstation configurations.

SR12.2: The system shall allow configuration for various hardware specifications.

SR12.3: The installation process shall include customizable deployment options.

OOUR3 – Gradual Implementation

User Requirement:
Support gradual implementation with minimal disruption to existing operations.

System Requirements:

SR13.1: The system shall support phased deployment alongside existing systems.

SR13.2: The system shall maintain backward compatibility with legacy data formats.

SR13.3: The system shall provide rollback and restore options during deployment.

4.1.4.6 Organizational: Environmental Requirements

(No user requirements currently defined — section reserved for future development.)

4.1.4.7 External: Legislative Requirements on Safety/Security

(No user requirements currently defined — section reserved for future compliance mapping.)

4.1.4.8 External: Cultural and Social Requirements

(No user requirements currently defined — section reserved for cultural adaptation or workforce diversity considerations.)

4.1.4.9 External: Interoperability Requirements
EIUR1 – Compatibility with Existing Software

User Requirement:
Maintain compatibility with existing KMD Technology Solutions software interfaces.

System Requirements:

SR14.1: The system shall integrate with all existing KMD Technology Solutions APIs and communication protocols.

SR14.2: The system shall maintain consistent data exchange formats used by KMD software products.

EIUR2 – JSON Schema Publication

User Requirement:
Publish comprehensive JSON schema for scan results and system outputs.

System Requirements:

SR15.1: The system shall define and publish a complete JSON schema for all output data.

SR15.2: The JSON schema shall be version-controlled and included in system documentation.

EIUR3 – Manufacturing System Integration

User Requirement:
Support integration with existing manufacturing systems and processes.

System Requirements:

SR16.1: The system shall support data exchange with existing Manufacturing Execution Systems (MES) and ERP tools.

SR16.2: The system shall be configurable to align with existing factory workflows and data pipelines.