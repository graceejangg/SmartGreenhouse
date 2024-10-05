from time import sleep
import mqtt.mqttClient as mqtt
import logging
from datetime import datetime





def main():
    client = mqtt.MqttClient("mosquitto", 1883)
    logging.debug("Start")
    client.subscribe("garden/+")
    logging.debug("Subscribed")
    value = 0
    while(True):
        continue
    client.disconnect()

if __name__ == '__main__':
    main()