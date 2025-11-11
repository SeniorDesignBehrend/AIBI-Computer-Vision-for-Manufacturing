# AIBI Computer Vision Project - Meeting Notes

## Meeting Information
- **Date:** September 19th, 2024
- **Time:** 3:30 PM
- **Attendees:** Daniel Pora, Jacob Dzikowski, Nathan DiGilio, Collin Miller, Kevin DiGilio
- **Recording:** [Microsoft Teams Meeting](https://fathom.video/share/JeN1gLfvzn9MjybLjwa2Dszn96c4vh1_) (62 mins)

---

## Meeting Purpose

Introduce AIBI's computer vision project for manufacturing quality control and discuss technical requirements and implementation strategies.

## Key Takeaways

- Project aims to streamline part tracking and quality control in manufacturing using computer vision and AI
- Two main components: barcode/QR code scanning and human activity monitoring for process adherence
- Implementation challenges include on-premise deployment, varying workstation setups, and integrating with existing systems
- Weekly meetings scheduled for Thursdays 12-1 PM; team to provide agenda by Tuesday

---

## Topics Discussed

### AIBI Background and Project Overview

**AIBI** spun off from **KMD Technology Solutions** to develop on-premise AI solutions for manufacturers:

- **Previous projects:** quote generation assistance and automated test creation from work instructions
- **Current focus:** computer vision for part tracking and quality control in manufacturing processes
- **Target customers:** Manufacturers with government contracts requiring heavy regulations and on-premise data storage

### Part Tracking System Requirements

#### Barcode/QR Code Detection
- Detect and decode **multiple barcodes/QR codes** from a single image or video frame
- Handle various scenarios:
  - Paper with multiple codes
  - Individual part barcodes
  - Etched identifiers on large parts (e.g., mandrels)
- Ensure **high accuracy** and ease of use for factory workers in challenging environments (gloves, safety equipment)
- Potential implementation: Raspberry Pi with cameras or centralized server-based processing

#### Technical Challenges
- **Barcode ordering:** Determine sequence for JSON output (top-left, top-down, left-to-right)
- **Damage resilience:** Handle damaged or unclear barcodes during transit
- **Mixed formats:** Support both traditional barcodes and 2D QR codes
- **Configuration:** Adaptable system for different workstation setups

### Human Activity Monitoring

#### Process Adherence Tracking
- Track worker adherence to **multi-step processes** at each workstation
- Use computer vision to detect completion of steps (e.g., applying cloth before resin)
- Provide **real-time feedback** and alerts for out-of-order operations
- **Challenge:** Accounting for variations in human behavior and camera angles

#### Implementation Example
**Mandrel Wrapping Process:**
1. ✅ Apply cloth to mandrel
2. ✅ Apply resin over fabric

**System Features:**
- Checkboxes on computer screen showing required steps
- Green checkmarks when steps completed in order
- **Alerts/alarms** when steps performed out of sequence
- Computer operator monitors while worker performs tasks

### Technical Considerations

#### Infrastructure
- **Platform:** On-premise deployment using Ubuntu server with Python
- **Hardware:** Evaluate need for GPUs vs. CPU-only processing
- **Network:** Consider constraints for video streaming from multiple workstations
- **Video Quality:** Aim for lower-quality feeds to reduce bandwidth and cost

#### Development Approach
- Leverage existing computer vision models and libraries where possible
- Focus on **application** rather than inventing new ML algorithms
- **Cost-effective solutions:** Prioritize affordable hardware (Raspberry Pi vs. high-end cameras)

#### System Architecture
- **Workstations:** Dumb terminals connected to main Windows server
- **AI Processing:** Separate Ubuntu server with Python APIs
- **Video Feeds:** Labeled by workstation (e.g., "Workstation 1")
- **Integration:** JSON output to existing KMD systems

### Documentation and Deployment

- Emphasis on **thorough documentation** (200-300 pages expected)
- Plan for easy deployment and maintenance in factory environments
- Create configurable system to adapt to different workstation setups
- **Real-world testing:** On-site validation in actual manufacturing environment

---

## Action Items

### Team Responsibilities
- [ ] **Nathan:** Schedule recurring Thursday meetings (12-1 PM) and reach out to Professor Liao
- [ ] **Team:** Compile and email questions daily to kevin@aibi.com
- [ ] **Team:** Investigate NDA requirements with Professor Ibrahim
- [ ] **All:** Connect with Kevin on LinkedIn for project updates and networking
- [ ] **Team:** Research existing computer vision technologies applicable to the project
- [ ] **Team:** Prepare detailed questions for next meeting, focusing on technical feasibility and implementation strategies
- [ ] **Team:** Send full name and address for NDA documents

### Meeting Protocol
- **Weekly meetings:** Thursdays 12-1 PM
- **Agenda submission:** Email agenda to Kevin by Tuesday each week
- **Communication:** Send organized daily emails with questions to kevin@aibi.com
- **Documentation:** Meeting recordings and notes via Fathom AI

---

## Technical Research Areas

### Immediate Focus
1. **Barcode/QR Detection Libraries** - Research existing Python libraries for multi-code detection
2. **Computer Vision Models** - Investigate models for activity recognition and object detection
3. **Hardware Requirements** - Analyze GPU vs. CPU needs for real-time processing
4. **Edge Computing** - Evaluate Raspberry Pi capabilities for distributed processing

### Future Considerations
1. **Network Architecture** - Design for multiple workstation video feeds
2. **Configuration Systems** - Develop adaptable setup for different factory layouts
3. **Integration APIs** - Plan JSON data format for KMD system integration
4. **Performance Optimization** - Balance accuracy with processing speed requirements

---

## Next Steps

1. **Academic Consultation:** Meet with Professor Liao to discuss technical approaches
2. **Legal Preparation:** Coordinate NDA requirements with Professor Ibrahim
3. **Technology Research:** Begin investigating relevant computer vision libraries and models
4. **Proof of Concept:** Plan simple demonstrations (similar to Nathan's pen assembly example)
5. **Requirements Gathering:** Prepare detailed technical questions for manufacturer consultation

---

## Meeting Transcript Summary

*The full meeting transcript has been preserved below for reference and detailed review of all technical discussions and context.*

---

## Full Meeting Transcript

### Connection and Introductions (0:00 - 7:30)

**1:27 - Daniel Pora:** Yo. Yo. Do hear me?

**1:34 - Nathan DiGilio:** Yeah.

**1:34 - Miller, Collin:** No.

**1:35 - Daniel Pora:** Yes. Good. Can I just paste it real quick? Thank you.

*[Brief informal discussion about climbing and activities]*

**3:15 - Kevin DiGilio:** How's it going? Hi.

**3:16 - Miller, Collin:** How are we doing? I'm pretty good.

**4:22 - Nathan DiGilio:** For we have Fathom in here, which is an AI note taker, it automatically records the video and does a pretty good job taking notes on action items and such.

**4:36 - Kevin DiGilio:** And it's going to kick out an email to everybody here with the summary. And what's cool is it has a link at the bottom that you can actually get in there and use a tool called Ask Fathom that works a lot like chat, except it knows everything about the meeting, the transcript, who is there, who said what.

### AIBI Company Background (7:30 - 11:30)

**7:28 - Kevin DiGilio:** So I have a company that Nathan has worked with for, I don't know, five plus years and Dan has played along. It's called KMD Technology Solutions. And we provide project management, service request management, and kind of general workflow management software to manufacturers.

**[Continued explanation of KMD's focus on government-regulated manufacturers]**

**11:12 - Kevin DiGilio:** And what we found is that these folks like to keep their data on-prem. They can't use the cloud. And I mean, can't is kind of in air quotes. There are a number of cloud entities that support. They typically cost more, but there's still kind of a general mistrust of the cloud because once your data leaves your facility, you can't really get it back.

### AIBI Formation and Previous Projects (11:30 - 15:00)

**Kevin DiGilio:** So, as we are kind of installing these systems and working with these companies, we found that there's a ton of work that we think AI can do for them. They can't use AI like we all understand it, so we need an on-prem AI solution. And so, back in November, we started AIBI with that kind of goal in mind.

**[Discussion of three primary goals: quote assistance, work instruction testing, and current computer vision project]**

### Part Tracking System Requirements (15:00 - 22:00)

**15:57 - Kevin DiGilio:** So we see this opportunity where one person has the room to make a lot of mistakes with this barcode scanner. They scan things in the wrong order, or if the scanner kind of sucks and doesn't work, or if the barcode's kind of crappy. There's just a lot of room for error.

**16:01 - Kevin DiGilio:** So we believe that if we have a piece of paper that has all the barcodes on it, let's just say there's 20 on there, we believe that we don't need barcode scanners anymore because computer vision with a single frame of those barcodes should be able to detect everything that's on there.

**18:22 - Kevin DiGilio:** So how are we feeling in general about, you know, the idea of a part moving through a factory, and the fact that this piece of paper with barcodes kind of goes with it?

**18:39 - Dzikowski, Jacob John:** So this is more so, rather than like object recognition, it's more so recognizing the barcodes that are moving along with the parts that are needed. So like, don't, we don't have to recognize the part, we just have to recognize that there's a barcode there, and then get the information from the barcode?

**18:58 - Kevin DiGilio:** I would say mostly yes. But a challenge that I know they're going to introduce. This is that some things that need scanned can't have barcodes, so there may be a little bit of object detection...

### Human Activity Monitoring (22:00 - 32:00)

**Kevin DiGilio:** The second piece is more human tracking, right? So these folks that get hired, they come from temp agencies. They sometimes don't speak our language. And so in the very early stages of things, things can go wrong often.

**[Detailed explanation of the mandrel wrapping process example]**

**28:54 - Kevin DiGilio:** One says apply cloth, one says apply resin. And then when the camera sees him put the cloth on, a green. Checkmark shows up, and now we know it's okay to apply the resin, and then when he applies the resin, the checkmark checks, right, and we kind of keep going with this nice, happy, smiley face, green checkmarks, but then if something goes out of, you know, goes out of order, then we would want some sort of flashy something, maybe an alarm to go off...

### Technical Infrastructure Discussion (32:00 - 48:00)

**42:16 - Kevin DiGilio:** So I don't even have any idea what to tell you to start with, except that I know that it's possible because I've seen it applied places.

**43:29 - Kevin DiGilio:** So each workstation, while it has computer hardware, it's really kind of a dumb terminal. It's got a mouse, a scanner, a keyboard, a screen, and then this little box that's Velcroed to the back of the monitor that remotes into the main server.

**45:09 - Nathan DiGilio:** Python and Ubuntu is kind of AI's favorite place for the most part.

**45:41 - Nathan DiGilio:** Unless you wanted to go down the route of having like a Raspberry Pi with a camera that sends just data.

### Meeting Logistics and Action Items (48:00 - End)

**48:54 - Nathan DiGilio:** And then I guess for bookkeeping, we would like to meet weekly.

**49:44 - Kevin DiGilio:** 12 to 1.30. Okay. Yeah, I do have that one at 12.30. I could probably shuffle that somewhere else. So that would leave a 12 to 1 every Thursday.

**52:43 - Kevin DiGilio:** And a rule that kind of happens on meetings that people press upon me is that, you know, at least a couple of days before the meeting have an idea of what the agenda is.

**53:38 - Kevin DiGilio:** I would say an organized email per day with all the questions would probably help us keep track of it.

**55:28 - Nathan DiGilio:** Yeah, I can send an email tonight to Liao asking for time to meet next week and Professor Ibrahim about NDA questions.

**55:45 - Kevin DiGilio:** Yeah, and if it's just mine, then it's no problem. I'll just, what I'll want, if I have to make it, I need a name and address, so whatever your legal name is and whatever address to make you different...

**57:38 - Kevin DiGilio:** Okay, and you guys can all connect with me on LinkedIn. Anytime anything cool happens, I'll probably brag about you.

---

*Meeting concluded at approximately 1:01:31 with plans for next Thursday meeting at 12:00 PM.*