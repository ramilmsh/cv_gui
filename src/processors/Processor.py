import time
from threading import Lock, Thread
from typing import Tuple, List, Callable, Dict

import numpy as np

from src.camera.Frame import Frame
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject


class Processor:
    """
    A convenience class that provides functionality to chain CV operations and stream results
    """

    FRAME_DELAY = .1  # type: float

    @inject
    def __init__(self, processors: [List[Tuple[Callable[[np.ndarray, ...], np.ndarray], dict]],
                                    List[Callable[[np.ndarray, ...], np.ndarray]]], pubsub: PubSub = None):
        """
        Initialize Processor

        :param processors: a list of middleware or tuple of [middleware, dictionary of parameters]
        :param PubSub pubsub: injected pubsub
        """

        self.pubsub = pubsub  # type: PubSub
        self.processors = []  # type: List[Tuple[Callable[[np.ndarray, ...], np.ndarray], dict]]
        self._add_processors(processors)

        self.image_cache = {}  # type: Dict[str, np.ndarray]
        self.image_lock = Lock()  # type: Lock
        self.processed = True  # type: bool

        # Publishing thread that dies as soon as processing is done
        self.publish_thread = Thread(target=self._publish_loop, daemon=True)
        self.publish_thread.start()

    def execute(self, data: [np.ndarray, Frame, bytes]) -> np.ndarray:
        """
        Execute the chain of processing logic on a piece of data

        :param [np.ndarray, Frame, bytes] data: an image for processing
        :return: processed image
        """

        image = Processor.data_to_bgr(data)  # type: np.ndarray

        for processor in self.processors:
            image = processor[0](image, **processor[1])
            if 'channel' in processor[1]:
                with self.image_lock:
                    self.image_cache[processor[1]['channel']] = image

        self.processed = True
        return image

    @staticmethod
    def data_to_bgr(data: [np.ndarray, Frame, bytes]) -> np.ndarray:
        """
        Convert an image into a numpy array

        :param [np.ndarray, Frame, bytes] data: image
        :return:
        """
        img = data
        if type(data) is Frame:
            img = data.to_cv2_bgr()
        elif type(data) is bytes:
            img = Frame.from_bytes(data).to_cv2_bgr()

        return img.copy()

    def _add_processors(self, processors: [Tuple[callable, dict], callable]):
        """
        Add processors in a uniform format to the chain

        :param processors: a list of middleware or tuple of [middleware, dictionary of parameters]
        :return:
        """
        for element in processors:
            if type(element) == tuple:
                processor, params = element
            else:
                processor = element
                params = {}

            self.processors.append((processor, params))

    def _publish(self, channel: str, image: np.ndarray):
        """
        Publish a frame to PubSub

        :param str channel: channel name
        :param np.ndarray image: image array
        :return:
        """
        self.pubsub.publish(channel, Frame.from_cv2_bgr(image).to_bytes())

    def subscribe(self, channel: str):
        """
        Dynamically process data from a PubSub channel

        :param str channel: channel name
        :return:
        """
        self.pubsub.subscribe(channel, self._receive_data)

    def _receive_data(self, data: bytes):
        """
        Convert image data to a numpy array

        :param bytes data: image data
        :return:
        """
        self.img = Frame.from_bytes(data).to_cv2_bgr()
        if self.processed:
            self.processed = False
            self.execute(self.img)

    def _publish_loop(self):
        """
        Periodically publish last processed frame

        :return:
        """
        while True:
            with self.image_lock:
                for channel in self.image_cache:
                    self._publish(channel, self.image_cache[channel])

            time.sleep(Processor.FRAME_DELAY)
