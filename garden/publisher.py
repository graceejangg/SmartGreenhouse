from time import sleep
import mqtt.mqttClient as mqtt
import logging
from datetime import datetime
import json
import random




def main():
    client = mqtt.MqttClient("mosquitto", 1883)
    logging.debug("Start")
    value = False
    while(True):
        client.publish("garden/water",json.dumps({"duration": 2, "timestamp": datetime.now().isoformat()}))
        client.publish("garden/lightAct",json.dumps({"id": 2222, "state": int(not value), "timestamp": datetime.now().isoformat()}))

        client.publishSensorData(f"garden/temperature", 1234, "C", 22, datetime.now())
        client.publishSensorData(f"garden/light", 1234, "lux", 750, datetime.now())
        client.publishSensorData(f"garden/moisture", 1234, "", 400, datetime.now())
        client.publishSensorData(f"garden/humidity", 1234, "%", 65, datetime.now())

        sleep(4) 

        client.publishSensorData(f"garden/temperature", 1234, "C", 10, datetime.now())
        client.publishSensorData(f"garden/light", 1234, "lux", 500, datetime.now())
        client.publishSensorData(f"garden/moisture", 1234, "", 200, datetime.now())
        client.publishSensorData(f"garden/humidity", 1234, "%", 40, datetime.now())
        sleep(4)
        client.publishSensorData(f"garden/temperature", 1234, "C", 30, datetime.now())
        client.publishSensorData(f"garden/light", 1234, "lux", 1100, datetime.now())
        client.publishSensorData(f"garden/moisture", 1234, "", 800, datetime.now())
        client.publishSensorData(f"garden/humidity", 1234, "%", 80, datetime.now())
        sleep(4)
    client.disconnect()

if __name__ == '__main__':
    main()