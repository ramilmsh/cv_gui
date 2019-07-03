from src.processors.DummyProcessor import *
from src.processors.Processor import Processor

processor = Processor([
    (resize, {'height': 4}),
    (in_range, {'channel': 'seg'}),
    # (save, {'filename': 'test8.png'})
])  # type: Processor

processor.execute(cv2.imread('src/processors/images/test7.png'))
