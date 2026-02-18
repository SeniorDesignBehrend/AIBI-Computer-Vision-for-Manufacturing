# Step Validation App

A Streamlit application that learns a sequence of manufacturing steps from a live camera feed and then verifies that an operator performs them in the correct order.

## How It Works

### Core Idea

The app uses **DINOv2** (a vision transformer from Meta) to extract a compact numerical "fingerprint" (embedding) from each camera frame. Steps are distinguished by comparing these fingerprints — visually similar frames produce similar embeddings, visually different ones do not.

Each trained step is represented by a single **centroid**: the average of all its training embeddings, normalized to unit length. During operation, every incoming frame is compared to all centroids using **cosine similarity** (dot product, since both vectors are normalized). The closest centroid above a confidence threshold is the predicted step.

---

## Workflow

### Phase 1 — Training

1. **Define steps** — enter a name for each step in the process (e.g. "Pick up part", "Insert bolt", "Torque to spec") and click **Add Step**.
2. **Record each step** — select a step from the dropdown, click **Start Recording**, perform the action in front of the camera for a few seconds, then click **Stop Recording**. Repeat for every step.
3. **Clear a bad recording** — if a recording was off (wrong angle, distraction), click **🗑 Clear Recording** for that step and re-record without affecting the others.
4. **Finalize** — once every step has at least one recorded frame, click **✅ Finalize Training**. This averages and normalizes all captured embeddings into one centroid per step. Only the centroid is used at inference time.
5. **Save** — after finalization a **💾 Save Process** button appears. Click it to download a `.pkl` file containing all step centroids. This file can be loaded in future sessions to skip retraining.
6. **Load** — use the **📂 Load Saved Process** file uploader to restore a previously saved process. The app immediately marks training as finalized and you can switch straight to Operation mode.

### Phase 2 — Operation

Switch to **Operation (Monitor)** in the sidebar.

The app shows a live checklist of steps with the current expected step highlighted. Click **Start Monitoring** to begin.

For each camera frame the app:
1. Extracts a DINOv2 embedding.
2. Computes cosine similarity against every step centroid.
3. Assigns the frame to the best-matching step — or marks it **IDLE** if the score is below the similarity threshold.
4. Adds the frame's vote to a **sliding window** of the last N frames.
5. **Confirms** the current step when enough frames in the window agree (majority vote).

Once confirmed, the app advances to the next step and the window resets.

---

## Verification States

| State | Meaning | Overlay Color |
|---|---|---|
| `IDLE` | No step detected above threshold | Gray |
| `CORRECT_STEP` | Expected step detected, building votes | Green |
| `CONFIRMED` | Vote threshold met — step complete | Bright green |
| `WRONG_ORDER` | A previously completed step re-detected | Orange |
| `SKIPPED` | A future step detected before current is confirmed | Red |
| `COMPLETE` | All steps finished | Bright green |

---

## Tuning Parameters (Operation sidebar)

| Parameter | Default | Effect |
|---|---|---|
| **Similarity Threshold** | 0.75 | Frames scoring below this are IDLE. Raise it if you get false matches; lower it if the step is hard to detect. |
| **Window Size** | 10 | Number of recent frames used for voting. Larger = more stable but slower to react. |
| **Required Votes** | 7 / 10 | Frames in the window that must agree to confirm a step. Higher = fewer false confirmations. |

---

## Run History

After each monitoring session ends (complete or interrupted), the run is saved to a **Run History** expander at the bottom of the page. Each entry shows:
- Run number and start time
- Whether the run completed
- Per-step results with any warnings (wrong-order detections or skips) that occurred during that step

Run history persists for the duration of the browser session and is cleared if steps are reset.

---

## Running the App

```bash
uv run streamlit run src/aibi_cv/step_validation/app.py
```

Requires a webcam on device index `0`.

## Dependencies

- `streamlit`
- `torch` + `torchvision`
- `opencv-python`
- `Pillow`
- `numpy`
