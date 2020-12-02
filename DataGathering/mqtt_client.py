import paho.mqtt.client as mqtt
import time


class MqttClient:
    def __init__(self, crypto, host_name):
        self.client = mqtt.Client(host_name, True)
        self.client.connect('localhost')
        self.client.subscribe(crypto + "/price_USD", 2)
        self.client.subscribe(crypto + "/symbol", 2)
        self.client.subscribe("all/+", 2)

    def set_on_connect(self, func):
        self.client.on_connect = func

    def set_on_message(self, func):
        self.client.on_message = func

    def loop_start(self):
        self.client.loop_start()
