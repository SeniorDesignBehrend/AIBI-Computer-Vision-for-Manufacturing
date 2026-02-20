import pickle
from typing import List

from .models import ActionStep


def serialize_process(steps: List[ActionStep]) -> bytes:
    data = []
    for step in steps:
        data.append({
            "name": step.name,
            "order": step.order,
            "centroid": step.centroid,
        })
    return pickle.dumps(data)


def deserialize_process(data: bytes) -> list[ActionStep]:
    loaded_data = pickle.loads(data)
    steps: list[ActionStep] = []
    for item in loaded_data:
        step = ActionStep(name=item["name"], order=item["order"])
        step.centroid = item["centroid"]
        steps.append(step)
    return steps
