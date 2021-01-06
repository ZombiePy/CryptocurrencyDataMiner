from DataGathering import csv_data_parser
import os
import sys


output_file_path = os.getcwd()
data_passer = csv_data_parser.CsvDataParser('XRP', 'XRP1', output_file_path)



def on_message_func(client, userdata, msg):
    print("Received msg")
    data_passer.add_message(msg.topic, msg.payload)


data_passer.run(on_message_func)

sys.exit()