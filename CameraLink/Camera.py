import threading
import time

import cv2 as cv

class Camera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.videoStreaming = False
        self.frequency = 0 # numero de frames por segundo en el video streaming

    def TakePicture (self):
        for n in range(1, 50):
            # en este bucle descarto las primeras fotos, que a veces salen en negro
            ret, frame = self.cap.read()
        return ret, frame

    def _start_video_stream (self, callback, params):
        while self.videoStreaming:
            # Read Frame
            ret, frame = self.cap.read()
            if ret:
                if params != None:
                    callback (frame, params)
                else:
                    callback(frame)

                time.sleep(1/ self.frequency)

    def setFrequency (self, frequency):
        self.frequency = frequency

    def StartVideoStream (self, frequency, callback, params = None):
        self.videoStreaming = True
        self.frequency = frequency
        streamingThread = threading.Thread(
            target=self._start_video_stream,
            args=[callback, params])
        streamingThread.start()


    def StopVideoStream (self):
        self.videoStreaming = False

    def Close (self):
        self.cap.release()
