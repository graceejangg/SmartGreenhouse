import paho.mqtt.client as mqtt
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Log to the console
        # Add additional handlers or specify a file to log to
    ]
)


class MqttClient:
    def __init__(self, fqdn, port) -> None:
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.topics = []
        self.callback = None

        self.mqttc.connect(fqdn, port, 60)
        self.mqttc.loop_start()

    def __del__(self):
        self.mqttc.loop_stop()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        logging.debug(f"Connected with result code {reason_code}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic in self.topics:
            self.mqttc.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        try:
            logging.debug(f"{msg.topic} {str(json.loads(msg.payload))}")
            if self.callback:
                self.callback(msg.topic, msg.payload)
        except json.decoder.JSONDecodeError: 
            logging.error(f"JSON parsing error wiht payload: {msg.payload}")



    def publish(self, topic, message):
        self.mqttc.publish(topic, message)
    
    def subscribe(self, topic):
        self.topics.append(topic)
        self.mqttc.subscribe(topic)

    def disconnect(self):
        self.mqttc.disconnect()

    def publishSensorData(self, topic, id, unit, value, timestamp):
        logging.debug(f'topic: {topic} data: {json.dumps({"id":id,"unit":unit,"value":value,"timestamp":timestamp.isoformat()})}')
        self.publish(topic, json.dumps({"id":id,"unit":unit,"value":value,"timestamp":timestamp.isoformat()}))
