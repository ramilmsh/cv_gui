import cv2
import numpy as np


def no_action(img):
    return img


def in_range(img, channel: str = 'image'):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(img, np.array([0, 0, 0]), np.array([100, 100, 100]))
