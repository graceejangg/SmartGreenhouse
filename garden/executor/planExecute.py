
from datetime import datetime
import json
import logging
import telebot


class PlanExecutor:
    
    def __init__(self, mqttClient) -> None:
        self.mqttClient = mqttClient
        self.teleBot = telebot.TeleBot("7209509678:AAFFsblFi0flHwv4ooyEARrpkbpiwu-2we0")	
        
   
    def decreaseTemperature(self):
        logging.debug("Inform User to decrease temperature")
        self.teleBot.send_message(499218695, "High temperature in the greenhouse. Open windows and close lids to decrease temperature.")
    
    def increaseTemperature(self):
        logging.debug("Inform User to increase temperature")
        self.teleBot.send_message(499218695, "It's getting cold in the greenhouse. Check if windows are closed and take measures to increase temperature.")

    def decreaseMoisture(self):
        logging.debug("Don't water the plants")

    def increaseMoisture(self):
        logging.debug("Start Watering the plants")
        self.mqttClient.publish("garden/water",json.dumps({"duration": 2, "timestamp": datetime.now().isoformat()}))

    def decreaseHumidity(self):
        logging.debug("Inform User to open windows to decrease humidity")
        self.teleBot.send_message(499218695, "High air humidity in the greenhouse. Open windows to decrease humidity.")


    def increaseHumidity(self):
        logging.debug("Inform User to close windows to increase humidity")
        self.teleBot.send_message(499218695, "Low air humidity in the greenhouse. Close windows.")
    
    def turnOnLight(self):
        logging.debug("Turning on light")
        self.mqttClient.publish("garden/lightAct",json.dumps({"state": 1, "timestamp": datetime.now().isoformat()}))

    def turnOffLight(self):
        logging.debug("Turning off light")
        self.mqttClient.publish("garden/lightAct",json.dumps({"state": 0, "timestamp": datetime.now().isoformat()}))
    
    def parseAction(self, actionString):
        logging.debug(f"Parsing action: {actionString}")
        actionString = actionString.replace("(", "").replace(")", "")

        action = actionString.split(" ")
        logging.debug(f"Action: {action}")
        if action[0] == "decrease_":
            logging.debug(f"decrease {action[1]}")
            if action[1] == "temperature":
                self.decreaseTemperature()
            elif action[1] == "moisture":
                self.decreaseMoisture()
            elif action[1] == "humidity":
                self.decreaseHumidity()
            elif action[1] == "light":
                self.turnOffLight()
        elif action[0] == "increase_":
            logging.debug(f"increase {action[1]}")
            if action[1] == "temperature":
                self.increaseTemperature()
            elif action[1] == "moisture":
                self.increaseMoisture()
            elif action[1] == "humidity":
                self.increaseHumidity()
            elif action[1] == "light":
                self.turnOnLight()
        elif action[0] == "achieve-dummy-goal":
            logging.debug(f"dummy")
        else:
            logging.warning(f"Unknown action: {action}")
    def executePlan(self, plan):
        for action in plan:
            print(action.strip())
            self.parseAction(action.strip())


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    plan = "(decrease-value temperaturesensor)\n(decrease-value moisturesensor)\n(decrease-value lightsensor)\n(decrease-value humiditysensor)\n(achieve-dummy-goal )"
    for action in plan.split("\n"):
        if action.strip()[0] == '(':
            parseAction(action.strip())
