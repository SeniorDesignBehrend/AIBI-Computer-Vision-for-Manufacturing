#!/usr/bin/env python3
"""Test script: decode QR codes from a single image, order them, and save JSON output."""
import argparse
import json
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np


def decode_qr(img):
    """Decode QR/barcodes from image using OpenCV fallback.
    Returns list of (text, points) where points may be None or an array-like Nx2.
    """
    results = []
    try:
        detector = cv2.QRCodeDetector()
        res = detector.detectAndDecodeMulti(img)
        texts = None
        points = None
        if isinstance(res, tuple) and len(res) >= 2:
            for item in res:
                if isinstance(item, (list, tuple)) and item and all(isinstance(x, str) for x in item):
                    texts = list(item)
                elif hasattr(item, 'shape') or (isinstance(item, (list, tuple)) and item and isinstance(item[0], (list, tuple))):
                    points = item
        elif isinstance(res, list):
            texts = res

        if texts:
            for i, t in enumerate(texts):
                if not t:
                    continue
                pts = None
                try:
                    if points is not None:
                        pts = np.array(points[i], dtype=int)
                except Exception:
                    pts = None
                results.append((t, pts))
            if results:
                return results
    except Exception:
        pass

    # fallback: single detect
    try:
        detector = cv2.QRCodeDetector()
        text, pts, _ = detector.detectAndDecode(img)
        if text:
            pts_arr = None
            try:
                pts_arr = np.array(pts, dtype=int) if pts is not None else None
            except Exception:
                pts_arr = None
            return [(text, pts_arr)]
    except Exception:
        pass

    return []


def centroid_of(box):
    if box is None:
        return None, None
    try:
        pts = np.array(box, dtype=float)
        cx = float(pts[:, 0].mean())
        cy = float(pts[:, 1].mean())
        return cx, cy
    except Exception:
        return None, None


def sort_detections(detections, scan_direction: str):
    if not scan_direction or scan_direction == 'any':
        return detections

    def key_fn(item):
        _, box = item
        cx, cy = centroid_of(box)
        if cx is None:
            return (float('inf'), float('inf'))
        if scan_direction in ('row-major', 'left-to-right-down'):
            return (cy, cx)
        if scan_direction == 'right-to-left-down':
            return (cy, -cx)
        if scan_direction in ('column-major', 'top-to-bottom-left-to-right'):
            return (cx, cy)
        if scan_direction == 'left-to-right':
            return (cx, 0)
        if scan_direction == 'right-to-left':
            return (-cx, 0)
        if scan_direction == 'top-to-bottom':
            return (cy, 0)
        if scan_direction == 'bottom-to-top':
            return (-cy, 0)
        return (cy, cx)

    try:
        return sorted(detections, key=key_fn)
    except Exception:
        return detections


def main():
    p = argparse.ArgumentParser(description="Decode and order QR codes in an image")
    p.add_argument("--image", required=True, help="Path to input image containing multiple QR codes")
    p.add_argument("--scan_direction", default="row-major",
                   help="scan direction: any|row-major|left-to-right|right-to-left|top-to-bottom|bottom-to-top")
    p.add_argument("--expected_qr_count", type=int, default=None, help="How many QR codes to collect (optional)")
    p.add_argument("--output", default=None, help="Output JSON path (optional)")
    args = p.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"Image not found: {img_path}")
        return

    img = cv2.imread(str(img_path))
    if img is None:
        print("Failed to read image")
        return

    detections = decode_qr(img)
    if not detections:
        print("No QR detections found")
        return

    ordered = sort_detections(detections, args.scan_direction)

    results = []
    for idx, (text, box) in enumerate(ordered, start=1):
        cx, cy = centroid_of(box)
        results.append({
            "index": idx,
            "text": text,
            "centroid": [cx, cy] if cx is not None else None,
        })

    # If expected_qr_count set, truncate to that many
    if args.expected_qr_count:
        results = results[: args.expected_qr_count]

    out_path = Path(args.output) if args.output else Path("outputs") / f"test_qr_order_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({"workstation_id": "test", "timestamp": datetime.now().isoformat(), "ordered": results}, f, indent=2)

    print(f"Wrote {len(results)} ordered detections to {out_path}")
    for r in results:
        print(f"{r['index']}: {r['text']} -> {r['centroid']}")


if __name__ == '__main__':
    main()
