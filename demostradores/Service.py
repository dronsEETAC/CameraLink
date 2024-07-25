import random
import ssl

import cv2 as cv

import paho.mqtt.client as mqtt
import base64
import threading
import time
import json
from CameraLink.Camera import *

import asyncio
import websockets
import netifaces as ni



def process_new_frame (frame):
    # Aqui recibo los frames que me envia camLib
    global newFrame, newFrameReady
    newFrame = frame
    newFrameReady = True



async def process_video(websocket, path):
    global camera
    global newFrame, newFrameReady
    global quality, frequency, videoStreaming, running

    try:
        print("Client connected.")

        frame_count = 0
        isProcessing = False
        processing_delay = 0.0  # Simulated delay between sending responses (adjust as needed)
        running = True
        while running:
            if videoStreaming:
                # Check if the server is still processing the previous frame
                if isProcessing:
                    await asyncio.sleep(processing_delay)
                    continue

                newFrameReady = False
                while not newFrameReady:
                    pass

                # Set the processing flag to indicate that the server is busy
                isProcessing = True

                frame_count += 1
                print(f"Processing frame {frame_count}...")

                # Encode the frame as base64
                _,  frame_data = cv.imencode(".jpg", newFrame, [int(cv.IMWRITE_JPEG_QUALITY), quality])
                base64_frame = base64.b64encode(frame_data).decode("utf-8")

                # Send the base64-encoded frame to the client
                await websocket.send(base64_frame)

                # Simulate processing delay
                await asyncio.sleep(processing_delay)

                # Reset the processing flag once frame processing is complete
                isProcessing = False

        # Close the video file and connection when finished
        #cap.release()
        print("Video processing complete. Closing connection.")
        await websocket.close()

    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected. Waiting for a new connection...")
    except Exception as e:
        print(f"Error on the server: {str(e)}")


def start_server_websockets ():
    start_server = websockets.serve(process_video, "0.0.0.0", 8765)  # Adjust the host and port
    print("WebSocket server started.")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def publish_video_stream (frame, quality):
    global external_client, origin
    _, image_buffer = cv.imencode(".jpg", frame, [int(cv.IMWRITE_JPEG_QUALITY), quality])
    jpg_as_text = base64.b64encode(image_buffer)
    client.publish("service/" + origin + "/frame", jpg_as_text)


def on_message(client, userdata, message):
    global camera
    global origin
    global quality, frequency, videoStreaming, running
    global op_mode

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]

    if command == "takePicture":
        print("Take picture")
        ret, frame = camera.TakePicture()
        _, image_buffer = cv.imencode(".jpg", frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(image_buffer)
        client.publish("service/" + origin + "/picture", jpg_as_text)

    if command == "startVideoStreamMQTT":
        print("start video stream via MQTT")
        parameters = json.loads(message.payload)
        camera.StartVideoStream(parameters['frequency'], publish_video_stream, parameters['quality']  )

    if command == "startVideoStreamWebsocket":
        print("start video stream via webSockets")
        parameters = json.loads(message.payload)
        frequency = parameters['frequency']
        quality = parameters['quality']
        videoStreaming = True
        camera.StartVideoStream(frequency, process_new_frame)

    if command == "getServerIP":
        print("get server IP")
        if op_mode == 'simulation':
            IP = "localhost"
        else:
            IP = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        client.publish("service/" + origin + "/IP", IP)

    if command == "stopVideoStream":
        print("stop video stream")
        videoStreaming = False
        camera.StopVideoStream()

    if command == "setParameters":
        print("set parameters")
        parameters = json.loads(message.payload)
        frequency = parameters['frequency']
        camera.setFrequency(frequency)
        quality = parameters['quality']


    if command == 'close':
        # paro el server de websockets
        running = False
        camera.Close()



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection")

def Service2(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap
    global colorDetector
    global camera
    global op_mode


    print("Connection mode: ", connection_mode)
    print("Operation mode: ", operation_mode)
    op_mode = operation_mode

    camera = Camera()
    print('ya tengo la camara activa')

    external_client = mqtt.Client("Service", transport="websockets")
    external_client.on_message = on_message
    external_client.on_connect = on_connect

    if connection_mode == "global":
        if external_broker == "hivemq":
            external_client.connect("broker.hivemq.com", 8000)
            print("Connected to broker.hivemq.com:8000")

        elif external_broker == "hivemq_cert":
            external_client.tls_set(
                ca_certs=None,
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            external_client.connect("broker.hivemq.com", 8884)
            print("Connected to broker.hivemq.com:8884")

        elif external_broker == "classpip_cred":
            external_client.username_pw_set(username, password)
            external_client.connect("classpip.upc.edu", 8000)
            print("Connected to classpip.upc.edu:8000")

        elif external_broker == "classpip_cert":
            external_client.username_pw_set(username, password)
            external_client.tls_set(
                ca_certs=None,
                certfile=None,
                keyfile=None,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS,
                ciphers=None,
            )
            external_client.connect("classpip.upc.edu", 8883)
            print("Connected to classpip.upc.edu:8883")
        elif external_broker == "localhost":
            external_client.connect("localhost", 8000)
            print("Connected to localhost:8000")
        elif external_broker == "localhost_cert":
            print("Not implemented yet")

    elif connection_mode == "local":
        if operation_mode == "simulation":
            external_client.connect("localhost", 8000)
            print("Connected to localhost:8000")
        else:
            external_client.connect("10.10.10.1", 8000)
            print("Connected to 10.10.10.1:8000")

    print("Waiting....")
    external_client.subscribe("+/service/#", 2)
    external_client.loop_start()
    start_server_websockets()

    '''start_server = websockets.serve(process_video, "localhost", 8765)  # Adjust the host and port
    print("WebSocket server started.")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()'''

def Service(operation_mode):

    global client

    global state
    global cap
    global colorDetector
    global camera
    global op_mode

    print("Operation mode: ", operation_mode)
    op_mode = operation_mode


    camera = Camera()
    print('ya tengo la camara activa')

    randomId = random.randint(1000, 9000)
    client = mqtt.Client("Service"+ str(randomId), transport="websockets")
    client.on_message = on_message
    client.on_connect = on_connect

    client.username_pw_set('dronsEETAC', 'mimara1456.')
    client.connect("classpip.upc.edu", 8000)
    print("Connected to classpip.upc.edu:8000")
    print("Waiting....")
    client.subscribe("+/service/#", 2)
    client.loop_start()
    start_server_websockets()



if __name__ == "__main__":
    import sys
    operation_mode = sys.argv[1]  # simulation o production

    Service(operation_mode)
