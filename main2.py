from DataGathering import mqtt_client
from DataGathering import data_passer
import time

client = mqtt_client.MqttClient()
data_passer = data_passer.DataPasser()

def on_message_func(client, userdata, msg):
    print("Received msg")
    data_passer.add_message(msg.topic, msg.payload)


client.client.on_message = on_message_func
client.start_loop()
