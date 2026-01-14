import paho.mqtt.client as mqtt

from maps import updateStops
from music import updateSongQueue

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("queues/songs")
    client.subscribe("queues/stops")

def on_message(client, userdata, msg):
    print(f"Recieved message on topic {msg.topic}: {msg.playload}")
    if msg.payload == b"Yes":
        try:
            updateStops()
            print("Stops Updated Successfully")
            updateSongQueue()
            print("Song Queue Updated Successfully")
        except Exception as e:
            print(e)
    else:
        print("Not updating Stops and Song Queue")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
print("Listening Forever")
try:
    client.loop_forever()
except:
    print("Something Happened Connecting to the Broker!")