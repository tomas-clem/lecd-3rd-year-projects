import json
import random
import time
import paho.mqtt.client as mqtt_client
import paho.mqtt.publish as publish # type: ignore
import sys

message =  {
    "room_number": 0, 
    "ac_switch_on": 0, 
    "hc_switch_on": 0, 
    "temperature_ideal": 0.0, 
    "humidity_ideal": 0
    }

if len(sys.argv) != 4:
    print("Usage: {sys.argv[0]} <GroupID> <TEMP_TIME> <MOV_TIME>")
    sys.exit(1)

GROUP_ID, TEMP_TIME, MOV_TIME = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])

# Replace with your group ID and MQTT Server details
MQTT_SERVER = '10.6.1.9'
MQTT_PORT = 1883
MQTT_TOPIC = f'{GROUP_ID}_ROOM_DATA'
TOPIC_CONTROL_CENTRAL = f'{GROUP_ID}_ACT'

# MQTT Publisher setup
client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))

    client.subscribe(TOPIC_CONTROL_CENTRAL)

def on_message(client, userdata, msg):
    global message

    if json.loads(msg.payload.decode("utf-8"))["room_number"] == room_number:
        message = json.loads(msg.payload.decode("utf-8"))
    
########### Connect to Broker via MQTT ###########

client.on_connect = on_connect
client.connect(MQTT_SERVER, MQTT_PORT)
client.on_message = on_message
client.loop_start()

##################################################

def simulate_room(room_number, temp_time, mov_time):

    room_data = {
        "temperature": 23.3,  # Initial temperature
        "humidity": 50,       # Initial humidity
        "motion": 0,          # Initial motion detection
        "ac_working": 0,      # Air conditioner status
        "hc_working": 0,      # Humidity controller status
        "sensor_type": 1,     # Sensor type
        "room_number": room_number  # Room number
    }

    while True:

        global message       

        # Simulate temperature changes
        if int(message["ac_switch_on"]) == 1:
            room_data["ac_working"] = 1
            if float(message["temperature_ideal"]) >= room_data["temperature"]:
                room_data["temperature"] += 0.5
            if float(message["temperature_ideal"]) < room_data["temperature"]:
                room_data["temperature"] -= 0.5
        else:
            room_data["ac_working"] = 0
            room_data["temperature"] += random.uniform(-0.1, 0.5)

        # Simulate humidity changes    
        if int(message["hc_switch_on"]) == 1:
            room_data["hc_working"] = 1
            if int(message["humidity_ideal"]) >= room_data["humidity"]:
                room_data["humidity"] += 5
            if int(message["humidity_ideal"]) < room_data["humidity"]:
                room_data["humidity"] -= 5
        else:
            room_data["hc_working"] = 0
            room_data["humidity"] += random.randint(-5, 10)
            room_data["humidity"] = max(0, min(room_data["humidity"], 100))



        # Simulate motion detection
        if int(time.time()) % mov_time == 0:
            room_data["motion"] = 1 if room_data["motion"] == 0 else 0

        # Publish data to MQTT Server
        publish.single(MQTT_TOPIC, payload=json.dumps(room_data), hostname=MQTT_SERVER,port=MQTT_PORT, transport="tcp")
        
        print("Sent:", room_data)
        

        # Wait for the next simulation cycle
        time.sleep(temp_time)

room_number = 5
simulate_room(room_number, temp_time=TEMP_TIME, mov_time=MOV_TIME)