import paho.mqtt.client as mqtt_client
import time

# VARIABLES
MQTT_BROKER = "10.6.1.9" #broker address, it can be IP of raspberry pi or simply localhost
MQTT_PORT = 1883
MQTT_TOPIC = "12_ROOM_DATA" #"12_ROOM_DATA" #topic # MQTT topic format: GroupID_TOPIC
MQTT_TOPIC2 = "OTHER_ROOMS"

# METHODS
def on_connect(client, userdata, flags, rc, properties):
    # Subscribing in on_connect() means if we lose the connection and reconnect then subscriptions will be renewed.
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] : [{msg.topic}] : [{msg.payload.decode()}]")
    #print(f"Received {msg.payload.decode()} from {msg.topic} topic")
 
# CONNECTING
client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(MQTT_TOPIC)
client.subscribe(MQTT_TOPIC2)
client.loop_forever() # use this line if you don't want to write any further code. It blocks the code forever to check for data