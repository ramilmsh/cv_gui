import time
from threading import Lock, Event, Thread

import cv2

from src.camera.Frame import Frame
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject


class Streamer:
    IMAGE_HEIGHT = 360
    TIMEOUT = 3.

    @inject
    def __init__(self, channel: str = "stream", pubsub: PubSub = None):
        self.channel = channel
        self.pubsub = pubsub

        self._subscriber = None  # type: Event
        self.frame_data = b''  # type: bytes
        self.frame_lock = Lock()
        self.running = 0  # type: int
        self.last_published = -1  # type: float

        self.timeout_thread = Thread(target=self._check_timeout)
        self.timeout = False

    def run(self):
        self.running += 1
        if self.running > 1:
            return
        self._subscriber = self.pubsub.subscribe(self.channel, self._receive_frame)
        self.timeout_thread.start()

    def stop(self):
        self.running -= 1
        self.frame_lock.release()
        self.last_published = -2
        if self.running == 0:
            self.pubsub.unsubscribe(self._subscriber)

    def generator(self):
        self.run()
        self.frame_lock.acquire()
        while True:
            self.frame_lock.acquire()
            if self.timeout:
                break
            try:
                frame = Frame.from_bytes(self.frame_data) \
                    .resize(height=Streamer.IMAGE_HEIGHT)
                yield self._encode(frame)
            except Exception as e:
                print(e)

    def _check_timeout(self):
        while True:
            if self.last_published == -1:
                pass
            elif time.time() - self.last_published > Streamer.TIMEOUT:
                self.timeout = True
                break
            time.sleep(Streamer.TIMEOUT)
        self.stop()

    @classmethod
    def _encode(cls, frame) -> bytes:
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' \
               + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes() \
               + b'\r\n'

    def _receive_frame(self, frame_data):
        self.last_published = time.time()
        self.frame_data = frame_data
        try:
            self.frame_lock.release()
        except RuntimeError:
            pass
