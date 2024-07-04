import os
import json
import mysql.connector
import paho.mqtt.client as mqtt
from dataclasses import dataclass

from setup import wait_for_db

# MySQL database credentials
DB_HOST = os.getenv('DB_HOST')  # # 'localhost'
DB_USER = os.getenv('DB_USER')  # 'iot_gb'
DB_PASSWORD = os.getenv('DB_PASSWORD')  # 'password'
DB_NAME = os.getenv('DB_NAME')  # 'iot_sensor_data'

# MQTT broker credentials
MQTT_BROKER = os.getenv('MQTT_BROKER')  # 'mqtt-dashboard.com'
MQTT_PORT = int( os.getenv('MQTT_PORT') )  # 1883
MQTT_TOPIC = os.getenv('MQTT_TOPIC')  # 'iot/motion'


@dataclass
class Message:
    sensor_id: str
    motion_detected: bool
    timestamp: str = None


# MySQL connection setup
def connect_to_mysql():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)


# MQTT on_message callback
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    try:
        data = json.loads( msg.payload.decode() )
        Message(**data)
    except Exception as e:
        print(f'error parsing message {e}, discarding...')
        return

    save_message_to_mysql(data)


# Save message to MySQL table
def save_message_to_mysql(message: dict):
    cnx = connect_to_mysql()
    cursor = cnx.cursor()

    if "timestamp" in message:
        add_message = ("INSERT INTO motion "
                    "(sensor_id, motion_detected, timestamp) "
                    "VALUES (%(sensor_id)s, %(motion_detected)s, %(timestamp)s)")
    else:
        add_message = ("INSERT INTO motion "
                    "(sensor_id, motion_detected) "
                    "VALUES (%(sensor_id)s, %(motion_detected)s)")
    cursor.execute(add_message, message)
    cnx.commit()
    cursor.close()
    cnx.close()


# Main function to set up MQTT client and start loop
def main():
    wait_for_db()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
