from subprocess import Popen, PIPE
import signal

import cv2

from src.processors.DummyProcessor import *
from src.processors.Processor import Processor

# server = Popen(['python3', 'app.py'], stdout=PIPE)

# try:
#     server.wait()
# except KeyboardInterrupt:
#     print('\nStopping Server...')
#     server.send_signal(signal.SIGKILL)
from src.utils.PubSub import PubSub

processor = Processor([
    (no_action, {}),
    (in_range, {'channel': 'image'})
])

pubsub.subscribe('stream', processor.execute, False)

