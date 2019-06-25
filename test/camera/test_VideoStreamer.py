from test.BaseTest import BaseTest

from src.gui.Server import Server


class VideoStreamerTest(BaseTest):

    def setUp(self):
        self.server = Server()
        #self.server.run(host="0.0.0.0", threaded=True)

    def test_init(self):
        self.assertIsInstance(self.server, Server, "Server should be a videostream server")