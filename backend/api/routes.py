import time
from collections import deque, Counter

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from config import (
    FACE_LANDMARKER_MODEL,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    CALIBRATION_SECONDS,
    ML_MODEL_PATH
)

from vision.face_tracker import FaceTracker
from vision.head_pose import HeadPoseEstimator
from vision.calibration import CalibrationManager
from ml.predict import GesturePredictor


router = APIRouter()


# ============================================================
# SETTINGS
# ============================================================

SEQUENCE_LENGTH = 30
CONFIDENCE_THRESHOLD = 0.55
PREDICTION_HISTORY_SIZE = 3
MIN_STABLE_PREDICTIONS = 2


# ============================================================
# BASIC ROUTES
# ============================================================

@router.get("/")
def home():
    return {
        "message": "Thalayattam API is running",
        "status": "success"
    }


@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@router.get("/gestures")
def get_gestures():
    return {
        "gestures": {
            "ATHE": "Athe",
            "SHERI": "Sheri",
            "VENDA": "Venda",
            "NOKKAM": "Nokkam",
            "ARIYILLA": "Ariyilla"
        }
    }


# ============================================================
# LIVE AI WEBSOCKET
# ============================================================

@router.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):

    await websocket.accept()

    print()
    print("======================================")
    print("   FRONTEND CONNECTED TO AI")
    print("======================================")

    face_tracker = None

    try:

        # ====================================================
        # INITIALIZE AI
        # ====================================================

        face_tracker = FaceTracker(
            FACE_LANDMARKER_MODEL
        )

        head_pose = HeadPoseEstimator(
            FRAME_WIDTH,
            FRAME_HEIGHT
        )

        calibration = CalibrationManager(
            CALIBRATION_SECONDS
        )

        predictor = GesturePredictor(
            ML_MODEL_PATH
        )

        # ====================================================
        # BUFFERS
        # ====================================================

        sequence = deque(
            maxlen=SEQUENCE_LENGTH
        )

        prediction_history = deque(
            maxlen=PREDICTION_HISTORY_SIZE
        )

        # ====================================================
        # INITIAL STATE
        # ====================================================

        calibration.start()

        calibration_start_time = time.time()

        stable_gesture = "WAITING"
        stable_confidence = 0.0

        last_timestamp_ms = 0

        # ====================================================
        # INITIAL MESSAGE
        # ====================================================

        await websocket.send_json({
            "type": "status",
            "status": "calibrating",
            "message": "Keep your head straight"
        })

        # ====================================================
        # MAIN LOOP
        # ====================================================

        while True:

            data = await websocket.receive_bytes()

            # =================================================
            # JPEG → IMAGE
            # =================================================

            np_array = np.frombuffer(
                data,
                dtype=np.uint8
            )

            frame = cv2.imdecode(
                np_array,
                cv2.IMREAD_COLOR
            )

            if frame is None:

                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid camera frame"
                })

                continue

            # =================================================
            # RESIZE
            # =================================================

            frame = cv2.resize(
                frame,
                (
                    FRAME_WIDTH,
                    FRAME_HEIGHT
                )
            )

            # =================================================
            # RGB
            # =================================================

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # =================================================
            # TIMESTAMP
            # =================================================

            timestamp_ms = int(
                time.time() * 1000
            )

            if timestamp_ms <= last_timestamp_ms:

                timestamp_ms = (
                    last_timestamp_ms + 1
                )

            last_timestamp_ms = timestamp_ms

            # =================================================
            # FACE DETECTION
            # =================================================

            landmarks = face_tracker.detect(
                rgb_frame,
                timestamp_ms
            )

            # =================================================
            # NO FACE
            # =================================================

            if landmarks is None:

                sequence.clear()
                prediction_history.clear()

                stable_gesture = "WAITING"
                stable_confidence = 0.0

                await websocket.send_json({

                    "type": "prediction",

                    "gesture": "WAITING",

                    "confidence": 0.0,

                    "confidence_percent": 0.0,

                    "calibrated":
                        calibration.is_calibrated,

                    "face_detected": False,

                    "frames": 0,

                    "sequence_length":
                        SEQUENCE_LENGTH

                })

                continue

            # =================================================
            # HEAD POSE
            # =================================================

            pose = head_pose.estimate(
                landmarks
            )

            if pose is None:
                continue

            # =================================================
            # CALIBRATION
            # =================================================

            if not calibration.is_calibrated:

                calibration.add_sample(
                    pose
                )

                elapsed = (
                    time.time()
                    - calibration_start_time
                )

                remaining = (
                    CALIBRATION_SECONDS
                    - elapsed
                )

                if remaining < 0:
                    remaining = 0

                # ---------------------------------------------
                # CALIBRATING
                # ---------------------------------------------

                if elapsed < CALIBRATION_SECONDS:

                    await websocket.send_json({

                        "type": "calibration",

                        "status": "calibrating",

                        "remaining": round(
                            remaining,
                            1
                        ),

                        "calibrated": False

                    })

                    continue

                # ---------------------------------------------
                # FINISH
                # ---------------------------------------------

                success = calibration.finish()

                if success:

                    sequence.clear()
                    prediction_history.clear()

                    stable_gesture = "WAITING"
                    stable_confidence = 0.0

                    print(
                        "✅ Calibration complete"
                    )

                    await websocket.send_json({

                        "type": "status",

                        "status": "calibrated",

                        "message":
                            "Calibration complete"

                    })

                continue

            # =================================================
            # RELATIVE POSE
            # =================================================

            relative_pose = (
                calibration.get_relative_pose(
                    pose
                )
            )

            if relative_pose is None:
                continue

            # =================================================
            # ADD FRAME
            # =================================================

            sequence.append(
                relative_pose
            )

            current_gesture = (
                stable_gesture
            )

            current_confidence = (
                stable_confidence
            )

            # =================================================
            # PREDICTION
            # =================================================

            if len(sequence) >= SEQUENCE_LENGTH:

                result = predictor.predict(
                    list(sequence)
                )

                predicted_gesture = (
                    result["gesture"]
                )

                predicted_confidence = (
                    result["confidence"]
                )

                # ---------------------------------------------
                # CONFIDENCE
                # ---------------------------------------------

                if (
                    predicted_confidence
                    >= CONFIDENCE_THRESHOLD
                ):

                    prediction_history.append(
                        predicted_gesture
                    )

                    # -----------------------------------------
                    # STABILITY
                    # -----------------------------------------

                    if (
                        len(prediction_history)
                        >= MIN_STABLE_PREDICTIONS
                    ):

                        counts = Counter(
                            prediction_history
                        )

                        best_gesture, best_count = (
                            counts.most_common(1)[0]
                        )

                        if (
                            best_count
                            >= MIN_STABLE_PREDICTIONS
                        ):

                            stable_gesture = (
                                best_gesture
                            )

                            stable_confidence = (
                                predicted_confidence
                            )

                            current_gesture = (
                                stable_gesture
                            )

                            current_confidence = (
                                stable_confidence
                            )

                # ---------------------------------------------
                # SLIDING WINDOW
                # ---------------------------------------------

                for _ in range(
                    SEQUENCE_LENGTH // 2
                ):

                    if sequence:
                        sequence.popleft()

            # =================================================
            # SEND RESULT
            # =================================================

            await websocket.send_json({

                "type": "prediction",

                "gesture": str(
                    current_gesture
                ),

                "confidence": round(
                    float(current_confidence),
                    4
                ),

                "confidence_percent": round(
                    float(current_confidence) * 100,
                    1
                ),

                "calibrated": True,

                "face_detected": True,

                "frames": len(sequence),

                "sequence_length":
                    SEQUENCE_LENGTH,

                "pose": {

                    "yaw": round(
                        float(
                            relative_pose["yaw"]
                        ),
                        2
                    ),

                    "pitch": round(
                        float(
                            relative_pose["pitch"]
                        ),
                        2
                    ),

                    "roll": round(
                        float(
                            relative_pose["roll"]
                        ),
                        2
                    )

                }

            })

    # ========================================================
    # DISCONNECTED
    # ========================================================

    except WebSocketDisconnect:

        print(
            "🔌 Frontend disconnected"
        )

    # ========================================================
    # ERROR
    # ========================================================

    except Exception as e:

        print(
            f"❌ WebSocket error: {e}"
        )

        try:

            await websocket.send_json({

                "type": "error",

                "message": str(e)

            })

        except Exception:
            pass

    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

        if face_tracker is not None:
            face_tracker.close()

        print(
            "🧹 AI resources released"
        )