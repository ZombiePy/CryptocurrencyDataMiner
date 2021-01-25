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
        """Setting on_connect function in client
        :parameter func - function that will be set as on_connect"""
        self.client.on_connect = func

    def set_on_message(self, func):
        """Setting on_message function in client
        :parameter func - function that will be set as on_message"""
        self.client.on_message = func

    def loop_start(self):
        """Starting loop, which will wait for msgs"""
        self.client.loop_start()
