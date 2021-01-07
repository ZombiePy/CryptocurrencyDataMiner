import threading
import os
import sys
from Utilities.functions import mqtt_receiving

cryptos = ['BTC', 'LTC', 'ETH', 'XRP']
output_file_path = os.path.join(os.getcwd(), 'Data', 'Output', 'Prices')


threads = list()
for crypto in cryptos:
    thread = threading.Thread(target=mqtt_receiving, args=(crypto, output_file_path))
    threads.append(thread)
    thread.start()

for _, thread in enumerate(threads):
    thread.join()

sys.exit()
