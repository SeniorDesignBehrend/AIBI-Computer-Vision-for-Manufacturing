# AIBI Computer Vision Project - Meeting Notes

## Meeting Information
- **Date:** October 2nd, 2024
- **Time:** 12:00 PM
- **Attendees:** Daniel Pora, Jacob Dzikowski, Nathan DiGilio, Collin Miller, Kevin DiGilio
- **Recording:** [Microsoft Teams Meeting](https://fathom.video/share/s3YUW-aJfiRQkpMzX3qxRJkR-suGPyay) (56 mins)

---

## Meeting Purpose

Discuss project requirements and implementation details for CompositeFlex's AI-assisted manufacturing process.

## Key Takeaways

- Project has **two main parts:** 1) Barcode scanning for part tracking, 2) Process monitoring for quality control
- Need to determine approach for training AI on workstation processes
- Hardware requirements include **Ubuntu server with GPUs** for video processing
- Integration with existing KMD software needs to be worked out, likely via **API calls**

---

## Topics Discussed

### Barcode Scanning Implementation

#### Environment & Setup
- **No conveyor belts** - parts manually moved between ~12 workstations
- **Fixed camera** at each station to scan paper with multiple barcodes
- Workers currently use scan guns with multiple manual steps prone to error

#### Data Requirements
Barcodes contain:
- **Part number** (design specification - e.g., N-12345)
- **Serial number** (instance identifier - e.g., Serial 1, 2, 3...)
- **Material batch info** (resin batch, fiber spool identifiers)
- **Sub-component tracking** (up to 7 fiber spools, resin batches)

#### Technical Implementation
- Develop **configurable system** to map barcode positions to data fields
- **Position-based identification** (top-left = part number, next = serial, etc.)
- Output **JSON string** with scanned data to integrate with KMD software
- May not need to re-scan all barcodes at every station (cached data)

### Process Monitoring System

#### Real-Time Monitoring
- **Live video feed** of worker performing tasks at each station
- AI to detect if steps are performed in **correct order**
- Focus on **process/steps** rather than final part quality
- **Real-time alerts** when steps performed out of sequence

#### Example Process (Mandrel Operations)
1. ✅ Apply resin to mandrel
2. ✅ Wrap cloth around tube
3. ✅ Apply second layer of resin
4. ✅ Start fiber winding
5. ✅ Additional layers as needed

**Critical:** Missing steps (e.g., cloth before fiber winding) would trigger alerts

#### User Interface
- **Simple UI** for training system on correct process steps
- Video feed with start/stop buttons for step identification
- Non-technical workers should be able to operate training interface

### Training Approach

#### Data Collection
- Capture video of **correct process**, mark start/end of each step
- Need videos showing:
  - ✅ Perfect execution
  - ❌ Common mistakes
  - ❌ Out-of-order operations
  - 📊 Various scenarios (2-step, 7-step processes)

#### Training Interface Requirements
- **Easy-to-use interface** for non-technical workers
- Video capture with step labeling capability
- May need engineering staff for initial setup
- Consider **embedding/centroid technology** for task identification

### Hardware & Software Requirements

#### Infrastructure
- **Ubuntu server** with multiple GPUs for video processing
- **Raspberry Pi cameras** at each workstation (cost consideration)
- **On-premise only** - no cloud services
- **Local network** communication between components

#### Software Preferences
- **Open source software** (MIT/Apache license) to avoid licensing costs
- **Custom web app** likely needed for training interface
- **Real-time processing** capabilities required

#### Workstation Setup
- Each workstation = dumb terminal connected to main Windows server
- Unique user accounts per station (WC_oven, WC_grinder, etc.)
- Remote desktop sessions to central server

### Integration with Existing Systems

#### Current KMD Integration
- KMD software currently uses **barcode scanners as keyboard input**
- Scan guns work like paste operations into text fields
- Workers manually click fields and scan individual barcodes

#### Proposed Integration
- Develop **API endpoints** for receiving scan data
- **Local network communication** between vision system and KMD
- Consider **database table** for intermediate data storage
- API calls must identify workstation and route data correctly

#### Implementation Challenges
- Camera detection triggers scan → API call to KMD
- May need to navigate to correct screen in KMD software
- **JSON to form field mapping** for different part types

### Testing Environment

#### Development Testing
- **No dedicated test environment** at CompositeFlex
- Team should create **simulated workstation** for initial testing
- Use classroom/lab space for proof-of-concept development

