import ssl

import cv2 as cv
import numpy as np

import paho.mqtt.client as mqtt
import base64
import threading
import time
import json
from Camera import *
import asyncio
import websockets


async def receive_and_display_frames():
    uri = "ws://localhost:8765"  # Adjust the WebSocket server URL
    frame_count = 0
    is_processing = False  # Flag to track if the client is busy processing a frame

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to the server.")

                ''' # Send the video file link to the server
                video_link = "rtsp://zephyr.rtsp.stream/movie?streamKey=YOUR_KEY"

                await websocket.send(video_link)
                print(f"Sent video link: {video_link}")'''

                while True:
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
                        cv.imshow("Frame", frame)
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
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection")

def on_message(client, userdata, message):
    global origin
    global recibido

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]


    if command == "picture":
        print("recibo picture")
        img = base64.b64decode(message.payload)

        npimg = np.frombuffer(img, dtype=np.uint8)
        # Decode to Original Frame
        img = cv.imdecode(npimg, 1)
        # show stream in a separate opencv window
        img = cv.resize(img, (640, 480))
        cv.imshow("Picture", img)
        cv.waitKey(1)
        recibido = True

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
        recibido = True






external_client = mqtt.Client("consolaRemota", transport="websockets")
external_client.on_message = on_message
external_client.on_connect = on_connect
external_client.username_pw_set("dronsEETAC", "mimara1456.")
external_client.connect("classpip.upc.edu", 8000)
print("Connected to classpip.upc.edu:8000")
external_client.subscribe("service/#", 2)
external_client.loop_start()
recibido = False

'''external_client.publish("consolaRemota/service/takePicture")
time.sleep (5)'''

print ('empezamos')



print ('pido que empiece el stream')

parameters = {'quality': 60,
              'frequency': 10}
parameters_json = json.dumps(parameters)

external_client.publish("consolaRemota/service/startVideoStreamWebSocket", parameters_json)

asyncio.get_event_loop().run_until_complete(receive_and_display_frames())
print ('ya he puesto en marcha el cliente')

time.sleep(20)
external_client.publish("consolaRemota/service/stopVideoStream")
while not recibido:
    pass
print ('final')

