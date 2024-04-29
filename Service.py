import ssl

import paho.mqtt.client as mqtt
import base64
import time
import json
from Camera import *


def publish_video_stream (frame, quality):
    global external_client, origin
    _, image_buffer = cv.imencode(".jpg", frame, [int(cv.IMWRITE_JPEG_QUALITY), quality])
    jpg_as_text = base64.b64encode(image_buffer)
    external_client.publish("service/" + origin + "/frame", jpg_as_text)


def on_message(client, userdata, message):
    global camera
    global origin

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

    if command == "stopVideoStream":
        print("stop video stream")
        camera.StopVideoStream()

    if command == "closeCamera":
        print("close camera")
        camera.Close()




def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection OK")
    else:
        print("Bad connection")

def Service(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap
    global colorDetector
    global camera



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

    external_client.loop_forever()


if __name__ == "__main__":
    import sys

    connection_mode = sys.argv[1]  # global or local
    operation_mode = sys.argv[2]  # simulation or production
    username = None
    password = None
    if connection_mode == "global":
        external_broker = sys.argv[3]
        if external_broker == "classpip_cred" or external_broker == "classpip_cert":
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    Service(connection_mode, operation_mode, external_broker, username, password)
