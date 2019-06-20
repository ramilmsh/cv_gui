import cv2
import datetime
from redis import Redis
from threading import Thread
import time

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame

class Camera(BaseCamera):


    def __init__(self, source, pubsub, name: str = 'DefaultCamera'):
        super().__init__(name=name)
        self.capture = cv2.VideoCapture(source)
        self.pubsub = pubsub

        self.thread = Thread(target=self._post_data, daemon=True)
        self.thread.start()

    def read(self):
        ret, frame = self.capture.read()
        frame = Frame.from_cv2_bgr(frame)
        return frame.to_bytes()

    def check(self):
        ret, = self.capture.read()
        return ret

    def _post_data(self):
        while True:
            self.pubsub.publish(self.name, self.read())
            time.sleep(.02)
