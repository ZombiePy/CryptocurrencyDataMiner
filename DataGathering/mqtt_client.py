import paho.mqtt.client as mqtt
from DataGathering import data_passer
import time


class MqttClient:
    def __init__(self):
        self.client = mqtt.Client("receiver_01")
        self.client.connect('localhost')
        self.client.subscribe("+/+")
        #self.data_passer = data_passer.DataPasser()

    def start_loop(self):
        self.client.loop_start()
        while True:
            time.sleep(20)