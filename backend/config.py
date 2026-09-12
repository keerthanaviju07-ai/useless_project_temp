from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Model
FACE_LANDMARKER_MODEL = BASE_DIR / "models" / "face_landmarker.task"

# Dataset
RAW_DATA_DIR = BASE_DIR / "backend" / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "backend" / "data" / "processed"

# ML model
ML_MODEL_PATH = BASE_DIR / "backend" / "ml" / "model.pkl"

# Camera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Calibration
CALIBRATION_SECONDS = 3

# Gesture recording
RECORDING_SECONDS = 2.5

# Supported gestures
GESTURES = {
    "a": "ATHE",
    "s": "SHERI",
    "v": "VENDA",
    "n": "NOKKAM",
    "i": "ARIYILLA"
}