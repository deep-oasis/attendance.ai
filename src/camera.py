import picamera
from PIL import Image
import numpy as np


class Camera:
    def __init__(self, resolution=(320, 240)):
        ''' Handles camera facillities
            resolution: image final resolution
        '''
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.np_output = np.zeros((resolution[1], resolution[0], 3),dtype=np.uint8)
        

    def get_frame(self, format='rgb'):
        ''' Get frame from raspberry-pi's camera
            format: capturing fornat

            returns a numpy array
        '''
        self.camera.capture(self.np_output, format='rgb')
        return self.np_output
    