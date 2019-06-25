from threading import Lock

import cv2

from src.camera.Frame import Frame
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject


class Streamer:
    IMAGE_HEIGHT = 360

    @inject
    def __init__(self, channel: str = "stream", pubsub: PubSub = None):
        self.channel = channel
        self.pubsub = pubsub

        self._pubsub_id = -1  # type: int
        self.frame_data = b''  # type: bytes
        self.frame_lock = Lock()
        self.running = 0  # type: int

    def run(self):
        self.running += 1
        if self.running > 1:
            return
        self._pubsub_id = self.pubsub.subscribe(self.channel, self._receive_frame)

    def stop(self):
        self.running -= 1
        if self.running == 0:
            self.pubsub.unsubscribe(self.channel, self._pubsub_id)

    def generator(self):
        self.run()
        self.frame_lock.acquire()
        while True:
            self.frame_lock.acquire()
            try:
                frame = Frame.from_bytes(self.frame_data) \
                    .resize(height=Streamer.IMAGE_HEIGHT)
                yield self._encode(frame)
            except Exception as e:
                print(e)

    @classmethod
    def _encode(cls, frame) -> bytes:
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' \
               + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes() \
               + b'\r\n'

    def _receive_frame(self, frame_data):
        self.frame_data = frame_data
        try:
            self.frame_lock.release()
        except RuntimeError:
            pass
