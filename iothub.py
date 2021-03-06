import requests
import os
import time
from azure.iot.device.aio import IoTHubDeviceClient
import json
import asyncio

from constants import CONNECTION_STRING

TIMESTAMP = "timestamp"
FAN_COMMAND = "fan_command"
HEAT_COMMAND = "heat_command"
COOL_COMMAND = "cool_command"
THERM_1_TEMP = "therm_1_temp"
THERM_2_TEMP = "therm_2_temp"
HEAT_STPT = "heat_set_point"
COOL_STPT = "cool_set_point"

MESSAGE_DELAY = 5000

device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# sensor_message = json.dumps(TEST_DICT)

def create_and_send_message(client):
    await device_client.connect()
    print('sending message...')
    await device_client.send_message('message')
    print('sent!')
    await device_client.shutdown()


def receive_message(message):
    print("Message received:")

    # print data from both system and application (custom) properties
    for property in vars(message).items():
        print ("    {}".format(property))



    

def main():
    # Attempt to attach the message handler
    try:
        # Attach the handler to the client
        client.on_message_received = receive_message

    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging device sample stopped")


    while True:
        create_and_send_message(device_client)
        time.sleep(MESSAGE_DELAY)

   



