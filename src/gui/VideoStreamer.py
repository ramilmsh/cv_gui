from flask import Flask, render_template, Response
from threading import Lock

import cv2
import os

from src.utils.injection.decorator import inject
from src.utils.PubSub import PubSub

from src.camera.Frame import Frame


class VideoStreamer(Flask):
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    IMAGE_HEIGHT = 360

    @inject
    def __init__(self, pubsub: PubSub = None):
        super().__init__("GUI", template_folder=VideoStreamer.DIRECTORY+"/templates",
                         static_folder=VideoStreamer.DIRECTORY+"/static")

        self.pubsub = pubsub

        self.frame_data = None
        self.frame_lock = Lock()

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/stream', view_func=self.stream)
        self.add_url_rule('/stream/<channel>', view_func=self.stream)

    def index(self):
        return render_template('index.html', context={"title": "Title"})

    def stream(self, channel: str = 'DefaultCamera'):
        _id = self.pubsub.subscribe(channel, self._receive_data)
        response = Response(self._generate_message(), mimetype='multipart/x-mixed-replace; boundary=frame')
        response.call_on_close(lambda: self.pubsub.unsubscribe("DefaultCamera", _id))
        return response

    def _generate_message(self):
        try:
            self.frame_lock.acquire()
            while True:
                self.frame_lock.acquire()
                try:
                    frame = Frame.from_bytes(self.frame_data)
                    frame.resize(height=VideoStreamer.IMAGE_HEIGHT)
                    yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'\
                        + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes()\
                        + b'\r\n'
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

    def _receive_data(self, data):
        self.frame_data = data
        try:
            self.frame_lock.release()
        except RuntimeError:
            pass
