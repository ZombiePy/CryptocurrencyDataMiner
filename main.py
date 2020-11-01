import messages_creator
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt

mqttc = mqtt.Client()
mqttc.connect(host="localhost")
mqttc.loop_start()
test = messages_creator.MessagesCreator()

test.publish()


mqttc.subscribe("+/+")

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

mqttc.on_message = on_message_print

