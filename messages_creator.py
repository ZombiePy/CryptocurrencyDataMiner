import data_receiver
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

class MessagesCreator:
    """Class that preprocess data for further objects"""

    def __init__(self):
        """Simple initializer"""
        self.data_receiver = data_receiver.DataReceiver()
        self.data_receiver.prepare_session()
        #self.client = mqtt.Client()
        #self.client.connect(host="localhost")
        #self.client.loop_start()

    def get_data(self):
        """Method to get data from API to preprocess"""
        data = self.data_receiver.get_data()
        timestamp = data['status']['timestamp']
        btc = data['data']['1']
        ltc = data['data']['2']
        xrp = data['data']['52']
        eth = data['data']['1027']
        cryptocurrencies = [btc, ltc, xrp, eth]
        return cryptocurrencies, timestamp

    def data_extractor(self, cryptocurrency):
        """Extracting key values from API response"""
        result_dict = {
            'name': cryptocurrency['name'],
            'symbol': cryptocurrency['symbol'],
            'cmc_rank': cryptocurrency['cmc_rank'],
            'is_fiat': cryptocurrency['is_fiat'],
            'prince_USD': cryptocurrency['quote']['USD']['price'],
            'percent_change_1h': cryptocurrency['quote']['USD']['percent_change_1h'],
            'percent_change_24h': cryptocurrency['quote']['USD']['percent_change_24h'],
            'percent_change_7d': cryptocurrency['quote']['USD']['percent_change_7d']
        }
        return result_dict

    def messages_constructor(self, dict):
        """Messages constructor form dictionary"""
        messages = []
        topic = dict['symbol'] + '/'
        for key in dict.keys():
            temp_tuple = (topic + key, dict[key], 0)
            messages.append(temp_tuple)
        return messages

    def publish(self):
        """Method that collects data prepare messages and publish them to mqtt server"""
        data = self.get_data()
        messages = []
        for crypto in data[0]:
             messages_temp = self.messages_constructor(self.data_extractor(crypto))
             for message in messages_temp:
                 messages.append(message)

        messages.append(('all/timestamp', data[1], 1))

        publish.multiple(messages)