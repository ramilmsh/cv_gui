"""
Author: Austin McKee
"""

import struct
import cv2
import numpy as np
import time
import math
from PIL import Image


class Frame:
    """
    8-bit RGB numpy array.
    height * width * 3 channels * uint8
    """

    def __init__(self, array: np.array, size, time_captured=None):
        """
        :param array:
        :param size: tuple(width, height)
        """
        if time_captured is None:
            time_captured = time.time()

        if array.flags['C_CONTIGUOUS']:
            self._array = np.array(array, dtype=np.uint8)
        else:
            self._array = np.ascontiguousarray(array, dtype=np.uint8)

        self._width, self._height = size
        self._channel_num = array.shape[2] if len(array.shape) > 2 else 1
        self._cap_time = time_captured

    def resize(self, height=-1, width=-1, scale=-1):
        if height != -1:
            scale = height / self._height
        if width != -1:
            scale = width / self._width
        self._array = cv2.resize(self._array, (math.floor(self._width * scale),
                                               math.floor(self._height * scale)),
                                 interpolation=cv2.INTER_CUBIC)

        return self

    def cvtColor(self, flag):
        self._array = cv2.cvtColor(self._array, flag)
        self._height, self._width = self._array.shape
        self._channel_num = self._array.shape[2] if len(self._array.shape) > 2 else 1
        return self

    def to_pillow(self):
        return Image.fromarray(self._array, mode='RGB')

    def to_bytes(self):
        metadata = struct.pack('<IIId', self._width, self._height, self._channel_num, self._cap_time)
        arr = np.insert(self._array.ravel(), 0, np.frombuffer(
            metadata, dtype=np.uint8), 0)
        return bytes(arr)

    def to_np_array(self):
        return self._array

    def to_cv2_bgr(self):
        return cv2.cvtColor(self._array, cv2.COLOR_RGB2BGR)

    def copy(self) -> 'Frame':
        return Frame(self._array.copy(), (self._width, self._height), self._cap_time)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    @classmethod
    def from_np_array(cls, np_array, time_captured=None) -> 'Frame':
        assert len(np_array.shape) == 3
        return cls(np_array, (np_array.shape[1], np_array.shape[0]), time_captured)

    @classmethod
    def from_cv2_bgr(cls, open_cv_img, time_captured=None) -> 'Frame':
        return cls(cv2.cvtColor(open_cv_img, cv2.COLOR_BGR2RGB),
                   (open_cv_img.shape[1], open_cv_img.shape[0]), time_captured)

    @classmethod
    def from_pillow(cls, image: Image, time_captured=None) -> 'Frame':
        if image.mode != 'RGB':
            image = image.convert('RGB')
        arr = np.array(image).reshape(
            (image.height, image.width, 3)).astype(np.uint8)
        return cls(arr, image.size, time_captured)

    @classmethod
    def from_bytes(cls, data, time_captured=None) -> 'Frame':
        width, height, channel_num, cap_time = struct.unpack_from('<IIId', data, 0)
        arr = np.frombuffer(data, dtype=np.uint8, offset=20)
        arr = arr.reshape((height, width, channel_num))
        return cls(arr, (width, height), time_captured)
