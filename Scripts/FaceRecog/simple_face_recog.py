#!/usr/bin/env python3
"""
simple_face_recog.py
Tiny face recognition demo with two modes:

1) Webcam:
   python simple_face_recog.py --known_dir known_faces --webcam

2) Single image:
   python simple_face_recog.py --known_dir known_faces --image test.jpg

Tips:
- Place one clear image per person in --known_dir (e.g., Alice.jpg).
- Use --tolerance 0.5 (stricter) to 0.6 (looser). Default 0.5.
- For speed on CPU, keep --model hog. For accuracy (needs GPU/CUDA or patience), try --model cnn.
"""

import argparse, os, glob, time
import numpy as np
import cv2
import face_recognition

def load_known_faces(known_dir, model="hog"):
    names, encs = [], []
    if not os.path.isdir(known_dir):
        raise FileNotFoundError(f"Known dir not found: {known_dir}")

    img_paths = []
    for pat in ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"):
        img_paths.extend(glob.glob(os.path.join(known_dir, pat)))
    if not img_paths:
        print(f"[WARN] No images found in {known_dir}")

    for p in img_paths:
        img = face_recognition.load_image_file(p)
        # detect once; assume a single main face per known image
        locs = face_recognition.face_locations(img, model=model)
        encs_list = face_recognition.face_encodings(img, locs)
        if not encs_list:
            print(f"[WARN] No face found in {os.path.basename(p)} — skipping.")
            continue
        names.append(os.path.splitext(os.path.basename(p))[0])
        encs.append(encs_list[0])

    if not names:
        print("[WARN] No valid known faces loaded.")
    return names, np.array(encs) if encs else np.empty((0,128))

def recognize_in_frame(frame_bgr, known_names, known_encs, tolerance=0.5, model="hog"):
    # Speed trick: downscale for detection/encoding
    scale = 0.25
    small = cv2.resize(frame_bgr, (0,0), fx=scale, fy=scale)
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    # Detect + encode
    locs = face_recognition.face_locations(rgb_small, model=model)
    encs = face_recognition.face_encodings(rgb_small, locs)

    results = []  # [(top, right, bottom, left, name)]
    for enc, (top, right, bottom, left) in zip(encs, locs):
        name = "Unknown"
        if len(known_encs) > 0:
            distances = face_recognition.face_distance(known_encs, enc)
            best_idx = np.argmin(distances)
            if distances[best_idx] <= tolerance:
                name = known_names[best_idx]

        # Upscale coords back to original frame
        top, right, bottom, left = int(top/scale), int(right/scale), int(bottom/scale), int(left/scale)
        results.append((top, right, bottom, left, name))
    return results

def draw_labels(frame, results):
    for (top, right, bottom, left, name) in results:
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.rectangle(frame, (left, bottom-25), (right, bottom), (0,255,0), cv2.FILLED)
        cv2.putText(frame, name, (left+6, bottom-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2, cv2.LINE_AA)
    return frame

def run_webcam(known_names, known_encs, tolerance, model, device=0):
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open webcam index {device}")
    print("Press 'q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("[WARN] Failed to read frame.")
            break
        results = recognize_in_frame(frame, known_names, known_encs, tolerance, model)
        frame = draw_labels(frame, results)
        cv2.imshow("Face Recognition (q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_image(known_names, known_encs, tolerance, model, image_path, out_path=None):
    frame = cv2.imread(image_path)
    if frame is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    results = recognize_in_frame(frame, known_names, known_encs, tolerance, model)
    frame = draw_labels(frame, results)

    if out_path:
        cv2.imwrite(out_path, frame)
        print(f"Saved labeled image to: {os.path.abspath(out_path)}")
    else:
        cv2.imshow("Face Recognition (press any key)", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--known_dir", required=True, help="Folder of known faces (one image per person)")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--webcam", action="store_true", help="Use live webcam")
    mode.add_argument("--image", type=str, help="Path to an image to label")
    ap.add_argument("--out", type=str, help="Output image path for --image mode")
    ap.add_argument("--tolerance", type=float, default=0.5, help="Lower is stricter (0.5 default)")
    ap.add_argument("--model", type=str, default="hog", choices=["hog","cnn"], help="Face detector backend")
    ap.add_argument("--device", type=int, default=0, help="Webcam index")
    args = ap.parse_args()

    known_names, known_encs = load_known_faces(args.known_dir, model=args.model)
    if args.webcam:
        run_webcam(known_names, known_encs, args.tolerance, args.model, device=args.device)
    else:
        run_image(known_names, known_encs, args.tolerance, args.model, args.image, args.out)

if __name__ == "__main__":
    main()
