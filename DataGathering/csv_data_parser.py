from DataGathering.mqtt_client import MqttClient
import pandas as pd
import time


class CsvDataParser:

    def __init__(self, crypto):
        self.crypto = crypto
        self.data_frame = pd.DataFrame({'timestamp': [], 'symbol': [], 'price_usd': []})
        self.mqtt_client = MqttClient(crypto)
        self.temp_value_holder = {}

    def add_message(self, topic, payload):
        key = topic.split('/')[1].lower()
        self.temp_value_holder[key] = [payload.decode('utf-8')]
        #print("Added value:", payload, "  to ", topic)
        self.check_if_full()

    def check_if_full(self):
        keys = list(self.temp_value_holder.keys())
        values = list(self.temp_value_holder.values())
        if keys == ['timestamp', 'symbol', 'price_usd']:
            print('Full')
            temp_data_frame = pd.DataFrame(self.temp_value_holder)
            #print(temp_data_frame)
            self.data_frame = self.data_frame.append(temp_data_frame)
            self.temp_value_holder = {}
            print(self.data_frame)
        else:
            print("Missing")

    def run(self, func):
        self.mqtt_client.set_on_message(func)
        self.mqtt_client.start_loop()
        while True:
            time.sleep(20)
            self.mqtt_client.client.loop()
            #self.check_if_full()