from src.gui.Server import Server
from src.camera.Camera import Camera
from threading import Thread
import time
import inspect
from redis import StrictRedis

from src.utils.injection.decorator import inject
from src.utils.PubSub import PubSub

Camera(0)

server = Server()
server.run(host="0.0.0.0", threaded=True)

#thread = Thread(target=server.run, kwargs={"host": "0.0.0.0", "threaded": True})
# thread.start()
