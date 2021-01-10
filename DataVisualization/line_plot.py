import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Utilities.functions_dataframe import get_one_date_dataframe
import Utilities.functions as func
import os


def plot_line(df, crypto):
    df['timestamp'] = list(date.split()[1] for date in df['timestamp'])
    ax = plt.subplot()
    ax.plot_date(df['timestamp'], df['price_usd'], xdate=True, fmt='-w')
    plt.xticks(df['timestamp'].iloc[::6], rotation=90)
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.grid(True)
    date = func.get_last_date()
    plt.title(crypto.upper() + ' Line plot for ' + date, color='white')
    plt.tight_layout()
    plots_path = func.get_output_path('Plots')
    fig_name = crypto.upper() + '_line_plot_' + date + '.png'
    absolute_path = os.path.join(plots_path, fig_name)
    plt.savefig(absolute_path, format='png', dpi=800)
    #plt.show()
    return absolute_path


if __name__ == "__main__":
    #
    cryptos = ['BTC', 'LTC', 'ETH', 'XRP']
    for crypto in cryptos:
        df_crypto = get_one_date_dataframe(crypto, func.get_last_date())
        plot_line(df_crypto, crypto)