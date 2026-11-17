import paho.mqtt.publish as publish
import random
import time

MQTT_SERVER = "10.6.1.9"
DPU_TOPIC = "ALARM_CONSOLE_12"

while(True):
    command = input("Comandos ON/OFF\nInsira: ")
    if(command.upper() == "ON" or command.upper() == "OFF"):
        publish.single(DPU_TOPIC, command.upper(), hostname=MQTT_SERVER)
    else:
        print("Formato errado")