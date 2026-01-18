import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
ACTIONS = "songs/actions"
UPDATES = "songs/updates"
QUIT = 14

DEFAULT_PAYLOAD = {
    "username": "",
    "action": 0,
    "url": "www.youtube.com",
    "original_index": 0,
    "new_index": 0,
    "new_time": 0,
    "new_volume": 0
}

ACTIONS_TABLE = {
    1: "Start Song",
    2: "Start Playlist",
    3: "Queue Song",
    4: "Queue Song NEXT",
    5: "Queue Playlist",
    6: "Queue Playlist NEXT",
    7: "Move Song",
    8: "Delete Song",
    9: "Adjust Song Time",
    10: "Adjust Volume",
    11: "Toggle Playback",
    12: "Skip Reverse",
    13: "Skip Forward",
    14: "Quit"
}

def print_queue(payload):
    print(f"Currently Playing : {payload["current_song"]}")
    print("Queue: ")
    for i, song in payload["queue"]:
        print(f"\t{i} : {song}")
    print("Trashbin: ")
    for i, song in payload["trashbin"]:
        print(f"\t-{i} : {song}")

def print_action():
    print("Actions: ")
    for i, action in ACTIONS_TABLE.items():
        print(f"\t{i} : {action}")

def requires_url(action):
    return action < 7

def get_url():
    return input("Enter YouTube URL: ")

def create_payload(username):
    print_action()
    payload = DEFAULT_PAYLOAD.copy()
    action = int(input("Enter Action: "))
    if (action == QUIT):
        return None
    payload["action"] = action
    payload["username"] = username

    if requires_url(action):
        payload["url"] = get_url()

    match action:
        case 7:
            payload["original_index"] = int(input("Enter location of move song: "))
            payload["new_index"] = int(input("Enter move location: "))
        
        case 8:
            payload["original_index"] = int(input("Enter song you'd like to delete: "))

        case 9:
            payload["new_time"] = int("Enter new song time: ")

        case 10:
            payload["new_volume"] = int(input("Enter volume level (1-100): "))
    
    return payload

def on_message(client, userdata, msg):
    payload = json.load(msg.payload.decode())

    if payload["success"] == 0:
        print_queue(payload)


def on_connect(client, userdata, flags, rc):
    print(f"[CLIENT] Connected with result code {rc}")

def create_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)

    client.subscribe(UPDATES)

    client.loop_start()
    time.sleep(1)   # give time to connect
    return client


client = create_client()
username = input("Enter a username: ")
while True:
    payload = create_payload(username)

    if payload is None:
        break

    json_payload = json.dumps(payload)
    client.publish(ACTIONS, json_payload)

    time.sleep(1)
client.loop_stop()
client.disconnect()