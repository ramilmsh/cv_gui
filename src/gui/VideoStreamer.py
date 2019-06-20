from flask import Flask, render_template, Response
from redis import StrictRedis

import cv2
import numpy as np
import os

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame


class VideoStreamer(Flask):
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    IMAGE_HEIGHT = 480


    def __init__(self, camera: BaseCamera):
        super().__init__("GUI", template_folder=VideoStreamer.DIRECTORY+"/templates",
                         static_folder=VideoStreamer.DIRECTORY+"/static")

        self.redis = StrictRedis()

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/stream', view_func=self.stream)

    def index(self):
        return render_template('index.html', context={"title": "Title"})

    def stream(self):
        return Response(self._generate_message(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def _generate_message(self):
        while True:
            frame = Frame.from_bytes(self.redis.get("DefaultCamera"))
            frame.resize(height=VideoStreamer.IMAGE_HEIGHT)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes() + b'\r\n')
