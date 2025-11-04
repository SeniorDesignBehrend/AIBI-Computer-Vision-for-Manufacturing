#!/usr/bin/env python3
"""
qr_test.py — A simple QR code testing harness.

Usage examples:
  # 1) Live webcam scan, annotate window, write detections.csv
  python qr_test.py --webcam --out out_live

  # 2) Batch test images in a folder, save annotated images + detections.csv
  python qr_test.py --dir test_imgs --out out_batch

  # 3) Batch test with ground truth to get accuracy metrics
  python qr_test.py --dir test_imgs --labels labels.csv --out out_scored
"""

import argparse
import csv
import os
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Tuple, Optional

import cv2
import numpy as np

# --------- Decoders ---------

def _decode_opencv(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Decode using OpenCV's QRCodeDetector (no extra deps)."""
    det = cv2.QRCodeDetector()
    try:
        result = det.detectAndDecodeMulti(img)
        if len(result) == 3:
            texts, points, _ = result
        else:
            texts, points = result
    except Exception:
        # Fallback to single if multi not present on some builds
        result = det.detectAndDecode(img)
        if len(result) == 3:
            text, pts, _ = result
        else:
            text, pts = result
        texts, points = ([text] if text else []), (np.array([pts]) if pts is not None else None)

    results = []
    if points is not None and len(points) > 0:
        for i, txt in enumerate(texts):
            if txt is None or txt == "":
                continue
            # points[i] is 4x2
            box = points[i].astype(np.int32)
            results.append((txt, box))
    return results

def _decode_pyzbar(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Decode using pyzbar if installed."""
    try:
        from pyzbar.pyzbar import decode
    except ImportError:
        return []
    out = []
    for d in decode(img):
        txt = d.data.decode("utf-8", errors="replace")
        pts = np.array([(p.x, p.y) for p in d.polygon], dtype=np.int32)
        if pts.shape[0] == 4:
            box = pts
        else:
            # approximate a quad
            rect = cv2.minAreaRect(pts)
            box = cv2.boxPoints(rect).astype(np.int32)
        out.append((txt, box))
    return out

def decode_qr(img: np.ndarray) -> List[Tuple[str, np.ndarray]]:
    """Try OpenCV first, then pyzbar as fallback; merge unique results."""
    seen = set()
    results = []
    for decoder in (_decode_opencv, _decode_pyzbar):
        for txt, box in decoder(img):
            key = (txt, tuple(map(int, box.flatten())))
            if key not in seen:
                seen.add(key)
                results.append((txt, box))
    return results

# --------- Utilities ---------

def draw_boxes(img: np.ndarray, detections: List[Tuple[str, np.ndarray]]) -> np.ndarray:
    out = img.copy()
    for txt, box in detections:
        cv2.polylines(out, [box], True, (0, 255, 0), 2)
        pt = box[0].flatten()
        x, y = int(pt[0]), int(pt[1])
        cv2.putText(out, txt[:64] + ("…" if len(txt) > 64 else ""), (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(out, txt[:64] + ("…" if len(txt) > 64 else ""), (x, y - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
    return out

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

@dataclass
class DetectionRow:
    source: str     # file path or "webcam"
    frame: int      # frame index for webcam, else 0
    text: str
    timestamp: float

def write_csv(rows: List[DetectionRow], out_csv: str):
    ensure_dir(os.path.dirname(out_csv) or ".")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "frame", "timestamp", "text"])
        for r in rows:
            w.writerow([r.source, r.frame, f"{r.timestamp:.3f}", r.text])

def load_labels(path: str) -> dict:
    """
    labels.csv format (no header):
        filename,expected_text
    """
    truth = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            fname, expected = row[0].strip(), ",".join(row[1:]).strip()
            truth[fname] = expected
    return truth

# --------- Batch mode ---------

def run_dir(dir_path: str, out_dir: str, labels_csv: Optional[str] = None) -> None:
    ensure_dir(out_dir)
    rows: List[DetectionRow] = []
    img_exts = {".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tif", ".tiff"}
    files = [f for f in os.listdir(dir_path) if os.path.splitext(f)[1].lower() in img_exts]
    files.sort()

    truth = load_labels(labels_csv) if labels_csv else None
    per_file_ok = []
    not_found_truth = []

    for fname in files:
        path = os.path.join(dir_path, fname)
        img = cv2.imread(path)
        if img is None:
            print(f"[WARN] Could not read {path}")
            continue
        detections = decode_qr(img)
        # Write annotated image
        annotated = draw_boxes(img, detections)
        cv2.imwrite(os.path.join(out_dir, f"annotated_{fname}"), annotated)

        ts = time.time()
        if detections:
            # record all
            for txt, _ in detections:
                rows.append(DetectionRow(source=fname, frame=0, text=txt, timestamp=ts))
        else:
            rows.append(DetectionRow(source=fname, frame=0, text="", timestamp=ts))

        # Optional scoring
        if truth is not None:
            expected = truth.get(fname)
            found_texts = {t for t, _ in detections}
            if expected is None:
                not_found_truth.append(fname)
            else:
                per_file_ok.append((fname, expected in found_texts))

    out_csv = os.path.join(out_dir, "detections.csv")
    write_csv(rows, out_csv)

    if truth is not None:
        total = len([f for f in files if f in truth])
        correct = sum(ok for _, ok in per_file_ok)
        print("\n=== Batch Scoring ===")
        print(f"Labeled images: {total}")
        print(f"Correct matches: {correct}")
        acc = (correct / total) if total else 0.0
        print(f"Accuracy: {acc:.3f}")
        if not_found_truth:
            print(f"[INFO] {len(not_found_truth)} image(s) missing labels in CSV:")
            for f in not_found_truth[:10]:
                print(f"  - {f}")
            if len(not_found_truth) > 10:
                print("  (… truncated)")

        # Save a simple report
        with open(os.path.join(out_dir, "report.txt"), "w", encoding="utf-8") as rf:
            rf.write("=== QR Batch Test Report ===\n")
            rf.write(f"Labeled images: {total}\n")
            rf.write(f"Correct matches: {correct}\n")
            rf.write(f"Accuracy: {acc:.3f}\n")
            if not_found_truth:
                rf.write("\nImages missing labels:\n")
                for f in not_found_truth:
                    rf.write(f"  - {f}\n")

    print(f"\nOutputs written to: {os.path.abspath(out_dir)}")
    print(f"- Detections: {os.path.abspath(out_csv)}")
    print("- Annotated images prefixed with 'annotated_'")

# --------- Webcam mode ---------

def run_webcam(device: int, out_dir: str, cooldown_s: float = 2.0) -> None:
    ensure_dir(out_dir)
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        print(f"[ERROR] Could not open webcam index {device}")
        sys.exit(1)

    rows: List[DetectionRow] = []
    last_seen = defaultdict(float)  # text -> last timestamp
    frame_idx = 0
    print("Press 'q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[WARN] Failed to read frame.")
            break

        detections = decode_qr(frame)
        now = time.time()
        # De-duplicate by cooldown window
        for txt, _ in detections:
            if now - last_seen[txt] >= cooldown_s:
                rows.append(DetectionRow(source="webcam", frame=frame_idx, text=txt, timestamp=now))
                last_seen[txt] = now
                print(f"[DETECTED] {txt}")

        # Show annotated
        vis = draw_boxes(frame, detections)
        cv2.imshow("QR Scanner (press 'q' to quit)", vis)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()
    out_csv = os.path.join(out_dir, "detections.csv")
    write_csv(rows, out_csv)
    print(f"Detections saved to: {os.path.abspath(out_csv)}")

# --------- Main ---------

def parse_args():
    p = argparse.ArgumentParser(description="QR code testing harness")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--webcam", action="store_true", help="Use webcam to scan live")
    mode.add_argument("--dir", type=str, help="Directory of images to batch scan")
    p.add_argument("--device", type=int, default=0, help="Webcam index (default 0)")
    p.add_argument("--labels", type=str, help="Optional labels CSV for scoring (dir mode)")
    p.add_argument("--out", type=str, default="qr_out", help="Output directory")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.webcam:
        run_webcam(args.device, args.out)
    else:
        run_dir(args.dir, args.out, args.labels)