#### Production Testing
- Schedule time on **live production floor** for final testing
- Work with engineering staff (Larry, Mike) for coordination
- Use **staging version** of FlexPro for testing
- **Non-production time** required for system validation

---

## Action Items

### Immediate Priorities
- [ ] **Compile comprehensive requirements list** from meeting notes
  - Include both project parts
  - User training process requirements
  - Hardware specifications
  - Software integration points
- [ ] **Prepare demo** of embedding/centroid technology for task identification
  - Include real-time processing capabilities explanation
- [ ] **Contact Dean Lewis** regarding NDA for CompositeFlex project
  - Clarify approval process and timeline
- [ ] **Consolidate team requirement lists** into single document
  - Prepare for review with Kevin at next meeting
  - Include both parts, prioritize key features

### Research & Development
- [ ] **Research open source computer vision libraries** compatible with project needs
- [ ] **Design initial mockup** of training interface for process monitoring
- [ ] **Determine development approach** - parallel vs. sequential for both project parts
- [ ] **Investigate hardware costs** - Raspberry Pi cameras vs. alternatives

### Client Coordination
- [ ] **Schedule factory tour** (pending NDA approval)
- [ ] **Request video samples** from CompositeFlex for training data
- [ ] **Clarify hardware procurement** process and budget

---

## Technical Requirements Summary

### Part 1: Barcode Scanning
- **Multi-barcode detection** from single image/video frame
- **Configurable mapping** of barcode positions to data fields
- **JSON output format** for KMD integration
- **Error handling** for damaged/unclear barcodes
- **Position-based identification** system

### Part 2: Process Monitoring
- **Real-time video analysis** of worker activities
- **Step sequence validation** with out-of-order detection
- **Training interface** for defining process steps
- **Alert system** for process deviations
- **Multiple workstation support** with unique configurations

### Integration Requirements
- **On-premise deployment** only
- **Local API endpoints** for KMD communication
- **Workstation identification** system
- **Database integration** for data persistence
- **User authentication** per workstation

### Hardware Specifications
- **Ubuntu server** with GPU capabilities
- **Camera systems** at each workstation
- **Network infrastructure** for video streaming
- **Cost-effective solutions** prioritized

---

## Next Steps

1. **Requirements Finalization:** Complete comprehensive requirements document
2. **Technology Research:** Investigate specific libraries and frameworks
3. **Development Planning:** Decide on parallel vs. sequential development approach
4. **Academic Coordination:** Consult with Professor Liao on technical approach
5. **Legal Coordination:** Complete NDA process for site access
6. **Proof of Concept:** Begin development of simplified test scenarios

---

## Meeting Transcript Summary

*The full meeting transcript has been preserved below for reference and detailed review of all technical discussions and context.*

---

## Full Meeting Transcript

### Opening and Requirements Discussion (0:00 - 2:40)

**0:06 - Kevin DiGilio:** How's it going?

**0:07 - Daniel Pora:** Hello.

**0:08 - Miller, Collin:** moly.

**0:08 - Kevin DiGilio:** This Dan Pora character gave me a really long list of questions. Yeah. Holy moly. We better, well, I guess your Fathom's here, so we can skip my Fathom. We showed up to a meeting and someone sent their, it was Fixer AI, and they didn't show up.

**0:33 - Daniel Pora:** Really? Nope.

**0:35 - Miller, Collin:** We ain't doing that.

**0:36 - Kevin DiGilio:** I ain't playing that game. You know, we need humans here. Oh. Yeah.

*[Discussion about AI meeting tools and attendance]*

**1:37 - Daniel Pora:** So we need to get a ton of user requirements. So just anything that we need to know about the project.

**1:47 - Kevin DiGilio:** Yeah, Nathan was describing the waterfall nature of these things. So... Yep.

### Factory Environment - No Conveyors (2:40 - 4:30)

**2:41 - Kevin DiGilio:** So number one, on the conveyors, will there be overlapping items? This one's easy. There are no conveyors. So let's be clear about the operating environment that I'm picturing, at least our test zone. Yeah. So there's a big open factory, and there's a bunch of workstations all around the factory. And there's no automation to move. The thing from place to place. So it's not really like an assembly line. While they may operate in an assembly line fashion, it's more of like this station over here is in charge of the first layup.

**[Continued explanation of 12 workstations, manual movement, fixed cameras]**

### Barcode Paper and Data Tracking (4:30 - 11:30)

**4:34 - Daniel Pora:** So you talk about a piece of paper a lot with a bunch of barcodes on it. Is it going to be attached or is someone just going to wave this in front to show?

