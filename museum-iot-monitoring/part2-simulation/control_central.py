import sys
import socket
import time
import os
from _thread import *
import json
import paho.mqtt.publish as publish

ip_address = '10.16.2.192'
MQTT_SERVER = '10.6.1.9'
MQTT_PORT = 1883
MQTT_ROOM = "12_ACT"
MQTT_ROOM2 = "OTHER_ACT"

######## TCP from Data Processing Unit #######

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ServerSocket.bind((ip_address, 5001)) 
except socket.error as e:
    print(str(e))
    sys.exit(1)

##############################################

ServerSocket.listen(5)

def multi_threaded_client(connection):
    try:
        data = connection.recv(2048)
        response = data.decode('utf-8')

        try:
            response = json.loads(response)

            ########### Redirect stderr to null ##########
            #### So it doesn't show connection errors #### 
            sys.stderr = open(os.devnull, 'w')

            publish.single(MQTT_ROOM, payload=json.dumps(response), hostname=MQTT_SERVER,port=MQTT_PORT, transport="tcp")
            publish.single(MQTT_ROOM2, payload=json.dumps(response), hostname=MQTT_SERVER,port=MQTT_PORT, transport="tcp")
            
            ################ Reset stderr ################
            sys.stderr = sys.__stderr__
            
        except (TypeError, ValueError):
            pass

        print(response)
        connection.close()

    except Exception:
        import traceback
        print(traceback.format_exc())
        connection.close()

try:
    while True:
        Client, address = ServerSocket.accept()
        start_new_thread(multi_threaded_client, (Client,))

except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
finally:
    ServerSocket.close()


