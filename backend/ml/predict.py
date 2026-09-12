from pathlib import Path
import sys

# ============================================================
# PATH SETUP
# ============================================================

# Get the backend directory
BACKEND_DIR = Path(__file__).resolve().parents[1]

# Add backend to Python's import path
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# IMPORTS
# ============================================================

import joblib
import pandas as pd

from vision.features import FeatureExtractor


# ============================================================
# GESTURE PREDICTOR
# ============================================================

class GesturePredictor:

    def __init__(self, model_path):

        """
        Load the trained Random Forest model.

        Parameters
        ----------
        model_path : str or Path
            Location of model.pkl
        """

        self.model_path = Path(model_path)

        # ----------------------------------------------------
        # CHECK MODEL
        # ----------------------------------------------------

        if not self.model_path.exists():

            raise FileNotFoundError(
                f"ML model not found:\n"
                f"{self.model_path}"
            )

        # ----------------------------------------------------
        # LOAD MODEL PACKAGE
        # ----------------------------------------------------

        package = joblib.load(
            self.model_path
        )

        self.model = package["model"]

        self.feature_names = (
            package["feature_names"]
        )

        self.classes = (
            package["classes"]
        )

        # ----------------------------------------------------
        # FEATURE EXTRACTOR
        # ----------------------------------------------------

        self.feature_extractor = (
            FeatureExtractor()
        )

        print("✅ ML model loaded successfully")

        print(
            f"Classes: {list(self.classes)}"
        )


    # ========================================================
    # PREDICT
    # ========================================================

    def predict(self, sequence):

        """
        Predict the gesture from a head-movement sequence.

        Parameters
        ----------
        sequence : list of dict

            Example:

            [
                {
                    "yaw": 2.1,
                    "pitch": 5.3,
                    "roll": 0.4
                },
                ...
            ]

        Returns
        -------
        dict

            {
                "gesture": "ATHE",
                "confidence": 0.95
            }
        """

        # ----------------------------------------------------
        # VALIDATE INPUT
        # ----------------------------------------------------

        if sequence is None:

            raise ValueError(
                "Sequence cannot be None"
            )

        if len(sequence) == 0:

            raise ValueError(
                "Cannot predict from an empty sequence"
            )

        # ----------------------------------------------------
        # EXTRACT FEATURES
        # ----------------------------------------------------

        features = (
            self.feature_extractor.extract(
                sequence
            )
        )

        # ----------------------------------------------------
        # CREATE FEATURE VECTOR
        # ----------------------------------------------------

        feature_vector = pd.DataFrame(
            [
                [
                    features[name]
                    for name in self.feature_names
                ]
            ],
            columns=self.feature_names
        )

        # ----------------------------------------------------
        # PREDICT GESTURE
        # ----------------------------------------------------

        prediction = self.model.predict(
            feature_vector
        )[0]

        # ----------------------------------------------------
        # PREDICTION PROBABILITIES
        # ----------------------------------------------------

        probabilities = (
            self.model.predict_proba(
                feature_vector
            )[0]
        )

        # Highest probability
        confidence = float(
            max(probabilities)
        )

        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {
            "gesture": str(prediction),
            "confidence": confidence
        }


    # ========================================================
    # PREDICT WITH ALL PROBABILITIES
    # ========================================================

    def predict_with_probabilities(
        self,
        sequence
    ):

        """
        Return gesture prediction together
        with probabilities for all classes.
        """

        if not sequence:

            raise ValueError(
                "Sequence cannot be empty"
            )

        # Extract features
        features = (
            self.feature_extractor.extract(
                sequence
            )
        )

        # Feature vector
        feature_vector = pd.DataFrame(
            [
                [
                    features[name]
                    for name in self.feature_names
                ]
            ],
            columns=self.feature_names
        )

        # Probabilities
        probabilities = (
            self.model.predict_proba(
                feature_vector
            )[0]
        )

        # Find highest probability
        best_index = probabilities.argmax()

        gesture = self.classes[
            best_index
        ]

        confidence = float(
            probabilities[best_index]
        )

        # Create probability dictionary
        all_probabilities = {}

        for class_name, probability in zip(
            self.classes,
            probabilities
        ):

            all_probabilities[
                str(class_name)
            ] = float(probability)

        return {
            "gesture": str(gesture),
            "confidence": confidence,
            "probabilities": all_probabilities
        }