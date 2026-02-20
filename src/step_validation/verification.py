from collections import deque
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


def get_verification_state(detected_idx: int, current_idx: int, num_steps: int,
                           window: deque, required_votes: int) -> VerificationState:
    if current_idx >= num_steps:
        return VerificationState.COMPLETE

    if detected_idx == -1:
        return VerificationState.IDLE

    if detected_idx > current_idx:
        return VerificationState.SKIPPED

    if detected_idx < current_idx:
        return VerificationState.WRONG_ORDER

    votes = sum(1 for v in window if v == current_idx)
    if votes >= required_votes:
        return VerificationState.CONFIRMED
    return VerificationState.CORRECT_STEP
