from src.gui.VideoStreamer import VideoStreamer

server = VideoStreamer(None)
server.run(host="0.0.0.0", threaded=True)