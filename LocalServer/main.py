import paho.mqtt.client as mqtt

import threading
import time

from maps.operator import action
from music.actions import music_action
from music.controller import Controller

controller = Controller()

BROKER = "localhost"
PORT = 1883
TOPIC_1 = "actions/songs"
TOPIC_2 = "actions/stops"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC_1)
    client.subscribe(TOPIC_2)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Received message on topic {msg.topic}: {payload}")

        music_action(controller, msg)

    except Exception as e:
        print("Error handling message:", e)

def autoplay_loop():
    while True:
        time.sleep(0.1)  # lightweight polling
        if controller.is_song_over():
            print("Song ended, autoplaying next...")
            controller.skip_forward()
    
def create_server():
    server = mqtt.Client()
    server.on_connect = on_connect
    server.on_message = on_message
    server.connect(BROKER, PORT, 60)
    server.loop_start()
    return server

server = create_server()
threading.Thread(target=autoplay_loop, daemon=True).start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    server.loop_stop()
