from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np


@dataclass
class ActionStep:
    name: str
    order: int
    centroids: List[np.ndarray] = field(default_factory=list)
    centroid: Optional[np.ndarray] = None
