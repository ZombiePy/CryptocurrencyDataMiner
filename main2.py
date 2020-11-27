from DataGathering import csv_data_parser


data_passer = csv_data_parser.CsvDataParser('BTC')

def on_message_func(client, userdata, msg):
    print("Received msg")
    data_passer.add_message(msg.topic, msg.payload)


data_passer.run(on_message_func)