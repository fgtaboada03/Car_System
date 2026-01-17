import paho.mqtt.client as mqtt

import threading
import time
import json

from LocalServer.maps.operator import action
from LocalServer.music.actions import music_action
from LocalServer.music.controller import Controller

controller = Controller()

BROKER = "localhost"
PORT = 1883
CHANNELS = [
    "songs/actions",
    "songs/updates",
    "maps/actions",
    "maps/updates"
]

DEFAULT_PAYLOAD = {
    "success" : 0,
    "playback" : 0,
    "current_song": "",
    "queue": {
        1 : "song_title",
        2 : "song_title"
    },
    "trashbin": {
        1 : "song_title",
        2 : "song_title"
    }
}
def connect_channels(client):
    for channel in CHANNELS:
        print(f"Connected to channel {channel}")
        client.subscribe(channel)
    
def propogate_update(current_song, queue, trashbin):
    print("Propogated Update")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    connect_channels(client)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Received message on topic {msg.topic}: {payload}")
        music_action(controller, payload)

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

def start_server():
    server = create_server()
    threading.Thread(target=autoplay_loop, daemon=True).start()
    return server
