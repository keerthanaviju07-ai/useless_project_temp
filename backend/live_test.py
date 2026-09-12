import cv2
import time
from collections import deque, Counter

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


# ============================================================
# SETTINGS
# ============================================================

# 30 frames ≈ 1 second at 30 FPS
SEQUENCE_LENGTH = 30

# Minimum confidence required
CONFIDENCE_THRESHOLD = 0.55

# Number of recent predictions
PREDICTION_HISTORY_SIZE = 3

# Number of matching predictions required
MIN_STABLE_PREDICTIONS = 2


# ============================================================
# MAIN
# ============================================================

def main():

    print("======================================")
    print("       THALAYATTAM LIVE AI")
    print("======================================")
    print("Starting camera...")
    print("Look straight at the camera for calibration.")
    print("Press Q or ESC to exit.")
    print()

    # ========================================================
    # CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("❌ Could not open camera")
        return

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        FRAME_WIDTH
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        FRAME_HEIGHT
    )

    # ========================================================
    # INITIALIZE MODULES
    # ========================================================

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

    # ========================================================
    # MOVEMENT BUFFER
    # ========================================================

    sequence = deque(
        maxlen=SEQUENCE_LENGTH
    )

    # ========================================================
    # PREDICTION HISTORY
    # ========================================================

    prediction_history = deque(
        maxlen=PREDICTION_HISTORY_SIZE
    )

    # ========================================================
    # PREDICTION VARIABLES
    # ========================================================

    stable_gesture = "WAITING"
    stable_confidence = 0.0

    # ========================================================
    # CALIBRATION
    # ========================================================

    calibration.start()

    calibration_start_time = time.time()

    last_timestamp_ms = 0

    # ========================================================
    # MAIN LOOP
    # ========================================================

    try:

        while True:

            # =================================================
            # READ CAMERA
            # =================================================

            ret, frame = cap.read()

            if not ret:

                print("❌ Could not read camera")
                break

            frame = cv2.resize(
                frame,
                (FRAME_WIDTH, FRAME_HEIGHT)
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
            # BGR → RGB
            # =================================================

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # =================================================
            # FACE TRACKING
            # =================================================

            landmarks = face_tracker.detect(
                rgb_frame,
                timestamp_ms
            )

            # =================================================
            # NO FACE
            # =================================================

            if landmarks is None:

                cv2.putText(
                    frame,
                    "NO FACE DETECTED",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

                sequence.clear()

                prediction_history.clear()

                stable_gesture = "WAITING"
                stable_confidence = 0.0

            else:

                # =================================================
                # HEAD POSE
                # =================================================

                pose = head_pose.estimate(
                    landmarks
                )

                if pose is not None:

                    # =============================================
                    # CALIBRATION
                    # =============================================

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

                        # -----------------------------------------
                        # CALIBRATION TEXT
                        # -----------------------------------------

                        cv2.putText(
                            frame,
                            "KEEP YOUR HEAD STRAIGHT",
                            (100, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 255),
                            2
                        )

                        cv2.putText(
                            frame,
                            f"Calibrating: {remaining:.1f}s",
                            (180, 90),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 255),
                            2
                        )

                        # -----------------------------------------
                        # FINISH CALIBRATION
                        # -----------------------------------------

                        if elapsed >= CALIBRATION_SECONDS:

                            success = calibration.finish()

                            if success:

                                print()
                                print(
                                    "======================================"
                                )

                                print(
                                    "       CALIBRATION COMPLETE"
                                )

                                print(
                                    "======================================"
                                )

                                print(
                                    f"Neutral Yaw: "
                                    f"{calibration.neutral_yaw:.2f}°"
                                )

                                print(
                                    f"Neutral Pitch: "
                                    f"{calibration.neutral_pitch:.2f}°"
                                )

                                print(
                                    f"Neutral Roll: "
                                    f"{calibration.neutral_roll:.2f}°"
                                )

                                print()

                                sequence.clear()
                                prediction_history.clear()

                    # =============================================
                    # AFTER CALIBRATION
                    # =============================================

                    else:

                        relative_pose = (
                            calibration.get_relative_pose(
                                pose
                            )
                        )

                        if relative_pose is not None:

                            # =====================================
                            # ADD CURRENT MOVEMENT
                            # =====================================

                            sequence.append(
                                relative_pose
                            )

                            # =====================================
                            # DISPLAY STATUS
                            # =====================================

                            cv2.putText(
                                frame,
                                "CALIBRATED",
                                (20, 35),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 0),
                                2
                            )

                            # =====================================
                            # DISPLAY YAW
                            # =====================================

                            cv2.putText(
                                frame,
                                f"Yaw: "
                                f"{relative_pose['yaw']:.1f}",
                                (20, 70),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (255, 255, 255),
                                2
                            )

                            # =====================================
                            # DISPLAY PITCH
                            # =====================================

                            cv2.putText(
                                frame,
                                f"Pitch: "
                                f"{relative_pose['pitch']:.1f}",
                                (20, 100),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (255, 255, 255),
                                2
                            )

                            # =====================================
                            # DISPLAY ROLL
                            # =====================================

                            cv2.putText(
                                frame,
                                f"Roll: "
                                f"{relative_pose['roll']:.1f}",
                                (20, 130),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (255, 255, 255),
                                2
                            )

                            # =====================================
                            # PREDICTION
                            # =====================================

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

                                # =================================
                                # CONFIDENCE FILTER
                                # =================================

                                if (
                                    predicted_confidence
                                    >= CONFIDENCE_THRESHOLD
                                ):

                                    prediction_history.append(
                                        predicted_gesture
                                    )

                                    # =============================
                                    # STABILITY CHECK
                                    # =============================

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

                                        # =========================
                                        # ACCEPT GESTURE
                                        # =========================

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

                                # =================================
                                # REMOVE OLDEST HALF
                                # =================================
                                #
                                # Instead of clearing all 30
                                # frames, keep the newest half.
                                # This makes prediction feel
                                # more continuous.
                                # =================================

                                for _ in range(
                                    SEQUENCE_LENGTH // 2
                                ):

                                    if sequence:

                                        sequence.popleft()

            # =================================================
            # DISPLAY PREDICTION
            # =================================================

            if calibration.is_calibrated:

                if stable_gesture != "WAITING":

                    cv2.putText(
                        frame,
                        f"GESTURE: {stable_gesture}",
                        (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 0),
                        2
                    )

                    cv2.putText(
                        frame,
                        f"CONFIDENCE: "
                        f"{stable_confidence * 100:.1f}%",
                        (20, 240),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

                else:

                    cv2.putText(
                        frame,
                        "ANALYZING...",
                        (20, 200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

            # =================================================
            # BUFFER STATUS
            # =================================================

            if calibration.is_calibrated:

                cv2.putText(
                    frame,
                    f"Frames: "
                    f"{len(sequence)}/{SEQUENCE_LENGTH}",
                    (20, 280),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            # =================================================
            # DISPLAY CAMERA
            # =================================================

            cv2.imshow(
                "Thalayattam - Live AI",
                frame
            )

            # =================================================
            # EXIT
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:

                break

    finally:

        # =====================================================
        # CLEANUP
        # =====================================================

        cap.release()

        face_tracker.close()

        cv2.destroyAllWindows()

        print()
        print("✅ Thalayattam Live AI closed")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()