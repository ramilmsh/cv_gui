import time
from threading import Lock, Thread
from typing import List, Dict, Tuple

import numpy as np

from src.camera.Frame import Frame
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject


class Processor:

    @inject
    def __init__(self, processors: [Tuple[callable, dict], callable], pubsub: PubSub = None):
        self.processors = processors
        self.pubsub = pubsub
        self.image_cache = {}
        self.image_lock = Lock()
        self.processed = True

        self.publish_thread = Thread(target=self._publish_loop, daemon=True)
        self.publish_thread.start()
        print("Processor initialized.")

    def execute(self, img) -> np.ndarray:
        if type(img) is Frame:
            img = img.to_cv2_bgr()
        elif type(img) is bytes:
            img = Frame.from_bytes(img).to_cv2_bgr()

        for element in self.processors:
            if type(element) == tuple:
                processor, params = element
            else:
                processor = element
                params = {}

            img = processor(img, **params)
            if 'channel' in params:
                with self.image_lock:
                    self.image_cache[params['channel']] = img

        self.processed = True
        return img

    def publish(self, channel: str, image: np.ndarray):
        self.pubsub.publish(channel, Frame.from_cv2_bgr(image).to_bytes())

    def subscribe(self, channel: str):
        self.pubsub.subscribe(channel, self._receive_data)

    def _receive_data(self, data):
        self.img = Frame.from_bytes(data).to_cv2_bgr()
        if self.processed:
            self.processed = False
            self.execute(self.img)

    def _publish_loop(self):
        while True:
            with self.image_lock:
                for channel in self.image_cache:
                    self.publish(channel, self.image_cache[channel])

            time.sleep(.2)


