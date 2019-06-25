from typing import Dict

from flask import Flask, render_template, Response
import os

from src.gui.Streamer import Streamer
from src.utils.injection.decorator import inject


class Server(Flask):
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    @inject
    def __init__(self):
        super().__init__("GUI", template_folder=Server.DIRECTORY + "/templates",
                         static_folder=Server.DIRECTORY + "/static")

        self.streamers = {}  # type: Dict[str, Streamer]

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/stream', view_func=self.stream)
        self.add_url_rule('/stream/<channel>', view_func=self.stream)

    def index(self):
        return render_template('index.html', context={"title": "Title"})

    def stream(self, channel: str = 'DefaultCamera'):
        # if channel not in self.config['active_channels']:
        #     return "Channel inactive"

        if channel not in self.streamers:
            self.streamers[channel] = Streamer(channel)

        response = Response(self.streamers[channel].generator(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        response.call_on_close(lambda: self.streamers[channel].stop())
        return response
