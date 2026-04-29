"""Directional sorting for detected Data Matrix codes."""

import numpy as np
from typing import List, Tuple, Optional


class ScanSorter:
    """Sorts detected Data Matrix codes by scan direction using row-based grouping."""

    @staticmethod
    def centroid(box) -> Tuple[Optional[float], Optional[float]]:
        """Compute the centroid of a detection polygon."""
        try:
            pts = np.array(box, dtype=float)
            cx = pts[:, 0].mean()
            cy = pts[:, 1].mean()
            return cx, cy
        except Exception:
            return None, None

    @staticmethod
    def sort(detections: list, scan_direction: str) -> list:
        """Sort detections by scan_direction using row-based grouping.

        Each detection is a (text, box) tuple. Returns the sorted list.
        If scan_direction is 'any' or None, returns detections unchanged.
        """
        if not scan_direction or scan_direction == 'any' or len(detections) < 2:
            return detections

        try:
            centroids = [ScanSorter.centroid(box) for _, box in detections]

            # Compute row threshold from vertical gaps
            valid_cys = [cy for _, cy in centroids if cy is not None]
            if len(valid_cys) >= 2:
                sorted_cys = sorted(valid_cys)
                gaps = np.diff(np.array(sorted_cys))
                median_gap = float(np.median(gaps)) if gaps.size else 0.0
                row_thresh = max(10.0, median_gap * 0.75)
            else:
                row_thresh = 10.0

            # Build items with position and assign row indices
            items = []
            for (det, (cx, cy)) in zip(detections, centroids):
                items.append({'item': det, 'cx': cx, 'cy': cy, 'row': None})

            items.sort(key=lambda x: float('inf') if x['cy'] is None else x['cy'])

            current_row = 0
            prev_cy = None
            for entry in items:
                cy = entry['cy']
                if cy is None:
                    entry['row'] = 9999
                    continue
                if prev_cy is None:
                    entry['row'] = current_row
                    prev_cy = cy
                    continue
                if abs(cy - prev_cy) > row_thresh:
                    current_row += 1
                entry['row'] = current_row
                prev_cy = cy

            # Sort within rows according to direction
            def _sort_key(e):
                cx = e['cx'] if e['cx'] is not None else float('inf')
                row = e['row']
                if scan_direction in ('row-major', 'left-to-right-down'):
                    return (row, cx)
                if scan_direction == 'right-to-left-down':
                    return (row, -cx)
                if scan_direction in ('column-major', 'top-to-bottom-left-to-right'):
                    return (cx, row)
                if scan_direction == 'left-to-right':
                    return (0, cx)
                if scan_direction == 'right-to-left':
                    return (0, -cx)
                if scan_direction == 'top-to-bottom':
                    return (row, 0)
                if scan_direction == 'bottom-to-top':
                    return (-row, 0)
                return (row, cx)

            items.sort(key=_sort_key)
            return [e['item'] for e in items]
        except Exception:
            return detections
