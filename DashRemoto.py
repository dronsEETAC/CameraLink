import json
import threading
import time
import tkinter as tk
from Camera import Camera
from tkinter import messagebox

import paho.mqtt.client as mqtt
import cv2 as cv
import base64
import numpy as np


import asyncio
import websockets



async def receive_and_display_frames():
    global connectWebsocket
    global serverIP
    global runningWebsocketStreaming
    uri = "ws://localhost:8765"  # Adjust the WebSocket server URL
    uri = "ws://"+serverIP+":8765"  # Adjust the WebSocket server URLç
    print ('uri ', uri)
    frame_count = 0
    is_processing = False  # Flag to track if the client is busy processing a frame

    runningWebsocketStreaming = True
    while runningWebsocketStreaming:
        if connectWebsocket:
            try:
                async with websockets.connect(uri) as websocket:
                    print("Connected to the server.")

                    ''' # Send the video file link to the server
                    video_link = "rtsp://zephyr.rtsp.stream/movie?streamKey=YOUR_KEY"
    
                    await websocket.send(video_link)
                    print(f"Sent video link: {video_link}")'''

                    while connectWebsocket:
                        # Check if the client is already processing a frame
                        if is_processing:
                            continue

                        # Receive a base64-encoded frame from the server
                        base64_frame = await websocket.recv()

                        # Check if the received response is empty (broken response) and skip it
                        if not base64_frame:
                            continue

                        # Set the processing flag to indicate that the client is busy
                        is_processing = True

                        frame_count += 1
                        print(f"Received frame {frame_count}...")

                        try:
                            # Decode the base64 frame and display it
                            frame_data = base64.b64decode(base64_frame)
                            frame_np = np.frombuffer(frame_data, np.uint8)
                            frame = cv.imdecode(frame_np, 1)
                            cv.imshow("Websockets", frame)
                            cv.waitKey(1)  # Adjust the delay as needed

                        except Exception as e:
                            print(f"Error decoding frame: {str(e)}")

                        # Reset the processing flag once frame processing is complete
                        is_processing = False

            except websockets.exceptions.ConnectionClosedError:
                print("Connection to the server closed. Reconnecting...")
                await asyncio.sleep(5)  # Wait for a few seconds before attempting to reconnect
            except Exception as e:
                print(f"Error on the client: {str(e)}")







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
    global origin, serverIP, getServerIPBtn

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
        cv.imshow("MQTT", img)
        cv.waitKey(1)

    if command == "IP":
        serverIP = message.payload.decode("utf-8")
        getServerIPBtn['text'] = 'Ya tengo la IP (' + serverIP + ')'
        getServerIPBtn['fg'] = 'white'
        getServerIPBtn['bg'] = 'green'


def connect ():
    global client

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


def videoStreamMQTT ():
    global client, streamingMQTT
    global qualitySldr, frequencySldr, videoStreamMQTTBtn

    if streamingMQTT:
        client.publish("DashRemoto/service/stopVideoStream")
        videoStreamMQTTBtn['text'] = 'Iniciar video streaming via MQTT'
        videoStreamMQTTBtn['fg'] = 'black'
        videoStreamMQTTBtn['bg'] = 'dark orange'
        streamingMQTT = False

    else:
        parameters = {'quality': int (qualitySldr.get()),
                      'frequency': int (frequencySldr.get())}
        parameters_json = json.dumps(parameters)

        client.publish("DashRemoto/service/startVideoStreamMQTT", parameters_json)
        videoStreamMQTTBtn['text'] = 'Detener video streaming'
        videoStreamMQTTBtn['fg'] = 'white'
        videoStreamMQTTBtn['bg'] = 'green'
        streamingMQTT = True
async def startStreamingWebsockets():
    asyncio.get_event_loop().run_until_complete(receive_and_display_frames())

def startConnection ():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(receive_and_display_frames())
def getServerIP ():
    global client
    client.publish("DashRemoto/service/getServerIP")


def videoStreamWebsocket ():
    global client, streamingWebsocket
    global qualitySldr, frequencySldr, videoStreamWebsocketBtn
    global connectWebsocket

    if streamingWebsocket:
        videoStreamWebsocketBtn['text'] = 'Iniciar video streaming via Websocket'
        videoStreamWebsocketBtn['fg'] = 'black'
        videoStreamWebsocketBtn['bg'] = 'dark orange'
        streamingWebsocket = False
        connectWebsocket = False

    else:
        parameters = {'quality': int (qualitySldr.get()),
                      'frequency': int (frequencySldr.get())}
        parameters_json = json.dumps(parameters)
        print ('publico start websocket')
        client.publish("DashRemoto/service/startVideoStreamWebsocket", parameters_json)
        connectWebsocket = True
        websocketThread = threading.Thread (target = startConnection)
        websocketThread.start()

        videoStreamWebsocketBtn['text'] = 'Detener video streaming'
        videoStreamWebsocketBtn['fg'] = 'white'
        videoStreamWebsocketBtn['bg'] = 'green'
        streamingWebsocket = True



def stopVideoStream ():
    global client
    client.publish("DashRemoto/service/stopVideoStreamMQTT")

def close():
    global client, ventana, runningWebsocketStreaming
    client.publish("DashRemoto/service/close")
    runningWebsocketStreaming = False
    ventana.destroy()



def changeParameters ():
    global frequencySldr, qualitySldr
    parameters = {'quality':  int(qualitySldr.get()),
                  'frequency': int(frequencySldr.get())}
    parameters_json = json.dumps(parameters)

    client.publish("DashRemoto/service/setParameters", parameters_json)

def crear_ventana():
    global camera
    global connectBtn, qualitySldr, frequencySldr, videoStreamMQTTBtn, takePictureBtn, videoStreamWebsocketBtn
    global streamingMQTT, streamingWebsocket, connectWebsocket
    global ventana
    global getServerIPBtn

    streamingMQTT = False
    streamingWebsocket = False
    connectWebsocket = False


    ventana = tk.Tk()
    ventana.geometry('350x400')
    ventana.title("Dash Camara")
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)
    ventana.rowconfigure(3, weight=1)
    ventana.rowconfigure(4, weight=1)
    ventana.rowconfigure(5, weight=1)
    ventana.rowconfigure(6, weight=1)
    ventana.rowconfigure(7, weight=1)
    ventana.rowconfigure(8, weight=1)
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

    parametersBtn = tk.Button(ventana, text="Cambia parámetros", bg="dark orange",
                                   command=changeParameters)
    parametersBtn.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    videoStreamMQTTBtn = tk.Button(ventana, text="Inicia video stream via MQTT", bg="dark orange", command=videoStreamMQTT)
    videoStreamMQTTBtn.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    getServerIPBtn = tk.Button(ventana, text="Obtener IP del servidor (para conexión por  websocket)", bg="dark orange",
                                        command=getServerIP)
    getServerIPBtn.grid(row=6, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    videoStreamWebsocketBtn = tk.Button(ventana, text="Inicia video stream via websocket", bg="dark orange", command=videoStreamWebsocket)
    videoStreamWebsocketBtn.grid(row=7, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    closeBtn = tk.Button(ventana, text="Cerrar", bg="dark orange", command = close)
    closeBtn.grid(row=8, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)





    return ventana


if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()
