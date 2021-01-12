from DataGathering.csv_data_parser import CsvDataParser
import os
import re


def mqtt_receiving(crypto, output_file_path):
    client_name = crypto + '1'
    data_parser = CsvDataParser(crypto, client_name, output_file_path)

    def on_message_func(client, userdata, msg):
        nonlocal data_parser
        data_parser.add_message(msg.topic, msg.payload)

    data_parser.run(on_message_func)


def get_dates(crypto='BTC'):
    file_names = get_prices_files(crypto)
    dates = set()
    for file_name in file_names:
        date_csv = file_name.split('_')[1]
        date = date_csv.split('.')[0]
        dates.add(date)

    return dates


def get_output_path(path_type='Prices'):
    active_path = os.getcwd()
    if os.path.isdir('Data'):
        output_path = os.path.join(active_path, 'Data', 'Output', path_type)
    else:
        os.chdir('..')
        output_path = get_output_path(path_type)
    return output_path


def get_file_path(crypto, date):
    output_path = get_output_path()
    file_name = crypto + '_' + date + '.csv'
    return os.path.join(output_path, file_name)


def get_prices_files(crypto):
    output_file_path = get_output_path()
    files = os.listdir(output_file_path)
    files_given_crypto = list()
    for file_price in files:
        if re.search(crypto, file_price):
            files_given_crypto.append(file_price)
    return files_given_crypto


def get_last_date():
    dates = get_dates()
    return sorted(dates)[-1]


def get_plot_path(date, plot_type, crypto):
    file_name = crypto.upper() + '_' + plot_type + '_' + date + '.png'
    return os.path.join(get_output_path('Plots'), file_name)


def list_to_html_table(list_of_data):
    table_content = ""
    for sublist in list_of_data:
        table_content += "<tr>\n"
        for data in sublist:
            table_content += "<td>" + str(data) + "</td>\n"
        table_content += "</tr>\n"
    return table_content[:-1]


def add_subscriber(email,name):
    subscribers_path = os.path.join("..", 'Data', 'Input', 'subscribers.csv')
    with open(subscribers_path, 'a') as subscribers:
        subscribers.write('\n' + email + ',' + name)


def remove_subscriber(email, name):
    subscribers_path = os.path.join("..", 'Data', 'Input', 'subscribers.csv')
    with open(subscribers_path, '') as subscribers:
        lines = subscribers.readlines()
        subscribers.seek(0)
        for line in lines:
            if line != email + "," + name:
                subscribers.write(line)
        subscribers.truncate()
