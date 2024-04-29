from Camera import *
from Dron import *

import cv2 as cv

def show (frame):
    cv.imshow("videostream", frame)
    cv.waitKey(1)
def enTierra ():
    print ('ya estamos en tierra')
camera = Camera ()
'''dron = Dron()
connection_string = 'tcp:127.0.0.1:5763'
baud = 115200'''
print ('voy a conectarme')
#dron.connect (connection_string, baud)
print ('ya estoy conectado')
camera.StartVideoStream(10,show)
#dron.arm()
print ('armado')
#dron.takeOff(5)
print ('en el aire')
#dron.startGo()
#dron.go('North')
print ('volando al norte durante 20 segundos')
time.sleep (10)
#dron.stopGo()
camera.StopVideoStream()
camera.Close()
print ('aterrizamos')
#dron.Land(blocking = False, callback=enTierra)


while True:
    time.sleep(1)