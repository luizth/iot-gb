import os
import json
import time
import numpy as np
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta


# Simulation parameters
config = json.load(open('config.json'))

DAYS_TO_SIMULATE = config['DAYS_TO_SIMULATE']
READ_INTERVAL_SECONDS = config['READ_INTERVAL_SECONDS']
MOTION_PROBABILITY = config['MOTION_PROBABILITY']
SUSPICIOUS_PROBABILITY = config['SUSPICIOUS_PROBABILITY']
OFFHOURS_PROBABILITY = config['OFFHOURS_PROBABILITY']
NORMAL_DURATION_MINUTES = config['NORMAL_DURATION_MINUTES']
SUSPICIOUS_DURATION_MINUTES = config['SUSPICIOUS_DURATION_MINUTES']

# MQTT broker details
MQTT_BROKER = os.getenv('MQTT_BROKER')  # 'mqtt-dashboard.com'
MQTT_PORT = int( os.getenv('MQTT_PORT') )  # 1883
MQTT_TOPIC = os.getenv('MQTT_TOPIC')  # 'iot/motion'

# Sensor ID
SENSOR_ID = os.getenv('SENSOR_ID')

# MQTT client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Motion duration count
motion_count = 0

def simulate_motion(duration_minutes):
    global motion_count
    motion_count = int((duration_minutes * 60) / READ_INTERVAL_SECONDS)

def publish_sensor_data():
    global motion_count

    current_time = datetime.now().replace(hour=0, minute=0, second=0)
    end_time = current_time + timedelta(days=DAYS_TO_SIMULATE)

    workinghours_start = current_time.replace(hour=9)
    workinghours_end = current_time.replace(hour=22)

    while current_time < end_time:
        motion_detected = motion_count > 0

        if motion_detected:
            motion_count -= 1
        else:

            if (current_time > workinghours_start and current_time < workinghours_end) or np.random.rand() < OFFHOURS_PROBABILITY:
                if np.random.rand() < MOTION_PROBABILITY:
                    if np.random.rand() < SUSPICIOUS_PROBABILITY:
                        duration_minutes = SUSPICIOUS_DURATION_MINUTES
                    else:
                        duration_minutes = np.random.uniform(*NORMAL_DURATION_MINUTES)

                    simulate_motion(duration_minutes)

        sensor_data = {
            "sensor_id": SENSOR_ID,
            "motion_detected": motion_detected,
            "timestamp": current_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

        client.publish(MQTT_TOPIC, json.dumps(sensor_data))
        print(f"Published: {sensor_data}")

        current_time += timedelta(seconds=READ_INTERVAL_SECONDS)
        time.sleep(0.1)

def main():
    client.loop_start()
    publish_sensor_data()
    client.loop_stop()

if __name__ == "__main__":
    main()
