from DataVisualization.candle_stick import plot_candle_stick
from DataVisualization.line_plot import plot_line
from Utilities.functions_dataframe import get_one_date_dataframe, get_daily_dataframe
import Utilities.functions as func
from tabulate import tabulate
import os
import yagmail


cryptos = ['BTC', 'LTC', 'ETH', 'XRP']
last_day = func.get_last_date()
#for crypto in cryptos:
#    df_crypto = get_one_date_dataframe(crypto, last_day)
#    plot_line(df_crypto, crypto)
os.system('python ./DataVisualization/candle_stick.py')
os.system('python ./DataVisualization/line_plot.py')

table = [['Low', 'High', 'Open', 'Close', 'Date']]
#for crypto in cryptos:
    #df_daily = get_daily_dataframe(crypto)
    #plot_candle_stick(df_daily, crypto)
    #table.append(list(df_daily(df_daily['Date'] == last_day)))

table_tabulate = tabulate(tabular_data=table, headers="firstrow")

email_form_path = os.path.join(os.getcwd(), 'Data', 'Input', 'email_form.txt')
with open(email_form_path, 'r') as email_file:
    email_form = email_file.read()

email_form.replace('space', table_tabulate)
plots_path = func.get_output_path('Plots')

email_form.format(name='Tymoteusz',
                  date=last_day,
                  btc_line_chart=func.get_plot_path(last_day, 'line_chart', 'btc'),
                  btc_candle=func.get_plot_path(last_day, 'candle_stick', 'btc'),
                  eth_line_chart=func.get_plot_path(last_day, 'line_chart', 'eth'),
                  eth_candle=func.get_plot_path(last_day, 'candle_stick', 'eth'),
                  xrp_line_chart=func.get_plot_path(last_day, 'line_chart', 'xrp'),
                  xrp_candle=func.get_plot_path(last_day, 'candle_stick', 'xrp'),
                  ltc_line_chart=func.get_plot_path(last_day, 'line_chart', 'ltc'),
                  ltc_candle=func.get_plot_path(last_day, 'candle_stick', 'ltc')
                  )

try:
    #initializing the server connection
    credentials_path = os.path.join(os.getcwd(), 'Data', 'Input', 'credentials.json')
    yag = yagmail.SMTP(user='zombie.crypto.project@gmail.com', password='')
    #sending the email
    yag.send(to='tdobrzanski97@gmail.com', subject='Daily cryptocurrencies update', contents='Hi')
    print("Email sent successfully")
except:
    print("Error, email was not sent")


