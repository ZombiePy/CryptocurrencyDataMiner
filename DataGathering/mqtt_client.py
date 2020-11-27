import paho.mqtt.client as mqtt
import time


class MqttClient:
    def __init__(self, crypto):
        self.client = mqtt.Client("receiver_01")
        self.client.connect('localhost')
        self.client.subscribe(crypto + "/price_USD", 1)
        self.client.subscribe(crypto + "/symbol", 1)
        self.client.subscribe("all/+", 1)

    def set_on_message(self, func):
        self.client.on_message = func

    def start_loop(self):
        self.client.loop_start()
