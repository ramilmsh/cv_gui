import io
import sys

from src.processors.DummyProcessor import *
from src.processors.Processor import Processor
from matplotlib import pyplot as plt

processor = Processor([
    # (resize, {'height': 4}),
    no_action,
    (print_contours, {'channel': 'seg'}),
    # (save, {'filename': 'test8.png'})
])  # type: Processor

processor.execute(cv2.imread('src/processors/images/6_1.png'))

if sys.stdin.readline():
    print("done")
