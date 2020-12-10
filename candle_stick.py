import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import os
import re


def prepare_dataframe(crypto='BTC'):
    path = os.path.join(os.getcwd(), 'running', 'Output')

    file_names = get_list_of_file(path, crypto)

    df_from_files = pd.DataFrame(columns=['timestamp', 'symbol', 'price_usd'])
    for file_name in file_names:
        df = pd.read_csv(os.path.join(path, file_name), index_col=0)
        df_from_files = df_from_files.append(df, ignore_index=True)
    list_of_dates = list(df_from_files['timestamp'].values)
    set_of_dates = set()
    for date in list_of_dates:
        set_of_dates.add(date.split()[0])
    df_from_files.drop_duplicates()

    dict = {'Low': [],
            'High': [],
            'Open': [],
            'Close': [],
            'Date': []}
    dates = []
    for date in set_of_dates:
        df = df_from_files['timestamp'].map(lambda x: bool(re.search(date, x)))
        df_date = df_from_files[df]

        dict['Low'].append(min(df_date['price_usd']))
        dict['High'].append(max(df_date['price_usd']))
        dict['Open'].append(df_date.sort_values(by=['timestamp'], ignore_index=True).iloc[0]['price_usd'])
        dict['Close'].append(df_date.sort_values(by=['timestamp'], ignore_index=True).iloc[-1]['price_usd'])
        dict['Date'].append(date)
    index = pd.Index(dict['Date'], name='Date')
    df_to_plot = pd.DataFrame(dict, index=index)
    plot_candle_stick(df_to_plot, crypto)


def get_list_of_file(path, pattern):
    list_of_files = os.listdir(path)
    file_names = []
    for file_name in list_of_files:
        if re.search(pattern, file_name):
            file_names.append(file_name)
    return file_names


def plot_candle_stick(df, crypto):
    df = df[['Open', 'High', 'Low', 'Close']]
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].map(mdates.date2num)

    ax = plt.subplot()
    candlestick_ohlc(ax, df.values, width=1, colorup='g', colordown='r')
    ax.set_axisbelow(True)
    ax.set_title(crypto + ' Price', color='white')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis_date()
    ax.grid(True)
    plt.show()

if __name__ == "__main__":
    prepare_dataframe('BTC')
    prepare_dataframe('ETH')
    prepare_dataframe("LTC")
    prepare_dataframe('XRP')