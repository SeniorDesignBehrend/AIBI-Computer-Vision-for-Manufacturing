import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoImageProcessor, AutoModel
from PIL import Image
import numpy as np

# --- Configuration ---
MODEL_NAME = "facebook/dinov2-small"  # Using small for speed; swap for 'base' or 'giant'
EMBEDDING_DIM = 384  # DINOv2-small output dim
PROJECTION_DIM = 128 # Compressed dimension for metric learning
MARGIN = 1.0         # Distance margin for Triplet Loss
LR = 0.001

class ActionNet(nn.Module):
    def __init__(self):
        super().__init__()
        print(f"Loading {MODEL_NAME}...")
        self.processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        self.backbone = AutoModel.from_pretrained(MODEL_NAME)
        
        # Freeze backbone (DINOv2 is already very strong)
        for param in self.backbone.parameters():
            param.requires_grad = False
            
        # Learnable Projection Head: Maps generic visual features to "Action" space
        self.head = nn.Sequential(
            nn.Linear(EMBEDDING_DIM, 256),
            nn.ReLU(),
            nn.Linear(256, PROJECTION_DIM),
            nn.LayerNorm(PROJECTION_DIM) # Normalization helps stability in metric learning
        )

    def forward(self, images):
        # 1. Extract raw features from DINOv2
        with torch.no_grad():
            inputs = self.processor(images=images, return_tensors="pt").to(self.backbone.device)
            outputs = self.backbone(**inputs)
            # DINOv2 CLS token is at index 0
            raw_embeddings = outputs.last_hidden_state[:, 0, :]
            
        # 2. Project to metric space
        projected = self.head(raw_embeddings)
        
        # 3. L2 Normalize (Crucial for Cosine/Euclidean distance stability)
        return F.normalize(projected, p=2, dim=1)

def compute_centroids(embeddings, labels, num_classes):
    """
    Calculates the mean vector (centroid) for each class in the current batch.
    In a real production system, you would maintain a running average (EMA) of these.
    """
    centroids = torch.zeros((num_classes, embeddings.shape[1]), device=embeddings.device)
    
    for c in range(num_classes):
        mask = (labels == c)
        if mask.sum() > 0:
            class_embeddings = embeddings[mask]
            centroids[c] = class_embeddings.mean(dim=0)
            
    # Normalize centroids so they stay on the hypersphere
    return F.normalize(centroids, p=2, dim=1)

def centroid_triplet_loss(embeddings, labels, centroids, margin=1.0):
    """
    Computes loss based on distance to the CORRECT centroid vs INCORRECT centroids.
    """
    loss = 0.0
    valid_samples = 0
    
    for i, emb in enumerate(embeddings):
        label = labels[i]
        
        # Positive: Distance to the centroid of the correct class
        pos_centroid = centroids[label]
        # Using Euclidean distance squared
        dist_pos = torch.sum((emb - pos_centroid) ** 2)
        
        # Negative: Find the closest INCORRECT centroid (Hard Negative Mining)
        dist_neg = float('inf')
        for c_idx, centroid in enumerate(centroids):
            if c_idx == label:
                continue # Skip self
            
            d = torch.sum((emb - centroid) ** 2)
            if d < dist_neg:
                dist_neg = d
        
        # Triplet Loss: max(d_pos - d_neg + margin, 0)
        # We want d_pos (dist to own class) to be small
        # We want d_neg (dist to other class) to be large
        current_loss = F.relu(dist_pos - dist_neg + margin)
        
        loss += current_loss
        valid_samples += 1
        
    return loss / max(valid_samples, 1)

# --- Mock Training Loop ---
def run_experiment():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ActionNet().to(device)
    optimizer = torch.optim.AdamW(model.head.parameters(), lr=LR)
    
    # Fake Data: 3 Classes (e.g., Walk, Run, Jump)
    # Creating random noise images just to verify the pipeline flows
    num_classes = 3
    batch_size = 6
    
    print("\nStarting simulated training loop...")
    model.train()
    
    for epoch in range(5):
        # 1. Create Dummy Batch (Random noise images)
        # In real life: load frames from video clips
        fake_images = [Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)) for _ in range(batch_size)]
        
        # Ensure at least one sample per class for centroid calculation in this toy example
        labels = torch.tensor([0, 0, 1, 1, 2, 2]).to(device)
        
        optimizer.zero_grad()
        
        # 2. Forward Pass
        embeddings = model(fake_images)
        
        # 3. Calculate Centroids (Prototypes) based on current batch
        centroids = compute_centroids(embeddings, labels, num_classes)
        
        # 4. Compute Loss
        loss = centroid_triplet_loss(embeddings, labels, centroids, margin=MARGIN)
        
        # 5. Backprop
        loss.backward()
        optimizer.step()
        
        print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")
        
    print("\nTraining Complete. Centroids are now 'trained' to separate these actions.")
    print("Shape of stored centroids:", centroids.shape)

if __name__ == "__main__":
    run_experiment()