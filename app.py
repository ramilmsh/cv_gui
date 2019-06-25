import cv2

from src.camera.Frame import Frame
from src.gui.Server import Server
from src.camera.Camera import Camera
from src.utils.PubSub import PubSub
from src.utils.injection.decorator import inject

Camera()


@inject
def stream(pubsub: PubSub = None):
    pubsub.subscribe('stream', read)


@inject
def read(data, pubsub: PubSub = None):
    pubsub.publish('bla', Frame.from_bytes(data).cvtColor(cv2.COLOR_RGB2GRAY).to_bytes())


stream()

server = Server()
server.run(host="0.0.0.0", threaded=True)
