from time import sleep
import time
import uuid
import random
import logging
import math
from sensors.grovepi import dht, analogRead

dht_sensor_port = 8 # connect the DHt sensor to port 8
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor
moisture_analog_port = 0
light_analog_port = 1

class Sensor:
    def __init__(self, sensorType, measuringUnit) -> None:
        self.id = uuid.uuid4()
        self.type = sensorType
        self.measuringUnit = measuringUnit
        self.lastRead = 0


    def getSensorType(self):
        return self.type

    def getId(self):
        return str(self.id)
    
    def getMeasuringUnit(self):
        return self.measuringUnit
    
    def getValue(self):
        pass

class Temperature(Sensor):

    
    def __init__(self) -> None:
        super(Temperature,self).__init__("temperature","°C")
        self.value = 0.0

    def getValue(self):
        if time.time() - self.lastRead > 5:
            [ temp,hum ] = [float("NaN"), float("NaN")]

            while math.isnan(temp) or math.isnan(temp):
                [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
                logging.debug(f"Values read temp: {temp} humidity: {hum}")

            self.lastRead = time.time()
            self.value = temp

        return self.value

class Humidity(Sensor):


    def __init__(self) -> None:
        super(Humidity,self).__init__("humidity","%")
        self.value = 0.0


    def getValue(self):
        if time.time() - self.lastRead > 5:
            [ temp,hum ] = [float("NaN"), float("NaN")]

            while math.isnan(temp) or math.isnan(temp):
                [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
                logging.debug(f"Values read temp: {temp} humidity: {hum}")

            self.lastRead = time.time()            
            self.value = hum

        return self.value

class Moisture(Sensor):
    def __init__(self) -> None:
        super(Moisture,self).__init__("moisture","")
        self.value = 0.0

    def getValue(self):
        if time.time() - self.lastRead > 5:
            self.lastRead = time.time()            
            self.value = analogRead(moisture_analog_port)
            logging.debug(f"Value read: {self.value}")

        return self.value

class Light(Sensor):
    def __init__(self) -> None:
        super(Light,self).__init__("light","")
        self.value = 0.0
        self.lastRead = 0

    def getValue(self):
        if time.time() - self.lastRead > 5:
            self.lastRead = time.time()            
            self.value = analogRead(light_analog_port)
            logging.debug(f"Value read: {self.value}")

        return self.value

class Co2(Sensor):
    def __init__(self) -> None:
        super(Co2,self).__init__("co2","ppm")
        self.value = 0.0

    def getValue(self):
        return self.value + random.uniform(1.0, 221.9)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Started Sensors")

    while True:
        sensorList = [Humidity(),Light(),Temperature(),Moisture()]

        for sensor in sensorList:
            logging.debug(f"{sensor.getSensorType()} read = {sensor.getValue()}")
