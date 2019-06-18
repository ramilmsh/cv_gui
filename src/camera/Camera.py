import cv2
import datetime

from src.camera.BaseCamera import BaseCamera


class Camera(BaseCamera):


    def __init__(self, source, name:str='DefaultCamera'):
        super().__init__(name=name)
        self.capture = cv2.VideoCapture(source)
    
    def read(self):
        ret, frame = self.capture.read()
        print(ret)
        return frame

    def check(self):
        ret, = self.capture.read()
        return ret
    