from time import sleep
import json
import logging
import time
import mqtt.mqttClient as mqtt
from datetime import datetime
from sensors.sensors import  Temperature, Humidity, Moisture, Light
from sensors.grovepi import digitalWrite
from sensors.grove_rgb_lcd import setRGB, setText_norefresh, textCommand

led_water = 4
relay_water = 5
led_light = 2

sensorReadInterval = 10

mqtt_hostname = "192.168.78.10"
mqtt_port = 1883
wateringDuration = 0
lightState = 0
textList = {}


def readSensors(client):
    global textList
    sensorList = [Temperature(),Humidity(),Light(),Moisture()]

    for sensor in sensorList:
        logging.debug(f"Read sensor {sensor.getSensorType()}")
        client.publishSensorData(f"garden/{sensor.getSensorType()}", sensor.getId(),sensor.getMeasuringUnit(),sensor.getValue(),datetime.now())
        textList[sensor.getSensorType()] = (f"{(sensor.getSensorType()+':').ljust(16)}\n{sensor.getValue()} {sensor.getMeasuringUnit()}")



def listener(topic, payload):
    global wateringDuration, lightState
    try:
        if topic == "garden/water":
            logging.debug(f"Water for {json.loads(payload)}")
            wateringDuration += int(json.loads(payload)["duration"])

        elif topic == "garden/lightAct":
            logging.debug(f"Light for {json.loads(payload)}")
            lightState = int(json.loads(payload)["state"])
        else:
            logging.debug(f"Unknown topic {topic}")
    except:
        logging.error(f"Topic: {topic} Error parsing payload {payload}")

def testGrovePi():
    digitalWrite(led_water,1)
    digitalWrite(led_light,1)
    sleep(1)

    digitalWrite(led_water,0)
    digitalWrite(led_light,0)

    setText_norefresh("Starting...")


def main():
    global wateringDuration, lightState, textList
    setRGB(0,255,0)
    testGrovePi()

    client = mqtt.MqttClient(mqtt_hostname, mqtt_port)
    logging.debug("Start")

    sleep(2)

    client.callback = listener
    client.subscribe("garden/water")
    client.subscribe("garden/lightAct")

    lastTimeRead = 0
    iterator = 0
    while True:
        if time.time() - lastTimeRead > sensorReadInterval:
            readSensors(client)
            lastTimeRead = time.time()
        
        if wateringDuration > 0:
            digitalWrite(led_water,1)
            digitalWrite(relay_water,1)
            logging.debug(f"Watering for {wateringDuration} seconds")
            wateringDuration -= 1
        else:
            digitalWrite(led_water,0)
            digitalWrite(relay_water,0)

        if lightState > 0:
            digitalWrite(led_light,1)
        else:
            digitalWrite(led_light,0)

        
            setText_norefresh(textList[list(textList.keys())[iterator]])
            iterator = (iterator + 1) % len(textList.keys())
        sleep(1)

    client.disconnect()

if __name__ == '__main__':
    main()