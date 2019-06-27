from threading import Thread

from src.gui.Server import Server
from src.camera.Camera import Camera
from src.processors.DummyProcessor import *
from src.processors.Processor import Processor

# Camera()

processor = Processor([
    (resize, {'height': 1080}),
    (seg_pencil, {})
])


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.destroyWindow('img')
        exit(0)


cv2.imshow('img', processor.execute(cv2.imread('test3.jpg')))
cv2.setMouseCallback('img', mouse_callback)
cv2.waitKey(0)

# server = Server()
# server.run(host="0.0.0.0", threaded=True)
