import requests
import json
import os

class DataReceiver:
    """Class for collecting data from API (CoinMarketCap API)"""
    URL_GET_DATA = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

    URL_CHECK_TOKENS = 'https://pro-api.coinmarketcap.com/v1/key/info'

    AUTHENTICATION_PATH = os.path.join(os.getcwd(), 'Data', 'authentication.txt')

    def __init__(self, cryptocurrencies="bitcoin,ethereum,litecoin,xrp", convert='USD'):
        """
        Default initializer to get data about cryptocurrencies, default bitcoin, ethereum, litecoin, xrp
        :parameter convert - currency that API convert prices
        :parameter cryptocurrencies - string contains cryptocurrencies separated by comma, DateReceiver will download
        data about this currencies
        """
        self.parameters = {
            'slug': cryptocurrencies,
            'convert': convert
            }
        with open(self.AUTHENTICATION_PATH) as json_file:
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
            print('Fail to connect with API')

    def request_counter(self, return_type='left'):
        """
        Method that check if program has API requests left or how many of them used
        :parameter return_type - one of ['left', 'used'] define what user will expects
        :rtype: int
        """
        try:
            response = self.session.get(self.URL_CHECK_TOKENS)
            data = json.loads(response.text)
            return data['data']['usage']['current_day']['credits_' + return_type]
        except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects):
            print('Fail to connect with API')
        except KeyError:
            print("return_type must be defined as 'left' or 'used")