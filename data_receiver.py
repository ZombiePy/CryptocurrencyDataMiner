import requests
import json

class DataReceiver:
    """Class for collecting data from API (CoinMarketCap API)"""
    URL_GET_DATA = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    URL_CHECK_TOKENS = 'https://pro-api.coinmarketcap.com/v1/key/info'

    def __init__(self, cryptocurrencies="bitcoin,ethereum,litecoin,xrp"):
        """Default initializer to get data about cryptocurrencies, default bitcoin, ethereum, litecoin, xrp"""
        self.parameters = {
            'slug': cryptocurrencies,
            'convert': 'USD'
            }
        with open('Data\\authentication.txt') as json_file:
            self.headers = json.load(json_file)

    def prepare_session(self):
        """Prepare session for requests"""
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_data(self):
        """Method to get data from API"""
        try:
            response = self.session.get(self.URL_GET_DATA, params=self.parameters)
            data = json.loads(response.text)
            return data
        except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)

    def request_left(self, return_type='left'):
        """Method that check if program has API requests left or how many of them used"""
        try:
            response = self.session.get(self.URL_CHECK_TOKENS)
            data = json.loads(response.text)
        except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
        try:
            return data['data']['usage']['current_day']['credits_' + return_type]
        except KeyError:
            raise KeyError("return_type must be defined as 'left' or 'used")