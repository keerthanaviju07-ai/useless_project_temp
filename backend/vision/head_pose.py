import cv2
import numpy as np


class HeadPoseEstimator:

    def __init__(self, frame_width=640, frame_height=480):

        self.frame_width = frame_width
        self.frame_height = frame_height

        # Approximate 3D facial model points
        self.model_points = np.array([
            (0.0, 0.0, 0.0),          # Nose
            (0.0, -330.0, -65.0),      # Chin
            (-225.0, 170.0, -135.0),   # Left eye
            (225.0, 170.0, -135.0),    # Right eye
            (-150.0, -150.0, -125.0),  # Left mouth
            (150.0, -150.0, -125.0)    # Right mouth
        ], dtype=np.float64)

        # Camera parameters
        focal_length = frame_width

        self.camera_matrix = np.array([
            [focal_length, 0, frame_width / 2],
            [0, focal_length, frame_height / 2],
            [0, 0, 1]
        ], dtype=np.float64)

        self.dist_coeffs = np.zeros((4, 1))

    def estimate(self, landmarks):

        # MediaPipe landmark indices
        landmark_ids = [
            1,    # Nose
            152,  # Chin
            33,   # Left eye
            263,  # Right eye
            61,   # Left mouth
            291   # Right mouth
        ]

        image_points = []

        for landmark_id in landmark_ids:

            landmark = landmarks[landmark_id]

            x = landmark.x * self.frame_width
            y = landmark.y * self.frame_height

            image_points.append((x, y))

        image_points = np.array(
            image_points,
            dtype=np.float64
        )

        # Solve head orientation
        success, rotation_vector, _ = cv2.solvePnP(
            self.model_points,
            image_points,
            self.camera_matrix,
            self.dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return None

        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(
            rotation_vector
        )

        # Extract Euler angles
        angles = cv2.RQDecomp3x3(
            rotation_matrix
        )

        pitch = angles[0][0]
        yaw = angles[0][1]
        roll = angles[0][2]

        # Normalize angles
        if pitch > 90:
            pitch -= 180
        elif pitch < -90:
            pitch += 180

        if yaw > 90:
            yaw -= 180
        elif yaw < -90:
            yaw += 180

        if roll > 90:
            roll -= 180
        elif roll < -90:
            roll += 180

        return {
            "yaw": float(yaw),
            "pitch": float(pitch),
            "roll": float(roll)
        }