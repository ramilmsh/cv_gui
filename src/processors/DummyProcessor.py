import cv2
import numpy as np
from scipy.ndimage import convolve
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

B = np.array([.0, 4.408490765224997, 3.144532188123648])
C = np.array([255., 257.2748941071508, 256.00960321263835])
D = (C - B) / np.linalg.norm(C - B)


def get_dist2(a, b, c):
    return 255 - 50 * int(np.linalg.norm([abs(a - b), abs(b - c), abs(a - c)]))


def get_dist(a, b, c):
    """
    Distance between a line and a point in 3d space
    :param a: x-coordinate
    :param b: y-coordinate
    :param c: z-coordinate
    :return: Distance between a line defined by B and C and point A
    """
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


def convolution(img):
    kernel = np.array([[1, 4, 7, 4, 1],
                       [4, 16, 26, 16, 4],
                       [7, 26, 41, 26, 7],
                       [4, 16, 26, 16, 4],
                       [1, 4, 7, 4, 1]])
    img = img.astype(np.float64)
    img = convolve(img, kernel / 273)
    img += abs(np.min(img))
    img *= 255. / np.max(img)
    img = img.astype(np.uint8)
    img = cv2.Laplacian(img, cv2.CV_64F)

    img[img > 0] = 0
    print(np.min(img), np.max(img))
    img = -img
    return img


def seg_pencil(img, channel: str = 'seg'):
    _img = img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.medianBlur(img, 5)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 10)
    return img


def erode_dilate(img):
    kernel = np.ones((3, 3), np.uint8)
    # img = cv2.dilate(img, kernel, iterations=1)
    kernel[1][1] = 3
    # img = cv2.erode(img, kernel, iterations=1)

    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # img = cv2.Laplacian(img, cv2.CV_64F)
    # img = cv2.filter2D(img, -1, kernel)
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img


def print_lines(img):
    img = cv2.Canny(img, 1000, 1100)
    lines = cv2.HoughLines(img, 1, np.pi / 180, 200)
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img


def print_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)  # max contour
    f = open('path.svg', 'w+')
    f.write(
        '<svg width="' + str(img.shape[0]) + '" height="' + str(img.shape[1]) + '" xmlns="http://www.w3.org/2000/svg">')
    for c in cnt:
        f.write('<path d="M')

        for i in range(len(c)):
            print(i)
            x, y = c[i][0]
            f.write(str(x) + ' ' + str(y) + ' ')

        f.write('"/>')
    f.write('</svg>')
    f.close()
    return img


def contour(img):
    return cv2.findContours()


def seg_pencil_stupid(img, channel: str = 'seg'):
    _temp = np.reshape(img, (img.shape[0] * img.shape[1], 3))
    v_get_dist = np.vectorize(get_dist2)
    _img = v_get_dist(_temp[:, 0], _temp[:, 1], _temp[:, 2])
    _img = np.reshape(_img, (img.shape[0], img.shape[1]))

    return _img.astype(np.uint8)
