from test.BaseTest import BaseTest

from src.gui.VideoStreamer import VideoStreamer

class VideoStreamerTest(BaseTest):

    def setUp(self):
        self.server = VideoStreamer(None)
        #self.server.run(host="0.0.0.0", threaded=True)

    def test_init(self):
        self.assertIsInstance(self.server, VideoStreamer, "Server should be a videostream server")