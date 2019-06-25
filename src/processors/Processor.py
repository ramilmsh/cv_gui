import time
from typing import List, Dict, Tuple

import numpy as np

from src.camera.Frame import Frame
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject


class Processor:

    @inject
    def __init__(self, processors: List[Tuple[callable, dict]], pubsub: PubSub = None):
        self.processors = processors
        self.pubsub = pubsub
        self.img = None
        self.processed = True

    def execute(self, img) -> np.ndarray:
        if type(img) is Frame:
            img = img.to_cv2_bgr()
        elif type(img) is bytes:
            img = Frame.from_bytes(img).to_cv2_bgr()

        for _tuple in self.processors:
            processor, params = _tuple
            img = processor(img, **params)
            if 'channel' in params:
                self.publish(params['channel'], img)

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


