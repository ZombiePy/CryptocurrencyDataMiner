import pandas as pd
import os
import Utilities.functions as func


def get_one_date_dataframe(crypto, date):
    dates = func.get_dates(crypto)
    if date in dates:
        output_path = func.get_output_path()
        absolute_path = os.path.join(output_path, crypto + '_' + date + '.csv')
        df = pd.read_csv(absolute_path, parse_dates=True)
    else:
        raise FileNotFoundError('There is no file from ' + date + ' date')
    return df


def get_full_crypto_dataframe(crypto):
    file_names = func.get_prices_files(crypto)
    output_path = func.get_output_path()

    result = pd.DataFrame(columns=['timestamp', 'symbol', 'price_usd'])
    for file in file_names:
        file_path = os.path.join(output_path, file)
        df = pd.read_csv(file_path, index_col=0)
        result.append(df, ignore_index=True)

    result.drop_duplicates()
    result.reset_index()
    return result


def get_daily_dataframe(crypto):
    temp_dict = {'Low': [],
            'High': list(),
            'Open': list(),
            'Close': list(),
            'Date': list()}

    dates = func.get_dates()

    for date in dates:
        file_path = func.get_file_path(crypto, date)
        df_daily = pd.read_csv(file_path)

        temp_dict['Low'].append(min(df_daily['price_usd']))
        temp_dict['High'].append(max(df_daily['price_usd']))
        temp_dict['Open'].append(df_daily.sort_values(by=['timestamp'], ignore_index=True).iloc[0]['price_usd'])
        temp_dict['Close'].append(df_daily.sort_values(by=['timestamp'], ignore_index=True).iloc[-1]['price_usd'])
        temp_dict['Date'].append(date)

    index = pd.Index(temp_dict['Date'], name='Date')
    df = pd.DataFrame(temp_dict, index=index)
    return df
