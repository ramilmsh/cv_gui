#from src.gui.VideoStreamer import VideoStreamer
#from src.camera.Camera import Camera
#from threading import Thread

from src.camera.PubSub import PubSub
pubsub = PubSub()

def _print(msg):
    print(msg)

pubsub.subscribe('message', _print)
pubsub.publish('message', 'dfsf')
#server = VideoStreamer(Camera(0, pubsub), pubsub)
#server.run(host="0.0.0.0", threaded=True)

#thread = Thread(target=server.run, kwargs={"host": "0.0.0.0", "threaded": True})
#thread.start()