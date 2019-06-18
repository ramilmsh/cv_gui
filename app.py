from src.gui.VideoStreamer import VideoStreamer
from src.camera.Camera import Camera
from threading import Thread

print("fsfs")
server = VideoStreamer(Camera(0))

#thread = Thread(target=server.run, kwargs={"host": "0.0.0.0", "threaded": True})