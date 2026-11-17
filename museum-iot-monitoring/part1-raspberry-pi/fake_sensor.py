import paho.mqtt.publish as publish
import random
import time

MQTT_SERVER = "10.6.1.9"
TOPIC = "VIRTUAL_SENSOR_7"


while True:
    publish.single(TOPIC,random.randint(0,5000)/100,hostname=MQTT_SERVER)
    time.sleep(3) # Time until it sends new data


    
