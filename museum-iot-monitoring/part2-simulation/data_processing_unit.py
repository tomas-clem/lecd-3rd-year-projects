import paho.mqtt.client as mqtt_client
import time
import config
import socket
import json
from influxdb_client_3 import InfluxDBClient3, Point

from influxdb_client_3 import flight_client_options
import certifi
import datetime


MQTT_BROKER = "10.6.1.9"
MQTT_PORT = 1883
MQTT_TOPIC1 = "12_ROOM_DATA"
MQTT_TOPIC2 = "OTHER_ROOMS"
MQTT_TOPIC_ALARM = "ALARM_CONSOLE_12"

ip_address = '10.16.2.192' 
startTime_1 = time.time()
startTime_2 = time.time()
startTime_3 = time.time()
startTime_4 = time.time()
startTime_5 = time.time()
alarm_state = False
status = {"ac1":0, "ac2":0, "ac3":0, "ac4":0, "ac5":0, "hc1":0, "hc2":0,"hc3":0, "hc4":0, "hc5":0}
times = {"ac1":0, "ac2":0, "ac3":0, "ac4":0, "ac5":0, "hc1":0, "hc2":0,"hc3":0, "hc4":0, "hc5":0, "ac1_hours":0, "ac2_hours":0, 
         "ac3_hours":0, "ac4_hours":0, "ac5_hours":0, "hc1_hours":0, "hc2_hours":0,"hc3_hours":0, "hc4_hours":0, "hc5_hours":0}


cfg = config.Config('intervals.cfg')

# Defining the InfluxDB host
token = "{token}" 	
org = "FCTUC"		
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "SRSA_Project"

fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()
write_client = InfluxDBClient3(host=host, token=token, database=database, org=org, flight_client_options=flight_client_options(tls_root_certs=cert))
#####################

def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code "+str(rc))

    client.subscribe(MQTT_TOPIC1)
    client.subscribe(MQTT_TOPIC2) 
    client.subscribe(MQTT_TOPIC_ALARM)  

def on_message(client, userdata, msg):

    # Turn ON/OFF MOTION ALARM by Alarm Console #
    global alarm_state 

    if(msg.topic == "ALARM_CONSOLE_12"):
        if(msg.payload == b"ON"): 
            try:
                ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientSocket.connect((ip_address, 5001))   
                ClientSocket.send(str.encode("==== ALARM ON ==== ALARM ON ==== ALARM ON ===="))
                ClientSocket.close()
            except socket.error as e:
                print(str(e))

            alarm_state = True
            p = Point("Project").field("Alarme", "Ligado").time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)

        elif(msg.payload == b"OFF"): 
            try:
                ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientSocket.connect((ip_address, 5001))   
                ClientSocket.send(str.encode("=== ALARM OFF === ALARM OFF === ALARM OFF ==="))
                ClientSocket.close()
            except socket.error as e:
                print(str(e))

            alarm_state = False
            p = Point("Project").field("Alarme", "Desligado").time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)
    #############################################
       
    if(msg.topic == MQTT_TOPIC1 or msg.topic == MQTT_TOPIC2):

        message = json.loads(msg.payload.decode("utf-8"))

        act_data = {
            "room_number": int(message["room_number"]),
            "ac_switch_on": int(message["ac_working"]),
            "hc_switch_on": int(message["hc_working"]),
            "temperature_ideal": float(cfg['temperature.ideal']),
            "humidity_ideal": int(cfg['humidity.ideal'])
        }

        ##### Convert Fahrenheit <-> Celsius #####
        if message["sensor_type"] == 2:
            message["temperature"] = round((message["temperature"]-32)*5/9, 1) # F -> C
            act_data["temperature_ideal"] = round((act_data["temperature_ideal"] * 9/5) + 32, 1) # C -> F
        ##########################################

        ########### TCP to Control Central ###########
        ########### and Energy Consumption ###########

        if ((cfg['temperature.low'] > float(message["temperature"]) or float(message["temperature"]) > cfg['temperature.hi']) and status[f'ac{message["room_number"]}'] == 0):

            times[f'ac{message["room_number"]}'] = time.time()
            times[f'ac{message["room_number"]}_hours'] = str(datetime.datetime.now(datetime.timezone.utc))[11:]
            act_data["ac_switch_on"] = 1
            status[f'ac{message["room_number"]}'] = 1

            p = Point("Project").field("ac_working", "ON").field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)

        elif(status[f'ac{message["room_number"]}'] == 1):
            t = time.time() - times[f'ac{message["room_number"]}']
            p = Point("Project").field("device", "AC").field("watt", float((t*3000)/3600)).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)
        
            if (cfg['temperature.ideal']-0.5 <float(message["temperature"]) and float(message["temperature"])<=cfg['temperature.ideal']+0.5):
                
                t = time.time() - times[f'ac{message["room_number"]}']
                hours = str(datetime.datetime.now(datetime.timezone.utc))[11:]
                cost = (t*0.45)/3600

                p = Point("Project").field("ac_working", "OFF").field("cost", cost).field("device", "AC").field("start",times[f'ac{message["room_number"]}_hours']).field("end", hours).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
                write_client.write(p)

                act_data["ac_switch_on"] = 0
                status[f'ac{message["room_number"]}'] = 0
        else:
            p = Point("Project").field("device", "AC").field("watt", float(0)).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)


        if ((cfg['humidity.low'] > int(message["humidity"]) or int(message["humidity"]) > cfg['humidity.hi']) and status[f'hc{message["room_number"]}'] == 0):

            times[f'hc{message["room_number"]}'] = time.time()
            times[f'hc{message["room_number"]}_hours'] = str(datetime.datetime.now(datetime.timezone.utc))[11:]
            act_data["hc_switch_on"] = 1
            status[f'hc{message["room_number"]}'] = 1

            p = Point("Project").field("hc_working", "ON").field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)
        
        elif(status[f'hc{message["room_number"]}'] == 1):
            t = time.time() - times[f'hc{message["room_number"]}']
            p = Point("Project").field("device", "HC").field("watt", float((t*1000)/3600)).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)

            if (cfg['humidity.ideal']-5 <float(message["humidity"]) and float(message["humidity"]) <=cfg['humidity.ideal']+5):
                
                t = time.time() - times[f'hc{message["room_number"]}']
                hours = str(datetime.datetime.now(datetime.timezone.utc))[11:]
                cost = (t*0.15)/3600

                p = Point("Project").field("hc_working", "OFF").field("cost", cost).field("device", "HC").field("start",times[f'hc{message["room_number"]}_hours']).field("end", hours).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
                write_client.write(p)

                act_data["hc_switch_on"] = 0
                status[f'hc{message["room_number"]}'] = 0
        else:
            p = Point("Project").field("device", "HC").field("watt", float(0)).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)
        
        
        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode(json.dumps(act_data)))
            ClientSocket.close()

        except socket.error as e:
            print(str(e))
            
        ##############################################
        
        ############ Motion Detected #############
        if (alarm_state and int(message["motion"]) == 1):
            try:
                ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientSocket.connect((ip_address, 5001))  
                ClientSocket.send(str.encode("====== SIREN ====== SIREN ====== SIREN ======"))

                p = Point("Project").field("Siren", "SIREN!!!").time(datetime.datetime.now(datetime.timezone.utc))
                write_client.write(p)

                ClientSocket.close()
                
            except socket.error as e:
                print(str(e))

        ##########################################

        ########## Send info to InfluxDB #########
        if (message["sensor_type"] == 1 or message["sensor_type"] == 2):
            
            p = Point("Project").field("temperature", message["temperature"]).field("humidity", message["humidity"]).field("room", message["room_number"]).time(datetime.datetime.now(datetime.timezone.utc))
            write_client.write(p)
        else:
            ### Discarded Data ###
            try:
                ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ClientSocket.connect((ip_address, 5001))   
                
                ClientSocket.send(str.encode(message))

                ClientSocket.close()
                
            except socket.error as e:
                print(str(e))
        ##########################################

        ##### Set Last Message Time by Room ######

        if message["room_number"] == 1:
            global startTime_1
            startTime_1 = time.time()

        if message["room_number"] == 2:
            global startTime_2
            startTime_2 = time.time()
        
        if message["room_number"] == 3:
            global startTime_3
            startTime_3 = time.time()
        
        if message["room_number"] == 4:
            global startTime_4
            startTime_4 = time.time()
        
        if message["room_number"] == 5:
            global startTime_5
            startTime_5 = time.time()

        ##########################################

