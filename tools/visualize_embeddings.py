"""Visualize DINOv2 embedding groupings for action-sequence training data.

Given one or more video files (each representing a step), this script:
  1. Samples frames from each video.
  2. Computes a DINOv2 embedding for every sampled frame.
  3. Projects all embeddings to 2D using PCA.
  4. Plots the projected points, colored by step.
  5. Optionally overlays the centroids stored in a .pkl process file.

Usage
-----
    python -m tools.visualize_embeddings --videos step1.mp4 step2.mp4 step3.mp4
    python -m tools.visualize_embeddings --videos *.mp4 --process process.pkl
    python -m tools.visualize_embeddings --videos step1.mp4 step2.mp4 \
        --sample-every 5 --output embeddings.png

The step name for each video is taken from its filename (without extension).
If multiple videos share the same name, they'll be treated as the same step.

Requirements
------------
    pip install matplotlib
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENCV_LOG_LEVEL", "SILENT")

import cv2
import numpy as np

# Make src/ importable so we can reuse DINOv2 + deserialization code
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from step_validation.embeddings import get_embedding, load_dinov2_model  # noqa: E402
from step_validation.serialization import deserialize_process  # noqa: E402


def sample_frames(video_path: Path, sample_every: int) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(video_path))
    frames: list[np.ndarray] = []
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % sample_every == 0:
            frames.append(frame.copy())
        idx += 1
    cap.release()
    return frames


def compute_embeddings_by_label(
    videos: list[Path], sample_every: int, labels: list[str] | None = None
) -> tuple[np.ndarray, list[str]]:
    """Return (N x 384 matrix, list of N label strings)."""
    all_embs: list[np.ndarray] = []
    all_labels: list[str] = []

    for i, video in enumerate(videos):
        label = labels[i] if labels else video.stem
        print(f"[visualize] {video.name} -> {label!r}: sampling frames...", flush=True)
        frames = sample_frames(video, sample_every)
        if not frames:
            print(f"[visualize]   WARNING: no frames read from {video.name}", flush=True)
            continue

        print(f"[visualize]   computing {len(frames)} embeddings...", flush=True)
        for frame in frames:
            all_embs.append(get_embedding(frame))
            all_labels.append(label)

    if not all_embs:
        raise RuntimeError("No embeddings were computed. Check that the video paths are valid.")

    return np.stack(all_embs), all_labels


def pca_2d(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Project rows of `matrix` to 2D via PCA (SVD).

    Returns (projected (N,2), components (2,D), mean (D,)).
    """
    mean = matrix.mean(axis=0)
    centered = matrix - mean
    # SVD: centered = U * S * Vt  →  top components are rows of Vt
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    components = vt[:2]  # (2, D)
    projected = centered @ components.T  # (N, 2)
    return projected, components, mean


def main():
    parser = argparse.ArgumentParser(description="Visualize DINOv2 embedding groupings.")
    parser.add_argument(
        "--videos", nargs="+", required=True, metavar="PATH",
        help="One or more video files. The filename stem is used as the step label.",
    )
    parser.add_argument(
        "--labels", nargs="+", default=None, metavar="LABEL",
        help="Optional step labels (one per video, in the same order). "
             "Overrides filename-based labeling. Use quotes for multi-word labels.",
    )
    parser.add_argument(
        "--process", type=str, default=None, metavar="PATH",
        help="Optional .pkl process file to overlay its centroids on the plot.",
    )
    parser.add_argument(
        "--sample-every", type=int, default=3, metavar="N",
        help="Sample every Nth frame from each video (default: 3).",
    )
    parser.add_argument(
        "--output", type=str, default=None, metavar="PATH",
        help="Save the plot to this path instead of showing it interactively.",
    )
    args = parser.parse_args()

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("ERROR: matplotlib is required. Install with: pip install matplotlib",
              file=sys.stderr)
        sys.exit(1)

    video_paths = [Path(v) for v in args.videos]
    missing = [p for p in video_paths if not p.exists()]
    if missing:
        print(f"ERROR: video file(s) not found: {missing}", file=sys.stderr)
        sys.exit(1)

    if args.labels is not None and len(args.labels) != len(video_paths):
        print(f"ERROR: got {len(args.labels)} --labels but {len(video_paths)} --videos "
              f"(counts must match)", file=sys.stderr)
        sys.exit(1)

    print("[visualize] Loading DINOv2 model...", flush=True)
    load_dinov2_model()

    embs, labels = compute_embeddings_by_label(video_paths, args.sample_every, args.labels)
    print(f"[visualize] Total embeddings: {len(embs)} across {len(set(labels))} step(s)", flush=True)

    print("[visualize] Running PCA to 2D...", flush=True)
    projected, components, mean = pca_2d(embs)

    # Plot
    unique_labels = sorted(set(labels))
    cmap = plt.get_cmap("tab10" if len(unique_labels) <= 10 else "tab20")
    colors = {lbl: cmap(i % cmap.N) for i, lbl in enumerate(unique_labels)}

    fig, ax = plt.subplots(figsize=(10, 7))
    for lbl in unique_labels:
        mask = np.array([l == lbl for l in labels])
        pts = projected[mask]
        ax.scatter(pts[:, 0], pts[:, 1], s=20, alpha=0.6,
                   color=colors[lbl], label=f"{lbl} ({mask.sum()})")

    # Overlay centroids from .pkl (project them through the same PCA)
    if args.process:
        pkl_path = Path(args.process)
        if not pkl_path.exists():
            print(f"WARNING: .pkl file not found: {pkl_path}", file=sys.stderr)
        else:
            print(f"[visualize] Loading centroids from {pkl_path.name}...", flush=True)
            steps = deserialize_process(pkl_path.read_bytes())
            for step in steps:
                if step.centroid is None:
                    continue
                proj = (step.centroid - mean) @ components.T
                color = colors.get(step.name, "black")
                ax.scatter(proj[0], proj[1], s=250, marker="*",
                           edgecolor="black", linewidth=1.2, color=color, zorder=5)
                ax.annotate(f"  {step.name} (centroid)", (proj[0], proj[1]),
                            fontsize=9, fontweight="bold", zorder=6)

    ax.set_title("DINOv2 Embedding Clusters (PCA 2D)")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=150)
        print(f"[visualize] Saved plot to {args.output}", flush=True)
    else:
        plt.show()


if __name__ == "__main__":
    main()