**4:44 - Kevin DiGilio:** Well, that's up for a decision on how they're actually going to do it. But right now, this piece of paper travels with the part and they're using a scan gun. Yeah. And they go into the software and they click on field one and then they scan barcode one. And they click on field two, the next text box, and then they scan the second barcode...

**[Detailed explanation of current manual scanning process and error-prone nature]**

**7:21 - Kevin DiGilio:** We absolutely need the piece of paper because what the piece of paper has is the part number, right? So the part number is the overall design that the engineer built, right? So let's say N dash one, two, three, four, five. Okay, so that's the part they're building. Well, that's the design of the part, but then it has a serial number, right?

**[Explanation of part numbers vs. serial numbers, missile tube example]**

### JSON Output and KMD Integration (11:30 - 22:30)

**15:01 - Daniel Pora:** So you talk about us outputting a big JSON string. How integrated do we want to be with KMD? Do we want to just give KMD this, or do we want to build the systems on KMD to handle this?

**15:21 - Kevin DiGilio:** Well, right now the way it works is because they're using a scan gun, a scan gun works just like a keyboard. Yeah. Right?

**[Discussion of current keyboard input method vs. proposed API integration]**

**19:25 - Kevin DiGilio:** I mean, these API calls are not going to be Azure calls, right? This is all on-prem on a local network.

**19:33 - Kevin DiGilio:** Okay, yeah. So the API call is going to be like localhost, something, something, right?

### Project Parts and Development Approach (22:30 - 24:50)

**22:31 - Daniel Pora:** Okay. So we know how there's kind of two parts of this project. Should we treat it as two parts? Like try to get the first one done first and then second one? We can talk to our advisor about this since it's technically two parts. Like how do I separate it? Probably not going to be two documents for one, but yeah. What's the priority on the first versus the second?

**23:07 - Kevin DiGilio:** I would say. Okay, the first one, this barcode scanning, seems more attainable, and I think they have a lot of stuff ready to support us there, right, so test data, test cases... should be an easy win. Yeah. And the second one is a really cool idea that we're not sure how much you guys can do...

### Process Monitoring - Correct Order vs. Quality (24:50 - 26:15)

**24:53 - Dzikowski, Jacob John:** I thought we talked about that. Uh, direction of, um, things that happened. Versus seeing them if they did it correctly, like how we discussed it correctly was not going to be the way we went down, because that's too hard.

**25:21 - Kevin DiGilio:** Well, let me let me rephrase correctly in the right order. Okay. Right, like maybe I'm supposed to sand it, then I'm supposed to scrape some edges, then I'm supposed to flip it over, sand it, scrape some edges. I'm just making, making stuff up here, but if we, if we can identify what the seven steps are, and just make sure they happen in the right order.

### Training Interface Requirements (26:15 - 35:00)

**26:15 - Daniel Pora:** I'm going to go through a little, a couple more questions. So what's going to be our process of, I guess, their process of training it? Because we're going to have to get trained data from it. But if they use us for different stuff, we're not always going to be there. So we might have to implement a way for them to train it. Is that something we do, do think? Give them a way to train it?

**26:50 - Kevin DiGilio:** It does seem like a requirement. Okay. You know, they would identify, you know, because now we're talking about how do we determine the steps for a workstation?

**[Discussion of training interface, video capture, step identification]**

**30:34 - Nathan DiGilio:** Yeah, I can show you when we meet as a group next. I can show you the demo that I had for one of the technologies I found, which was basically creating embeddings and kind of making a centroid of what each task is, and then comparing it to the current frame.

### Data Reliability and Site Access (33:30 - 36:00)

**33:34 - Daniel Pora:** Yeah, how, when I was working with Rhonda was CompositeFlex the same place? Okay, how reliable are they going to be with our data? With, like, trying to give us videos and pictures of this stuff?

**33:56 - Kevin DiGilio:** Great question. Do not have an answer. Okay. But I'm prepared to, in the event where they cannot produce these things for us, to drive out there and take some videos.

**34:10 - Daniel Pora:** So they want me to come in and tour.

**34:12 - Kevin DiGilio:** They like that idea. just, I like the work from home, so I haven't done that yet. And there's coordination, right? I'm supposed to bring you guys. And I think Larry even agreed to you guys having a tour...

### Testing Environment (37:00 - 41:20)

