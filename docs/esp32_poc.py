import network
import ujson
from machine import Pin
from time import sleep
from umqtt.simple import MQTTClient

# Sensor Parameters
SENSOR_ID = "iot_device_001"

# MQTT Server Parameters
MQTT_CLIENT_ID = "iot-luizth"
MQTT_BROKER    = "mqtt-dashboard.com"
MQTT_USER      = "luizth"
MQTT_PASSWORD  = "pass"
MQTT_TOPIC     = "iot/motion"

# WIFI Connection
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    sleep(0.1)
print(" Connected!")

# MQTT Server connection
print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected!")

# ---

motion = False
def handle(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin


pir = Pin(14, Pin.IN)
pir.irq(trigger=Pin.IRQ_RISING,handler=handle)

while True:

    """
    if motion:  # print('Motion detected! Interrupt caused by:',interrupt_pin)
        message = ujson.dumps({
            "sensor_id": SENSOR_ID,
            "motion_detected": motion
        })
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        # sleep(5)  # sample from distribution
        motion = False  # print('Motion Stopped!')
    """

    message = ujson.dumps({
        "sensor_id": SENSOR_ID,
        "motion_detected": motion
    })
    print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
    client.publish(MQTT_TOPIC, message)

    if motion:
        motion = False

    sleep(5)  # reads every 5 sec
