import cv2
from cv2.typing import MatLike
from typing import Optional, Tuple
from pyglet.image import ImageData, Texture
import mediapipe as mp
from dataclasses import dataclass
import time

mp_hands = mp.solutions.hands

@dataclass
class CameraFrame:
    texture: Optional[Texture]
    finger_coordinates: Optional[Tuple[int, int]]

class Camera:
    def __init__(self, cap_width: int, cap_height: int):
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
        self.hands_detector = mp_hands.Hands(model_complexity=0, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
    def finger_coordinates(self, frame: MatLike) -> Optional[Tuple[int, int]]:
        # detect hand landmarks
        results = self.hands_detector.process(frame)
        if results.multi_hand_landmarks:
            # get the first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]
            # get the index finger tip
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            # convert the normalized coordinates to pixel coordinates
            x = int(index_finger_tip.x * self.cap_width)
            y = int(index_finger_tip.y * self.cap_height)
            return x, y
        return None
    
    def capture(self) -> CameraFrame:
        if not self.cap.isOpened():
            raise Exception("Camera is not opened")
        # capture frame
        _, frame_bgr = self.cap.read()
        # check if frame is None
        if frame_bgr is None:
            return CameraFrame(None, None)
        # convert to RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        # flip the image vertically
        frame_rgb = cv2.flip(frame_rgb, 0)
        # detect hand landmarks
        finger_coordinates = self.finger_coordinates(frame_rgb)
        # convert to bytes
        frame_data = frame_rgb.tobytes()
        # create image data with pitch
        # pitch = width * channels
        pitch = self.cap_width * 3
        image_data = ImageData(self.cap_width, self.cap_height, "RGB", frame_data, pitch=pitch)
        # create texture
        texture = image_data.get_texture()
        return CameraFrame(texture, finger_coordinates)
    
    def release(self):
        self.cap.release()
