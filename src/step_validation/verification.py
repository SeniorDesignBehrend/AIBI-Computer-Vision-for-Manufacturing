import time
from typing import List, Tuple

import numpy as np

from .models import ActionStep
from .state import VerificationState


def calculate_similarity(embedding: np.ndarray, steps: List[ActionStep], threshold: float) -> Tuple[int, float]:
    best_match_idx = -1
    best_similarity = -1.0

    for i, step in enumerate(steps):
        if step.centroid is None:
            continue
        similarity = float(np.dot(embedding, step.centroid))
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_idx = i

    if best_similarity < threshold:
        return -1, best_similarity
    return best_match_idx, best_similarity


def get_verification_state(
    detected_idx: int,
    current_idx: int,
    num_steps: int,
    timed_window: list[tuple[float, int]],
    window_duration: float,
    required_fraction: float,
) -> VerificationState:
    if current_idx >= num_steps:
        return VerificationState.COMPLETE

    if detected_idx == -1:
        return VerificationState.IDLE

    if detected_idx > current_idx:
        return VerificationState.SKIPPED

    if detected_idx < current_idx:
        return VerificationState.WRONG_ORDER

    cutoff = time.monotonic() - window_duration
    recent = [idx for ts, idx in timed_window if ts >= cutoff]
    if not recent:
        return VerificationState.CORRECT_STEP
    fraction = sum(1 for idx in recent if idx == current_idx) / len(recent)
    if fraction >= required_fraction:
        return VerificationState.CONFIRMED
    return VerificationState.CORRECT_STEP
