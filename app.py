from src.gui.VideoStreamer import VideoStreamer
from src.camera.Camera import Camera
from threading import Thread

server = VideoStreamer(Camera(0))
server.run(host="0.0.0.0", threaded=True)

# thread = Thread(target=server.run, kwargs={"host": "0.0.0.0", "threaded": True})
# thread.start()