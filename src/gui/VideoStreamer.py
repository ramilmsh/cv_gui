from flask import Flask, render_template, Response
from redis import Redis

import cv2
import numpy as np
import os
import time

from src.camera.BaseCamera import BaseCamera
from src.camera.Frame import Frame


class VideoStreamer(Flask):
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    IMAGE_HEIGHT = 360

    def __init__(self, camera: BaseCamera):
        super().__init__("GUI", template_folder=VideoStreamer.DIRECTORY+"/templates",
                         static_folder=VideoStreamer.DIRECTORY+"/static")

        self.redis = Redis()

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/stream', view_func=self.stream)

    def index(self):
        return render_template('index.html', context={"title": "Title"})

    def stream(self):
        return Response(self._generate_message(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def _generate_message(self):
        redis_pubsub = self.redis.pubsub()
        redis_pubsub.subscribe("DefaultCamera")

        for message in redis_pubsub.listen():
            if message['type'] != 'message':
                continue
            try:
                frame = Frame.from_bytes(message['data'])
                frame.resize(height=VideoStreamer.IMAGE_HEIGHT)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpeg', frame.to_cv2_bgr())[1].tobytes() + b'\r\n')
            except Exception as e:
                pass
        
        print("WTF")
