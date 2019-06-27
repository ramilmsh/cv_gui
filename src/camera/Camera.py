import time

import cv2
from threading import Thread

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame
from src.utils.injection.decorator import inject
from src.utils.PubSub import PubSub


class Camera(BaseCamera):

    @inject
    def __init__(self, source: [int, str] = 0, name: str = 'stream', pubsub: PubSub = None):
        super().__init__(name=name)
        self.capture = cv2.VideoCapture(source)
        self.pubsub = pubsub

        self.thread = Thread(target=self._post_data, daemon=True)
        self.thread.start()

    def read(self):
        ret, frame = self.capture.read()
        return Frame.from_cv2_bgr(frame).to_bytes()

    def check(self):
        ret, = self.capture.read()
        return ret

    def _post_data(self):
        while True:
            self.pubsub.publish(self.name, self.read())
            time.sleep(.2)
