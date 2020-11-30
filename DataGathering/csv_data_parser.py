from DataGathering.mqtt_client import MqttClient
import pandas as pd
import time


class CsvDataParser:

    def __init__(self, crypto):
        self.crypto = crypto
        self.row_list = []
        self.mqtt_client = MqttClient(crypto)
        self.temp_value_holder = {}

    def add_message(self, topic, payload):
        key = topic.split('/')[1].lower()
        self.temp_value_holder[key] = payload.decode('utf-8')
        #print("Added value:", payload, "  to ", topic)
        #self.check_if_full()

    def check_if_full(self):
        keys = list(self.temp_value_holder.keys())
        if keys == ['timestamp', 'symbol', 'price_usd']:
            print('Full')
            self.row_list.append(self.temp_value_holder)
            timestamp = self.temp_value_holder['timestamp']
            date, current_time = timestamp.split()
            hour, minute, sec = current_time.split(':')
            hour, minute, sec = int(hour), int(minute), int(sec)
            print(hour, minute, hour>=23, minute>=55)
            if hour >= 23 and minute >= 55:
                self.day_close(date)
            self.temp_value_holder = {}

    def run(self, func):
        self.mqtt_client.set_on_message(func)
        self.mqtt_client.start_loop()
        while True:
            time.sleep(5)
            self.mqtt_client.client.loop()
            self.check_if_full()

    def day_close(self, date):
        print("Closing Day")
        data_frame = pd.DataFrame(self.row_list)
        data_frame.to_csv('D:\Temp\JiBADProject\Data\Output\\' + date + '.csv')
        self.row_list = []
        print('Done')
