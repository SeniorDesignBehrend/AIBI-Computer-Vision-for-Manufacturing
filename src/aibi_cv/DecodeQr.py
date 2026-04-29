import numpy as np
from pylibdmtx.pylibdmtx import decode as dmtx_decode
import cv2 as cv


class DecodeQr:
    @staticmethod
    def multi_datamatrix(img):
        """Decode Data Matrix codes using pylibdmtx."""
        results = []
        try:
            decoded = dmtx_decode(img, timeout=200, max_count=5)
            if not decoded:
                return results
            for d in decoded:
                try:
                    text = d.data.decode('utf-8') if isinstance(d.data, (bytes, bytearray)) else str(d.data)
                except Exception:
                    text = str(d.data)

                pts = None
                if hasattr(d, 'rect'):
                    try:
                        r = d.rect
                        pts = np.array([
                            [r.left, r.top],
                            [r.left + r.width, r.top],
                            [r.left + r.width, r.top + r.height],
                            [r.left, r.top + r.height]
                        ], dtype=int)
                    except Exception:
                        pts = None

                results.append((text, pts))
        except Exception:
            return []
        return results