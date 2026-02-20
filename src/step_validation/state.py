from enum import Enum, auto


class VerificationState(Enum):
    IDLE = auto()
    CORRECT_STEP = auto()
    CONFIRMED = auto()
    WRONG_ORDER = auto()
    SKIPPED = auto()
    COMPLETE = auto()
