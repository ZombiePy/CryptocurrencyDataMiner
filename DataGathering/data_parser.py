class DataParser:
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



