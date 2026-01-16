import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "actions/songs"   # change to actions/stops if needed

DEFAULT_PAYLOAD = {
    "username": "",
    "action": 0,
    "url": "www.youtube.com",
    "original_index": 0,
    "new_index": 0,
    "new_time": 0,
    "new_volume": 0
}

def on_connect(client, userdata, flags, rc):
    print(f"[CLIENT] Connected with result code {rc}")

def print_action():
    return

def print_queue():
    return

def requires_url(action):
    return action < 7

def get_url():
    return input("Enter YouTube URL: ")

def create_payload(username):
    print_action()
    payload = DEFAULT_PAYLOAD.copy()
    action = int(input("Enter Action: "))
    payload["action"] = action
    payload["username"] = username

    if requires_url(action):
        payload["url"] = get_url()

    match action:
        case 7:
            print_queue()
            payload["original_index"] = int(input("Enter location of move song: "))
            payload["new_index"] = int(input("Enter move location: "))
        
        case 8:
            payload["original_index"] = int(input("Enter song you'd like to delete: "))

        case 9:
            payload["new_time"] = int("Enter new song time: ")

        case 10:
            payload["new_volume"] = int(input("Enter volume level (1-100): "))
    
    return payload

def create_client():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()
    time.sleep(1)   # give time to connect
    return client


client = create_client()
username = input("Enter a username: ")
while True:
    payload = create_payload(username)

    json_payload = json.dumps(payload)
    client.publish(TOPIC, json_payload)

    time.sleep(1)

    if input("Enter Q to quit.").lower() == "q":
        break
client.loop_stop()
client.disconnect()