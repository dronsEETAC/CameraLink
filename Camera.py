import threading
import time

import cv2 as cv

class Camera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.videoStreaming = False

    def TakePicture (self):
        '''for n in range(1, 50):
            # this loop is required to discard first frames'''
        ret, frame = self.cap.read()
        return ret, frame

    def _start_video_stream (self, frequency, callback, params):
        period = 1 / frequency

        while self.videoStreaming:
            # Read Frame
            ret, frame = self.cap.read()
            if ret:
                callback (frame, params)
                time.sleep(period)


    def StartVideoStream (self, frequency, callback, params):
        self.videoStreaming = True
        streamingThread = threading.Thread(
            target=self._start_video_stream,
            args=[frequency, callback, params])
        streamingThread.start()


    def StopVideoStream (self):
        self.videoStreaming = False

    def Close (self):
        self.cap.release()
