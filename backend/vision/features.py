import numpy as np


class FeatureExtractor:

    def extract(self, sequence):
        """
        Extract numerical features from a head-movement sequence.

        Parameters
        ----------
        sequence : list of dict
            Each item should contain:
            {
                "yaw": float,
                "pitch": float,
                "roll": float
            }

        Returns
        -------
        dict
            Extracted features for ML training/prediction.
        """

        if not sequence:
            raise ValueError("Sequence is empty")

        yaw = np.array(
            [sample["yaw"] for sample in sequence],
            dtype=np.float64
        )

        pitch = np.array(
            [sample["pitch"] for sample in sequence],
            dtype=np.float64
        )

        roll = np.array(
            [sample["roll"] for sample in sequence],
            dtype=np.float64
        )

        features = {

            # -------------------------
            # YAW
            # -------------------------

            "yaw_mean": float(np.mean(yaw)),
            "yaw_std": float(np.std(yaw)),
            "yaw_min": float(np.min(yaw)),
            "yaw_max": float(np.max(yaw)),
            "yaw_range": float(np.ptp(yaw)),

            # -------------------------
            # PITCH
            # -------------------------

            "pitch_mean": float(np.mean(pitch)),
            "pitch_std": float(np.std(pitch)),
            "pitch_min": float(np.min(pitch)),
            "pitch_max": float(np.max(pitch)),
            "pitch_range": float(np.ptp(pitch)),

            # -------------------------
            # ROLL
            # -------------------------

            "roll_mean": float(np.mean(roll)),
            "roll_std": float(np.std(roll)),
            "roll_min": float(np.min(roll)),
            "roll_max": float(np.max(roll)),
            "roll_range": float(np.ptp(roll)),
        }

        return features