**37:19 - Daniel Pora:** Yeah, so we talked about the result output, kind of talked about the testing environment. That kind of just means like, oh yeah. Yeah, so once we kind of confidently have a system that we're ready to install, what's our testing environment going to look like?

**37:58 - Kevin DiGilio:** Well, I would say that before we go to the factory, we will have done enough testing in our own fake little factory. Mm-hmm. That's maybe, you know, the room that I see behind you or a classroom or a something. Right. So I feel like we should be able to create a lot of things that simulate what we're talking about. Yeah. But they don't have a test environment. Right. So we're going to walk into their live factory floor.

### Video Processing and Hardware (41:20 - 44:00)

**41:20 - Daniel Pora:** Yeah. So our advisor, Liao, knows a bit about AI, and he was talking to us about processing video and how it's very intensive. Processed video. I'm not sure if he was talking about this for the first or second part, but how do we plan on processing the video?

**42:48 - Kevin DiGilio:** This is a live feed of a human doing it right now. And we need to smack him in the middle of his stuff. Yes. Right.

**42:55 - Nathan DiGilio:** So I mean, this is a real time, like my my demo was real time, and I was just processing groups of frames. Okay. And it's like, I was just describing it as it's a lot more work. But I was also processing live video on my laptop...

**43:23 - Kevin DiGilio:** And Nathan, I think you have a general appreciation for the hardware involved, right? Yeah. An Ubuntu server with a whole bunch of GPU. I mean, we have a Dell that we chose, but it's very similar to, we chose a smaller model. But it's got, you know, Buko GPUs and reasonable RAM.

### Software Licensing and Hardware Costs (44:00 - 46:30)

**44:23 - Nathan DiGilio:** For at least the LLM project that we did over the summer, we decided to look for like MIT or Apache 2.0 license because those are kind of open source. Anyone can use them for most purposes.

**44:35 - Kevin DiGilio:** Yes, we love the MIT. That's at least what we did. Okay.

**45:11 - Kevin DiGilio:** I don't see any other direction. Yeah. But obviously ask the school first. Maybe they have some magical hidden budget.

*[Discussion about Penn State president's 47% raise while closing campus services]*

### Process Focus - Part 2 Requirements (47:00 - 50:00)

**46:32 - Daniel Pora:** So, I think… Yeah, I kind of went through most of my questions, I think I have, like, one left, so for the second part, are we focusing on the person, or the part? I think we kind of answered this before, but… Are we focusing more on the process?

**47:14 - Nathan DiGilio:** Yeah, part two. I would guess process because if we looked at the part, we would only know if it was like done right after the fact or wrong after the fact, whereas we're trying to tell them that they're in the wrong order. like as they're doing it.

**[Detailed mandrel process example with resin, cloth, fiber sequence]**

**49:43 - Daniel Pora:** It sounds almost like what Amazon does with their drivers, where they'll have like cameras pointing towards the drivers to make sure they're doing the right thing, like having their seatbelt on or not being on their phone.

### NDA and Final Planning (50:00 - End)

**50:07 - Daniel Pora:** from the NDA to Dean Lewis.

**50:13 - Kevin DiGilio:** No. I have not. You can feel free to do that for me. I think it's yours up.

**50:30 - Nathan DiGilio:** Oh, I didn't think I had any jobs.

**50:30 - Kevin DiGilio:** You have a client mentor.

**51:06 - Kevin DiGilio:** Well, I enjoyed question number 15.

**51:06 - Nathan DiGilio:** That's just open-ended enough to think of that's an ongoing question yeah I might have related more towards do we want part one part two both done yeah yeah I wrote that with that in mind sorry cool that was good I think for next meeting we should try to have as many requirements as we can yeah at least just a list like we don't need the story cards or whatever we just need as many requirements and then we can kind of go over those with Kevin and see if he's got any additions critiques things that uh if we're on the right track or not

**52:25 - Kevin DiGilio:** And then you guys are to figure out part one, part two, do them in parallel, do them in serial, right? Yeah. Yeah, we'll ask.

**52:34 - Daniel Pora:** I anticipate them saying just do it in parallel or at least plan for it.

**53:33 - Kevin DiGilio:** Yeah, I'm guessing it's not likely going to be part of KMD. Okay. Just because I don't see any real great reasons to put it in that software. Like Nathan, I'm kind of picturing what you and Max put together, just that simple web page. Yeah. It could just be something like that, that, you know, it's got a video feed and a couple of buttons on it.

---

*Meeting concluded at approximately 55:47 with plans for comprehensive requirements documentation and next steps coordination.*