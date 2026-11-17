# ======= Libraries ======= #
import paho.mqtt.client as mqtt 
import socket
from gpiozero import LED
# ========================= #


# ======= GPIO PIN's ====== #
led_1 = LED(17) 
led_2 = LED(27) 
led_3 = LED(18) 
# ========================= #


MQTT_SERVER = "10.6.1.9" # broker address (IP of raspberry pi)
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("REAL_SENSOR")
    client.subscribe("CONTROLLER_7")        # -> Connect to controller.py (running local)
    client.subscribe("VIRTUAL_SENSOR_7")    # -> Connect to fake_sensor.py (running local) 

def on_message(client, userdata, msg):
    global alarm_state # Define alarm_state as global (so it can change value inter def's)

    if(msg.topic == "CONTROLLER_7"):
        if(msg.payload == b"ON"): # Ensure payload is compared with bytes
            alarm_state = True
        elif(msg.payload == b"OFF"): # Ensure payload is compared with bytes
            alarm_state = False
    elif(msg.topic == "REAL_SENSOR" or msg.topic == "VIRTUAL_SENSOR_7"): 
        if(alarm_state):
            distance = 0
            try:
                distance  = float(msg.payload)
            except:
                led_1.off()     # Make sure that only messages with numbers go through
                led_2.off()
                led_3.off()
            if(distance > 30):
                led_1.off()
                led_2.off()
                led_3.off()
            elif distance >=20:
                led_1.on()
                led_2.off()
                led_3.off()
            elif distance >= 10:
                led_1.on()
                led_2.on()
                led_3.off()
            else:
                led_1.on()
                led_2.on()
                led_3.on()
            print(f"{msg.topic}:{distance}")        # I had this: print(f"Distancia:{distance}") (still works)
                                                    # But with these changes, you know directly from which topic the message comes

        else:                      # Turn off LED's if system is in deactivated mode
            led_1.off()
            led_2.off()
            led_3.off()

alarm_state = False
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()
