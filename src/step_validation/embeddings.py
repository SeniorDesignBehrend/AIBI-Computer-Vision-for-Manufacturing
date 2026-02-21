import cv2
import numpy as np
import streamlit as st
import torch
import torchvision.transforms as T
from PIL import Image


@st.cache_resource
def load_dinov2_model():
    model = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14")
    model.eval()
    return model


def _build_transform():
    return T.Compose([
        T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ])


_transform = _build_transform()


def get_embedding(frame: np.ndarray) -> np.ndarray:
    model = load_dinov2_model()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    with torch.no_grad():
        img_tensor = _transform(pil_image).unsqueeze(0)
        embedding = model(img_tensor).squeeze().cpu().numpy()
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm > 0 else embedding
