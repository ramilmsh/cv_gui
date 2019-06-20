#from src.gui.VideoStreamer import VideoStreamer
#from src.camera.Camera import Camera
from threading import Thread
import time
from src.camera.PubSub import PubSub
pubsub = PubSub()


def _print(msg):
    print(msg)


def _publish():
    while True:
        pubsub.publish('message', 'dfsf')
        time.sleep(1)


_id = pubsub.subscribe('message', _print)
thread = Thread(target=_publish, daemon=False)

thread.start()

time.sleep(3)
pubsub.unsubscribe('message', _id)
time.sleep(3)
_id = pubsub.subscribe('message', _print)

#server = VideoStreamer(Camera(0, pubsub), pubsub)
#server.run(host="0.0.0.0", threaded=True)

#thread = Thread(target=server.run, kwargs={"host": "0.0.0.0", "threaded": True})
# thread.start()
