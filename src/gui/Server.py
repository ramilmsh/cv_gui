from typing import Dict

from flask import Flask, render_template, Response, request
import os

from src.gui.Streamer import Streamer
from src.utils.injection.decorator import inject


class Server(Flask):
    """
    A generic flask server with MJPEG streaming functionality
    """
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))

    @inject
    def __init__(self):
        super().__init__("GUI", template_folder=Server.DIRECTORY + "/templates",
                         static_folder=Server.DIRECTORY + "/static")

        self.streamers = {}  # type: Dict[str, Streamer]

        self.add_url_rule('/', view_func=self.index)
        self.add_url_rule('/stream', view_func=self.stream)
        self.add_url_rule('/stream/<channel>', view_func=self.stream)
        self.add_url_rule('/stop', view_func=self.stop)
        self.add_url_rule('/ping', view_func=self.ping)

    def index(self):
        return render_template('index.html', context={"title": "Title"})

    def stream(self, channel: str = 'stream'):
        if channel in self.streamers:
            del self.streamers[channel]
        self.streamers[channel] = Streamer(channel)

        response = Response(self.streamers[channel].generator(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        response.call_on_close(lambda: self.streamers[channel].stop())
        return response

    def stop(self):
        shutdown_func = request.environ.get('werkzeug.server.shutdown')
        return Response(self._shutdown_server(shutdown_func))

    def ping(self):
        return "pong"

    def _shutdown_server(self, shutdown: callable):
        yield "Shutting down..."
        if shutdown is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown()