########### Connect to Broker via MQTT ###########

client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT)
client.on_message = on_message
client.loop_start()

##################################################

######## Less than 15s between messages? #########

while True:
    if (time.time() - startTime_1 > 15):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode("============ ROOM 1 DISCONNECTED ============"))
            ClientSocket.close()
        except socket.error as e:
            print(str(e))

        p = Point("Project").field("Room1_DC", "Room Disconnected").time(datetime.datetime.now(datetime.timezone.utc))
        write_client.write(p)
        startTime_1 = time.time()

    if (time.time() - startTime_2 > 15):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode("============ ROOM 2 DISCONNECTED ============"))
            ClientSocket.close()
        except socket.error as e:
            print(str(e))

        p = Point("Project").field("Room2_DC", "Room Disconnected").time(datetime.datetime.now(datetime.timezone.utc))
        write_client.write(p)
        startTime_2 = time.time()

    if (time.time() - startTime_3 > 15):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode("============ ROOM 3 DISCONNECTED ============"))
            ClientSocket.close()
        except socket.error as e:
            print(str(e))

        p = Point("Project").field("Room3_DC", "Room Disconnected").time(datetime.datetime.now(datetime.timezone.utc))
        write_client.write(p)
        startTime_3 = time.time()

    if (time.time() - startTime_4 > 15):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode("============ ROOM 4 DISCONNECTED ============"))
            ClientSocket.close()
        except socket.error as e:
            print(str(e))

        p = Point("Project").field("Room4_DC", "Room Disconnected").time(datetime.datetime.now(datetime.timezone.utc))
        write_client.write(p)
        startTime_4 = time.time()

    if (time.time() - startTime_5 > 15):
        try:
            ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ClientSocket.connect((ip_address, 5001))   
            ClientSocket.send(str.encode("============ ROOM 5 DISCONNECTED ============"))
            ClientSocket.close()
        except socket.error as e:
            print(str(e))

        p = Point("Project").field("Room5_DC", "Room Disconnected").time(datetime.datetime.now(datetime.timezone.utc))
        write_client.write(p)
        startTime_5 = time.time()

##################################################