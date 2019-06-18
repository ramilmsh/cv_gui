from src.gui.VideoStreamer import VideoStreamer

self.server = VideoStreamer(None)
self.server.run(host="0.0.0.0", threaded=True)