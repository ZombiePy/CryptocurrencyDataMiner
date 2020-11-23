import mysql.connector


class DataPasser:
    mydb = mysql.connector.connect(
        host='localhost',
        user='zombie',
        password='Jw$90kmzq0',
        database='crypto'
    )

    SQL_INSERT = "INSERT INTO crpyto_prices (timestamp, symbol, price_usd) VALUES (%s, %s, %s)"

    def __init__(self):
        self.crypto = {'btc': {},
                       'eth': {},
                       'xrp': {},
                       'ltc': {}}
        self.needed_keys = ['name',
                            'symbol',
                            'cmc_rank',
                            'is_fiat',
                            'price_usd',
                            'percent_change_1h',
                            'percent_change_24h',
                            'percent_change_7d',
                            'timestamp']
        self.my_cursor = self.mydb.cursor()

    def add_message(self, topic, payload):
        print(topic)
        crypto = topic.split('/')[0].lower()
        key = topic.split('/')[1].lower()
        if crypto == 'all':
            self.crypto['btc']['timestamp'] = payload
            self.crypto['eth']['timestamp'] = payload
            self.crypto['xrp']['timestamp'] = payload
            self.crypto['ltc']['timestamp'] = payload
        else:
            self.crypto[crypto][key] = payload
        print("Added value:", payload, "  to ", topic)
        self.check_if_full(crypto)

    def check_if_full(self, crypto):
        existing_keys = self.crypto[crypto].keys()
        send = True
        for needed_key in self.needed_keys:
            if needed_key not in existing_keys:
                print("missing ", needed_key)
                send = False
        if send == True:
            self.sql_insert(crypto)
            self.crypto[crypto] = {}

    def sql_insert(self, crypto):
        insert_values = (self.crypto[crypto]['timestamp'],
                         self.crypto[crypto]['symbol'],
                         self.crypto[crypto]['price_usd'])
        self.my_cursor.execute(self.SQL_INSERT, insert_values)