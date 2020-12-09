from DataGathering import csv_data_parser
import os


output_file_path = os.getcwd()
data_passer = csv_data_parser.CsvDataParser('LTC', 'LTC1', output_file_path)



def on_message_func(client, userdata, msg):
    print("Received msg")
    data_passer.add_message(msg.topic, msg.payload)


data_passer.run(on_message_func)