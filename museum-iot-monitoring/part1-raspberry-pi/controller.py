import paho.mqtt.publish as publish
import random
import time

MQTT_SERVER = "10.6.1.9"
TOPIC = "CONTROLLER_7"

while(True):
    command = input("Comandos ON/OFF\nInsira: ")
    if(command == "ON" or command == "OFF"):
        publish.single(TOPIC,command,hostname=MQTT_SERVER)
    else:
        print("Formato errado")
