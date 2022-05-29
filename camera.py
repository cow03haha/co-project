import cv2
import mss
import numpy

import threading
import time
from collections import deque

class Camera(object):
    thread = None
    frame = None
    last_access = 0
    first_time = 0

    def __init__(self):
        if Camera.thread is None:
            Camera.last_access = time.time()
            Camera.first_time = time.time()
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        '''Get the current frame.'''
        Camera.last_access = time.time()
        return Camera.frame

    @staticmethod
    def frames():
        '''Create a new frame every 0.01 seconds.'''
        monitor = {
            'top': 225,
            'left': 538,
            'width': 828,
            'height': 489
        }
        
        with mss.mss() as sct:
            while True:
                time.sleep(0.01)
                raw = sct.grab(monitor)
                # Use numpy and opencv to convert the data to JPEG.
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 55]
                img = cv2.imencode('.jpg', numpy.array(raw))[1].tobytes()
                yield(img)

    @classmethod
    def _thread(cls):
        '''As long as there is a connection and the thread is running, reassign the current frame.'''
        print('Starting camera thread.')

        frames_queue = deque()
        frames_iter = cls.frames()

        for frame in frames_iter:
            frames_queue.append(frame)
            # if time.time() - cls.first_time >= 2:
            Camera.frame = frames_queue.popleft()

            if time.time() - cls.last_access >= 10:
                frames_iter.close()
                print('Stopping camera thread due to inactivity.')
                break
        
        cls.thread = None
