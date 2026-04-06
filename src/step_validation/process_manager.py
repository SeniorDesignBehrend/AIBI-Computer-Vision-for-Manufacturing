from collections import defaultdict

import numpy as np

from .models import ActionStep


class ProcessManager:
    def __init__(self):
        self.steps = []
        self.current_op_step = 0
        self.training_finalized = False
        self.run_log = []
        self.recorded_segments = []
        self.training_phase = "record"

    def add_step(self, name: str) -> None:
        new_order = len(self.steps)
        self.steps.append(ActionStep(name=name, order=new_order))
        self.training_finalized = False

    def get_steps(self):
        return self.steps

    def clear_steps(self) -> None:
        self.steps = []
        self.current_op_step = 0
        self.training_finalized = False
        self.run_log = []

    def clear_training_state(self) -> None:
        self.recorded_segments = []
        self.training_phase = "record"
        self.training_finalized = False

    def finalize_training(self) -> None:
        for step in self.steps:
            if step.centroids:
                mean_emb = np.mean(step.centroids, axis=0)
                norm = np.linalg.norm(mean_emb)
                step.centroid = mean_emb / norm if norm > 0 else mean_emb
        self.training_finalized = True

    def finalize_training_from_segments(self, segments: list) -> None:
        from .embeddings import get_embedding

        label_to_frames: dict[str, list] = defaultdict(list)
        label_order: list[str] = []
        for seg in segments:
            if seg["label"] and seg["frames"]:
                if seg["label"] not in label_order:
                    label_order.append(seg["label"])
                label_to_frames[seg["label"]].extend(seg["frames"])

        steps = []
        for idx, label in enumerate(label_order):
            embeddings = [get_embedding(f) for f in label_to_frames[label]]
            mean_emb = np.mean(embeddings, axis=0)
            norm = np.linalg.norm(mean_emb)
            step = ActionStep(name=label, order=idx)
            step.centroid = mean_emb / norm if norm > 0 else mean_emb
            steps.append(step)

        self.steps = steps
        self.training_finalized = True
        self.recorded_segments = []
        self.training_phase = "record"

    def augment_steps_from_segments(self, segments: list) -> int:
        """Add new video segments to existing steps and re-compute centroids.

        Segments whose label matches an existing step name are merged in.
        Returns the number of steps that were augmented.
        """
        from .embeddings import get_embedding

        step_by_name: dict[str, ActionStep] = {s.name: s for s in self.steps}

        augmented = 0
        for seg in segments:
            label = seg.get("label", "").strip()
            frames = seg.get("frames", [])
            if not label or not frames or label not in step_by_name:
                continue

            step = step_by_name[label]
            new_embeddings = [get_embedding(f) for f in frames]

            # Combine existing centroid with new embeddings
            all_embeddings = list(new_embeddings)
            if step.centroid is not None:
                all_embeddings.append(step.centroid)

            mean_emb = np.mean(all_embeddings, axis=0)
            norm = np.linalg.norm(mean_emb)
            step.centroid = mean_emb / norm if norm > 0 else mean_emb
            augmented += 1

        self.recorded_segments = []
        return augmented
