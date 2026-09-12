import numpy as np


class CalibrationManager:

    def __init__(self, duration_seconds=3):

        self.duration_seconds = duration_seconds

        self.samples = []

        self.is_calibrated = False

        self.neutral_yaw = 0.0
        self.neutral_pitch = 0.0
        self.neutral_roll = 0.0

    def start(self):

        """Start a new calibration session."""

        self.samples = []
        self.is_calibrated = False

    def add_sample(self, pose):

        """Add one head-pose sample."""

        if pose is None:
            return

        self.samples.append([
            pose["yaw"],
            pose["pitch"],
            pose["roll"]
        ])

    def finish(self):

        """Calculate the neutral head position."""

        if not self.samples:
            return False

        samples = np.array(
            self.samples,
            dtype=np.float64
        )

        self.neutral_yaw = float(
            np.mean(samples[:, 0])
        )

        self.neutral_pitch = float(
            np.mean(samples[:, 1])
        )

        self.neutral_roll = float(
            np.mean(samples[:, 2])
        )

        self.is_calibrated = True

        return True

    def get_relative_pose(self, pose):

        """Return pose relative to calibrated neutral position."""

        if pose is None:
            return None

        if not self.is_calibrated:
            return None

        return {
            "yaw": pose["yaw"] - self.neutral_yaw,
            "pitch": pose["pitch"] - self.neutral_pitch,
            "roll": pose["roll"] - self.neutral_roll
        }

    def reset(self):

        """Reset calibration."""

        self.samples = []

        self.is_calibrated = False

        self.neutral_yaw = 0.0
        self.neutral_pitch = 0.0
        self.neutral_roll = 0.0