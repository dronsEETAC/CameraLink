import json
import time
import tkinter as tk
from Camera import Camera
from tkinter import messagebox

import paho.mqtt.client as mqtt
import cv2 as cv
import base64
import numpy as np

def on_connect(client, userdata, flags, rc):
    global connectBtn
    if rc == 0:
        connectBtn ['text'] = 'Conectado'
        connectBtn ['fg'] = 'white'
        connectBtn ['bg'] ='green'
    else:
        connectBtn['text'] = 'Fallo de conexion'
        connectBtn['fg'] = 'white'
        connectBtn['bg'] = 'red'

def on_message(client, userdata, message):
    global origin

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]

    if command == "picture":
        img = base64.b64decode(message.payload)

        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        img = cv.resize(img, (320, 240))
        cv.imshow("Picture", img)
        cv.waitKey(1)



    if command == "frame":
        img = base64.b64decode(message.payload)
        # converting into numpy array from buffer
        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        img = cv.resize(img, (640, 480))
        cv.imshow("Stream", img)
        cv.waitKey(1)




def connect ():
    global client
    camera = Camera()

    client = mqtt.Client("DashRemoto", transport="websockets")
    client.on_message = on_message
    client.on_connect = on_connect
    client.username_pw_set("dronsEETAC", "mimara1456.")
    client.connect("classpip.upc.edu", 8000)
    print("Connected to classpip.upc.edu:8000")
    client.subscribe("service/DashRemoto/#", 2)
    client.loop_start()

def takePicture ():
    global client, takePictureBtn
    client.publish("DashRemoto/service/takePicture")


def videoStream ():
    global client, streaming
    global qualitySldr, frequencySldr, videoStreamBtn

    if streaming:
        client.publish("DashRemoto/service/stopVideoStream")
        videoStreamBtn['text'] = 'Iniciar video streaming'
        videoStreamBtn['fg'] = 'black'
        videoStreamBtn['bg'] = 'dark orange'
        streaming = False

    else:
        parameters = {'quality': int (qualitySldr.get()),
                      'frequency': int (frequencySldr.get())}
        parameters_json = json.dumps(parameters)
        client.publish("DashRemoto/service/startVideoStreamMQTT", parameters_json)
        videoStreamBtn['text'] = 'Detener video streaming'
        videoStreamBtn['fg'] = 'white'
        videoStreamBtn['bg'] = 'green'
        streaming = True





def stopVideoStream ():
    global client
    client.publish("DashRemoto/service/stopVideoStreamMQTT")

def close():
    global client, ventana
    client.publish("DashRemoto/service/closeCamera")
    ventana.destroy()



def crear_ventana():
    global camera
    global connectBtn, qualitySldr, frequencySldr, videoStreamBtn, takePictureBtn
    global streaming
    global ventana

    streaming = False


    ventana = tk.Tk()
    ventana.geometry('200x400')
    ventana.title("Dash Camara")
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)
    ventana.rowconfigure(3, weight=1)
    ventana.rowconfigure(4, weight=1)
    ventana.rowconfigure(5, weight=1)
    ventana.rowconfigure(6, weight=1)
    ventana.columnconfigure(0, weight=1)



    connectBtn = tk.Button(ventana, text="Conectar la cámara", bg="dark orange", command = connect)
    connectBtn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    takePictureBtn = tk.Button(ventana, text="Foto", bg="dark orange", command=takePicture)
    takePictureBtn.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    qualitySldr = tk.Scale(ventana, label="Calidad:", resolution=5, from_=0, to=100, tickinterval=20,
                          orient=tk.HORIZONTAL)
    qualitySldr.set(50)
    qualitySldr.grid(row=2, column=0,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    frequencySldr = tk.Scale(ventana, label="Frames por segundo:", resolution=1, from_=0, to=30, tickinterval=5,
                              orient=tk.HORIZONTAL)
    frequencySldr.set(10)
    frequencySldr.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    videoStreamBtn = tk.Button(ventana, text="Inicia video stream", bg="dark orange", command=videoStream)
    videoStreamBtn.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    '''stopVideoStreamBtn = tk.Button(ventana, text="Detener video stream", bg="dark orange", command=stopVideoStream)
    stopVideoStreamBtn.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
    '''
    closeBtn = tk.Button(ventana, text="Cerrar", bg="dark orange", command = close)
    closeBtn.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)



    return ventana


if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()
