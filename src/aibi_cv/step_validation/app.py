import streamlit as st
import cv2
import numpy as np
import time
from dataclasses import dataclass, field
from typing import List, Optional

# --- 1. Backend Logic (State & Embeddings) ---

@dataclass
class ActionStep:
    name: str
    order: int
    centroids: List[np.ndarray] = field(default_factory=list)
    # In a real app, 'centroids' would be the averaged embedding vector

class ProcessManager:
    def __init__(self):
        if 'steps' not in st.session_state:
            st.session_state.steps = []
        if 'current_op_step' not in st.session_state:
            st.session_state.current_op_step = 0

    def add_step(self, name):
        new_order = len(st.session_state.steps)
        st.session_state.steps.append(ActionStep(name=name, order=new_order))

    def get_steps(self):
        return st.session_state.steps

    def clear_steps(self):
        st.session_state.steps = []
        st.session_state.current_op_step = 0

import torch
import torchvision.transforms as T
from PIL import Image

# DINOv2 Model Setup
@st.cache_resource
def load_dinov2_model():
    model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14')
    model.eval()
    return model

# Image preprocessing for DINOv2
transform = T.Compose([
    T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
    T.CenterCrop(224),
    T.ToTensor(),
    T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
])

def get_embedding(frame):
    """Extract DINOv2 embedding from frame."""
    model = load_dinov2_model()
    
    # Convert BGR to RGB and to PIL
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    
    # Preprocess and get embedding
    with torch.no_grad():
        img_tensor = transform(pil_image).unsqueeze(0)
        embedding = model(img_tensor)
        return embedding.squeeze().cpu().numpy() 

def calculate_similarity(embedding, steps):
    """Compare embedding to stored step centroids using cosine similarity."""
    if not steps:
        return -1, 0.0
    
    best_match_idx = -1
    best_similarity = 0.0
    
    for i, step in enumerate(steps):
        if not step.centroids:
            continue
            
        # Calculate average centroid for this step
        step_centroid = np.mean(step.centroids, axis=0)
        
        # Cosine similarity
        similarity = np.dot(embedding, step_centroid) / (
            np.linalg.norm(embedding) * np.linalg.norm(step_centroid)
        )
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_idx = i
    
    return best_match_idx, best_similarity

# --- 2. The User Interface ---

st.set_page_config(layout="wide", page_title="Action Sequence Trainer")
manager = ProcessManager()

st.sidebar.title("System Mode")
mode = st.sidebar.radio("Select Phase:", ["Training (Teach)", "Operation (Monitor)"])

# --- PHASE 1: TRAINING ---
if mode == "Training (Teach)":
    st.title("Phase 1: Teach the Process")
    
    # Step Input
    with st.expander("1. Define Process Steps", expanded=True):
        col1, col2 = st.columns([3, 1])
        new_step_name = col1.text_input("New Step Name (e.g., 'Jack up Car')")
        if col2.button("Add Step"):
            if new_step_name:
                manager.add_step(new_step_name)
                st.success(f"Added: {new_step_name}")

    # Display Steps
    steps = manager.get_steps()
    if steps:
        st.write("### 2. Record Actions")
        
        # Create a container for the video feed
        video_placeholder = st.empty()
        
        # Select which step to train
        selected_step_name = st.selectbox("Select Step to Train:", [s.name for s in steps])
        selected_step_idx = next(i for i, s in enumerate(steps) if s.name == selected_step_name)
        
        col_start, col_stop, col_next = st.columns(3)
        recording = st.session_state.get('recording', False)
        
        if col_start.button("🔴 Start Recording"):
            st.session_state.recording = True
        
        if col_stop.button("⬛ Stop Recording"):
            st.session_state.recording = False
            st.success(f"Saved centroids for '{selected_step_name}'")

        if col_next.button("Next Step >>"):
            # logic to auto-select the next index in dropdown could go here
            st.info("Moved to next step context.")

        # Camera Loop (Simulated)
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened() and not recording:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(frame, caption="Live Feed (Idle)", use_container_width=True)
            # Streamlit needs a small sleep to allow UI interaction updates
            time.sleep(0.03)
            # Break the loop if user clicked start (Streamlit reruns script on interaction)
            if st.session_state.get('recording'): break

        # Recording Loop
        while st.session_state.get('recording'):
            ret, frame = cap.read()
            if not ret: break
            
            # --- CORE LOGIC: EXTRACT & SAVE EMBEDDINGS ---
            emb = get_embedding(frame)
            steps[selected_step_idx].centroids.append(emb)
            # ---------------------------------------------
            
            # Visual Feedback
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.putText(frame, f"RECORDING: {selected_step_name}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            video_placeholder.image(frame, channels="RGB", use_container_width=True)
            time.sleep(0.1) # Throttle to simulate processing time

        cap.release()

# --- PHASE 2: OPERATION ---
elif mode == "Operation (Monitor)":
    st.title("Phase 2: Sequence Verification")
    
    steps = manager.get_steps()
    if not steps:
        st.warning("No process defined. Please go to Training mode first.")
    else:
        # Progress Bar
        current_idx = st.session_state.current_op_step
        progress = current_idx / len(steps)
        st.progress(progress)
        
        # Status Indicators
        st.subheader(f"Expecting: Step {current_idx + 1} - {steps[current_idx].name if current_idx < len(steps) else 'COMPLETE'}")
        
        video_loc = st.empty()
        status_loc = st.empty()
        
        if st.button("Start Monitoring"):
            cap = cv2.VideoCapture(0)
            
            consecutive_matches = 0
            REQUIRED_FRAMES = 5  # Require 5 stable frames to advance step
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                
                # 1. Get Embedding
                emb = get_embedding(frame)
                
                # 2. Classify Action
                detected_idx, conf = calculate_similarity(emb, steps)
                detected_name = steps[detected_idx].name
                
                # 3. SEQUENCE LOGIC
                status_color = (0, 255, 0) # Green by default
                status_text = "Looking for action..."
                
                if current_idx >= len(steps):
                    status_text = "PROCESS COMPLETE!"
                    status_color = (0, 255, 0)
                
                elif detected_idx == current_idx:
                    # Correct step detected
                    consecutive_matches += 1
                    status_text = f"✔ detecting {detected_name} ({consecutive_matches}/{REQUIRED_FRAMES})"
                    
                    if consecutive_matches >= REQUIRED_FRAMES:
                        st.session_state.current_op_step += 1
                        current_idx += 1
                        consecutive_matches = 0
                        status_text = "Step Complete! Moving to next..."
                        
                elif detected_idx > current_idx:
                    # Future step detected (Skipped a step!)
                    status_text = f"⚠ WARNING: Skipped to {detected_name}! (Expected {steps[current_idx].name})"
                    status_color = (255, 0, 0) # Red
                    consecutive_matches = 0
                    
                else:
                    # Past step or noise
                    consecutive_matches = 0
                
                # Visuals
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.putText(frame, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
                
                video_loc.image(frame, use_container_width=True)
                
                # Break condition?
                if current_idx >= len(steps):
                    st.success("Process Completed Successfully!")
                    break