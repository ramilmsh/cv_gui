import io
import sys

from src.processors.DummyProcessor import *
from src.processors.Processor import Processor
from matplotlib import pyplot as plt

processor = Processor([
    # (resize, {'height': 4}),
    (edges, {'channel': 'seg'}),
    (save, {'filename': 'src/processors/images/test_1.png'}),
    # erode_dilate
])  # type: Processor

processor.execute(cv2.imread('src/processors/images/test_1.jpg'))

if sys.stdin.readline():
    print("done")
