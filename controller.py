from w1thermsensor import W1ThermSensor, Unit, Sensor
import RPi.GPIO as gpio
import time
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

from constants import CONNECTION_STRING, DEVICE_ID

internal_temp_sensor = '0000068af58a'
external_temp_sensor = '00000687d2d8'
relay_2 = 11
relay_1_side_2 = 13
#LOW is one HIGH is off
fan = 15
thermometer = 7

HEATING_SET_POINT = 78.0
COOLING_SET_POINT = 82.0
DELAY = 1000

gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(3, gpio.OUT)
gpio.setup(5, gpio.OUT)
gpio.setup(thermometer, gpio.IN)

class Controller():

    def __init__(self, hpt, cpt, delay):
        self.heating_set_point = hpt
        self.cooling_set_point = cpt
        self.delay = delay

    def run_forever(self):
        # get temperature reading
        sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=internal_temp_sensor)
        sensor_temp = sensor.get_temperature(Unit.DEGREES_F)
        
        # is temperature in range?
        if sensor_temp <= COOLING_SET_POINT and sensor_temp >= HEATING_SET_POINT:
            # turn fan off if on
            self.fanoff()
            # turn off heating/cooling
            self.poweroff()
        # no
        else:
            # turn fan on
            self.fanon()

            # is temperature greater than cooling setpoint? then cool
            if sensor[1] > COOLING_SET_POINT:
                self.cool()

            # else heat
            else:
                self.heat()

    def heat(self):
        # turn on heat
        gpio.output(relay_2, gpio.LOW)
        gpio.output(relay_1_side_2, gpio.LOW)
        #turn on red light
        gpio.output(3, gpio.LOW)

    def cool(self):
        gpio.output(relay_2, gpio.HIGH)
        gpio.output(relay_1_side_2, gpio.LOW)
        gpio.output(5, gpio.LOW)

    def poweroff(self):
        gpio.output(relay_2, gpio.HIGH)
        gpio.output(relay_1_side_2, gpio.HIGH)
        gpio.output(3, gpio.HIGH)
        gpio.output(5, gpio.HIGH)

    def fanon(self):
        gpio.output(fan, gpio.LOW)

    def fanoff(self):
        gpio.output(fan, gpio.HIGH)
        
    
    

async def main():
#def main():
    my_controller = Controller(0, 0, 0)
    my_controller.fanon()
    my_controller.heat()

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await client.connect()
    for i in range(100):
        sensor_bean = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id= internal_temp_sensor)
        sensor_fan = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id= external_temp_sensor)
        sensor_temp_bean = sensor_bean.get_temperature(Unit.DEGREES_F)
        sensor_temp_fan = sensor_fan.get_temperature(Unit.DEGREES_F)
        asyncio.sleep(5)
        print(sensor_temp_bean)
        print(sensor_temp_fan)
        print(CONNECTION_STRING)
        
        await client.send_message("bean temp: {} fan temp: {}".format(str(sensor_temp_bean), str(sensor_temp_fan)))
        #await client.disconnect()
#    except err:
 #       print('Error', err)

    my_controller.poweroff()
    my_controller.fanoff()


if __name__ == "__main__":
    asyncio.run(main())
