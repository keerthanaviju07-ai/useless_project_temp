import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceTracker:

    def __init__(self, model_path):

        base_options = python.BaseOptions(
            model_asset_path=str(model_path)
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_faces=1,
            min_face_detection_confidence=0.5,
            min_face_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.landmarker = (
            vision.FaceLandmarker
            .create_from_options(options)
        )

    def detect(self, frame_rgb, timestamp_ms):

        """
        Detect facial landmarks from an RGB frame.

        Parameters:
            frame_rgb: RGB image as a NumPy array
            timestamp_ms: Increasing timestamp in milliseconds

        Returns:
            Facial landmarks for the first detected face,
            or None if no face is detected.
        """

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame_rgb
        )

        results = self.landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        if not results.face_landmarks:
            return None

        return results.face_landmarks[0]

    def close(self):

        self.landmarker.close()