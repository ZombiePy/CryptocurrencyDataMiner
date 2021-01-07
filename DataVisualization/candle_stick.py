import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from Utilities.functions_dataframe import get_daily_dataframe
import Utilities.functions as func
import os

def plot_candle_stick(df, crypto):
    df = df[['Open', 'High', 'Low', 'Close']]
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].map(mdates.date2num)
    date = func.get_last_date()

    ax = plt.subplot()
    candlestick_ohlc(ax, df.values, width=1, colorup='g', colordown='r')
    ax.set_axisbelow(True)
    ax.set_title(crypto + ' Price to ' + date, color='white')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis_date()
    ax.grid(True)
    plt.xticks(rotation=45)
    #plt.tight_layout()
    plots_path = func.get_output_path('Plots')
    fig_name = crypto.upper() + '_candle_stick_' + date + '.png'
    absolute_path = os.path.join(plots_path, fig_name)
    plt.savefig(absolute_path, format='png', dpi=800)
    #plt.show()
    return absolute_path


if __name__ == "__main__":
    cryptos = ['BTC', 'LTC', 'ETH', 'XRP']
    for crypto in cryptos:
        df_crypto = get_daily_dataframe(crypto)
        plot_candle_stick(df_crypto, crypto)
