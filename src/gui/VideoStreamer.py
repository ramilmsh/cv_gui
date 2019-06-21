import cv2
import numpy as np
import os
import time
from threading import Event, Lock

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame
from src.utils.injection.decorator import inject
from src.utils.PubSub import PubSub
from src.utils.OrderedHashSet import OrderedHashSet

from tornado import websocket, httpserver, ioloop, web


class VideoStreamer(websocket.WebSocketHandler):
    IMAGE_HEIGHT = 360

    @inject
    def initialize(self, pubsub: PubSub = None):
        self.pubsub = pubsub
        self.current_frame = None
        self.clients = {}
        self.clients_lock = Lock()
        self.image_lock = Lock()

    def open(self):
        self._id = self.pubsub.subscribe("DefaultCamera", self._process_frames)
        self.clients[self._id] = self

    def on_message(self, message):
        if self.current_frame is None:
            return cv2.imread('src/camera/skins_feature.jpg')

        self.write_message(self.current_frame)

    def on_close(self):
        self.pubsub.unsubscribe("DefaultCamera", self._id)
        with self.clients_lock:
            del self.clients[self._id]

    def _process_frames(self, data):
        frame = Frame.from_bytes(data)
        frame.resize(height=VideoStreamer.IMAGE_HEIGHT)
        data = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'\
            + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes()\
            + b'\r\n'
        self.current_frame = data
        self.image_lock.release()


class MainHandler(web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("templates/index.html", title="My title")


class GUIServer:

    @inject
    def __init__(self, pubsub: PubSub = None):
        self.pubsub = pubsub
        # self.cam_manager = CameraManager()

    def run(self) -> object:
        # self.cam_manager.run()

        routes = [('/stream', VideoStreamer), ('/', MainHandler)]
        application = web.Application(routes)

        http_server = httpserver.HTTPServer(application)
        http_server.listen(8888)
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            http_server.stop()
            ioloop.IOLoop.instance().stop()
