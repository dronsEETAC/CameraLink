from CameraLink.Camera import *
import cv2 as cv

def showVideoStream (frame):
    cv.imshow("videostream", frame)
    cv.waitKey(1)

print ('voy a poner en marcha la cámara')
camera = Camera ()
print ('Ya tengo la cámara preparada')

print ('pido una foto')
ret, frame = camera.TakePicture()
if ret:
    cv.imshow("Picture", frame)
    cv.waitKey(1)
    time.sleep (5)
else:
    print ('error')

print ('pido otra foto')
ret,frame = camera.TakePicture()
cv.imshow("Picture", frame)
cv.waitKey(1)
time.sleep (5)

print ('Inicio el stream de video')
# 10 frames por segundo
camera.StartVideoStream(10,showVideoStream)
# veo el video durante 15 segundos
time.sleep (15)
camera.StopVideoStream()
camera.Close()


