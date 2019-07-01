from src.processors.DummyProcessor import *
from src.processors.Processor import Processor

processor = Processor([
    (resize, {'height': 720}),
    (seg_pencil, {})
])  # type: Processor

processor.execute(cv2.imread('test3.jpg'))
