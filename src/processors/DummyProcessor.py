import cv2
import numpy as np

B = np.array([.0, 4.408490765224997, 3.144532188123648])
C = np.array([255., 257.2748941071508, 256.00960321263835])
D = (C - B) / np.linalg.norm(C - B)


def get_dist2(a, b, c):
    return 255 - 50 * int(np.linalg.norm([abs(a - b), abs(b - c), abs(a - c)]))


def get_dist(a, b, c):
    A = np.array([a, b, c])
    v = A - B
    t = v.dot(D)
    P = B + t * D
    return 255 if np.linalg.norm(P - A) > 10 else 0


def no_action(img):
    return img


def in_range(img, channel: str = 'image'):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(img, np.array([0, 0, 100]), np.array([360, 50, 100]))


def resize(img: np.ndarray, height: float = 360):
    h = height
    w = int(height / img.shape[0] * img.shape[1])
    return cv2.resize(img, (w, h))


def gray_scale(img, channel: str = 'image'):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def seg_pencil(img, channel: str = 'seg'):
    img = cv2.inRange(img, np.array([0, 0, 0]), np.array([110, 110, 110]))
    kernel = np.ones((3, 3), np.uint8)
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 10)
    # img = cv2.dilate(img, kernel, iterations=1)
    kernel[1][1] = 3
    # img = cv2.erode(img, kernel, iterations=1)
    kernel = np.array([[1, 1, 1, 1, 1],
                       [1, 2, 2, 2, 1],
                       [1, 2, 1, 2, 1],
                       [1, 2, 2, 2, 1],
                       [1, 1, 1, 1, 1]])
    # img = cv2.dilate(img, kernel, iterations=1)
    # img = cv2.erode(img, kernel, iterations=1)

    img = cv2.Laplacian(img, cv2.CV_64F)
    # img = cv2.filter2D(img, -1, kernel)
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img


def contour(img):
    return cv2.findContours()


def seg_pencil_stupid(img, channel: str = 'seg'):
    _temp = np.reshape(img, (img.shape[0] * img.shape[1], 3))
    v_get_dist = np.vectorize(get_dist2)
    _img = v_get_dist(_temp[:, 0], _temp[:, 1], _temp[:, 2])
    _img = np.reshape(_img, (img.shape[0], img.shape[1]))

    return _img.astype(np.uint8)
