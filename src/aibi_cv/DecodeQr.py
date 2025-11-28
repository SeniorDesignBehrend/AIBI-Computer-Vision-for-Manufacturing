import numpy as np
from pyzbar.pyzbar import decode as pyzbar_decode
import cv2 as cv


class DecodeQr:
    @staticmethod
    def multi_pyzbar(img):
        """Decode multiple barcodes using pyzbar and return list of (text, pts)."""
        results = []
        try:
            decoded = pyzbar_decode(img)
            if not decoded:
                return results
            for d in decoded:
                try:
                    text = d.data.decode('utf-8') if isinstance(d.data, (bytes, bytearray)) else str(d.data)
                except Exception:
                    text = str(d.data)

                pts = None
                if getattr(d, 'polygon', None):
                    try:
                        pts = np.array([[p.x, p.y] for p in d.polygon], dtype=int)
                    except Exception:
                        pts = None

                results.append((text, pts))
        except Exception:
            return []
        
        return results

    @staticmethod
    def multi_opencv(img):
        """Decode multiple QR codes using OpenCV's detectAndDecodeMulti."""
        results = []
        try:
            detector = cv.QRCodeDetector()
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
        except Exception:
            return []
        return results

    @staticmethod
    def single_opencv(img):
        """Decode a single QR code using OpenCV."""
        try:
            detector = cv.QRCodeDetector()
            text, pts, _ = detector.detectAndDecode(img)
            if text:
                try:
                    pts_arr = np.array(pts, dtype=int) if pts is not None else None
                except Exception:
                    pts_arr = None
                return [(text, pts_arr)]
        except Exception:
            return []
        