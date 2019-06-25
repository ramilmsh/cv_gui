from threading import Thread

from src.gui.Server import Server
from src.camera.Camera import Camera
from src.processors.DummyProcessor import *
from src.processors.Processor import Processor
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject

Camera()

processor = Processor([
    (no_action, {}),
    (in_range, {'channel': 'image'})
]).subscribe('stream')


server = Server()
server.run(host="0.0.0.0", threaded=True)
