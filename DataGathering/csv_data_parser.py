from DataGathering.mqtt_client import MqttClient
import pandas as pd
import time
from pathlib import Path
import os


def on_connect(client, userdata, flags, rc):
    print("Connected")


class CsvDataParser:

    def __init__(self, crypto, host_name):
        self.crypto = crypto
        self.row_list = []
        self.mqtt_client = MqttClient(crypto, host_name)
        self.host_name = host_name
        self.temp_value_holder = {}
        self.current_time = (0, 0, 0)

    def add_message(self, topic, payload):
        key = topic.split('/')[1].lower()
        self.temp_value_holder[key] = payload.decode('utf-8')

    def check_if_full(self):
        keys = list(self.temp_value_holder.keys())
        if keys == ['timestamp', 'symbol', 'price_usd']:
            print('Full')
            self.row_list.append(self.temp_value_holder)
            timestamp = self.temp_value_holder['timestamp']
            date, current_time = self.timestamp_processing(timestamp, True)
            self.to_csv(date)
            if current_time[0] >= 23 and current_time[1] >= 55:
                self.day_close()
            self.temp_value_holder = {}
            return True
        else:
            return False

    def run(self, func):
        self.mqtt_client.set_on_connect(on_connect)
        self.mqtt_client.set_on_message(func)
        self.mqtt_client.loop_start()
        while True:
            time.sleep(20)
            self.check_if_full()
            self.mqtt_client.client.loop()

    def timestamp_processing(self, timestamp, to_print=False):
        date, current_time = timestamp.split()
        hour, minute, sec = current_time.split(':')
        hour, minute, sec = int(hour), int(minute), int(sec)
        current_time = (hour, minute, sec)
        self.current_time = current_time
        if to_print:
            print(self.current_time)
        return date, current_time

    def day_close(self):
        self.mqtt_client.client.loop_stop()
        self.mqtt_client.client.reinitialise(self.host_name, True)
        time.sleep(5)
        self.mqtt_client.loop_start()
        self.row_list = []
        return True

    def to_csv(self, date):
        print("Saving Data")
        file_name = self.crypto + '_' + date + '.csv'
        absolute_path = 'D:\Temp\JiBADProject\Data\Output\\' + self.crypto + '_' + date + '.csv'
        data_frame = pd.DataFrame(self.row_list)
        #data_frame.to_csv('D:\Temp\JiBADProject\Data\Output\\' + self.crypto + '_' + date + '.csv')
        if not os.path.isfile(absolute_path):
            data_frame.to_csv(absolute_path)
        else:  # else it exists so append without writing the header
            data_frame.to_csv(absolute_path, mode='a', header=False)
            self.row_list = []


