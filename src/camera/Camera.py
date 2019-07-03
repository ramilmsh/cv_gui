import time

import cv2
from threading import Thread

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame
from src.utils.injection.decorator import inject
from src.utils.PubSub import PubSub


class Camera(BaseCamera):
    FRAME_DELAY = .1  # type: float

    @inject
    def __init__(self, source: [int, str] = 0, name: str = 'stream', pubsub: PubSub = None, daemon=False):
        super().__init__(name=name)
        self.capture = cv2.VideoCapture(source)  # type: cv2.VideoCapture
        self.pubsub = pubsub  # type: PubSub

        self.thread = Thread(target=self._post_data, daemon=daemon)  # type: Thread

    def run(self):
        self.thread.start()

    def read(self) -> bytes:
        ret, frame = self.capture.read()
        return Frame.from_cv2_bgr(frame).to_bytes()

    def check(self):
        ret, = self.capture.read()
        return ret

    def _post_data(self):
        while True:
            self.pubsub.publish(self.name, self.read())
            time.sleep(Camera.FRAME_DELAY)
