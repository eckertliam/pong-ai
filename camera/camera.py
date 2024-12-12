import cv2
from cv2.typing import MatLike
from pyglet.image import ImageData, Texture

class Camera:
    def __init__(self, cap_width: int, cap_height: int, display_width: int, display_height: int):
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.display_width = display_width
        self.display_height = display_height
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)
    
    def capture(self) -> Texture:
        if not self.cap.isOpened():
            raise Exception("Camera is not opened")
        # capture frame
        _, frame_bgr = self.cap.read()
        # convert to RGB and then to bytes
        frame_data = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB).tobytes()
        # create image data with pitch
        # pitch = width * channels
        pitch = self.cap_width * 3
        image_data = ImageData(self.cap_width, self.cap_height, "RGB", frame_data, pitch=pitch)
        # create texture
        texture = image_data.get_texture()
        return texture
    
    def release(self):
        self.cap.release()
