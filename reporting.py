from Utilities.functions_dataframe import  get_daily_dataframe
import Utilities.functions as func
import os
import yagmail
import pandas as pd
import json
import time


cryptos = ['BTC', 'LTC', 'ETH', 'XRP']
last_day = func.get_last_date()

os.system('python3 ./candle_stick.py &')
os.system('python3 ./line_plot.py &')
os.system('python3 ./email_organizer.py &')

time.sleep(60)

table = list()
for crypto in cryptos:
    df_daily = get_daily_dataframe(crypto)
    df_daily = df_daily[df_daily['Date']==last_day]
    temp_list = [crypto,
                 round(df_daily['Low'].values[0], 2),
                 round(df_daily['High'].values[0], 2),
                 round(df_daily['Open'].values[0], 2),
                 round(df_daily['Close'].values[0], 2)]
    table.append(temp_list)


email_form_path = os.path.join(os.getcwd(), 'Data', 'Input', 'email_form.txt')
with open(email_form_path, 'r') as email_file:
    email_form = email_file.read()

email_form = email_form.replace('rest_of_table', func.list_to_html_table(table))
plots_path = func.get_output_path('Plots')

attachments = [
    func.get_plot_path(last_day, 'line_plot', 'btc'),
    func.get_plot_path(last_day, 'candle_stick', 'btc'),
    func.get_plot_path(last_day, 'line_plot', 'eth'),
    func.get_plot_path(last_day, 'candle_stick', 'eth'),
    func.get_plot_path(last_day, 'line_plot', 'xrp'),
    func.get_plot_path(last_day, 'candle_stick', 'xrp'),
    func.get_plot_path(last_day, 'line_plot', 'ltc'),
    func.get_plot_path(last_day, 'candle_stick', 'ltc')
]
credentials_path = os.path.join(os.getcwd(), 'Data', 'Input', 'authentication_email.json')
with open(credentials_path) as json_file:
    credentials = json.load(json_file)

subscribers = pd.read_csv(os.path.join(os.getcwd(), 'Data', 'Input', 'subscribers.csv'))
subscribers = subscribers.drop_duplicates()

for _, row in subscribers.iterrows():
    email_form_personalized = email_form.format(name=row['name'], date=last_day)
    #initializing the server connection
    yag = yagmail.SMTP(user=credentials['user'], password=credentials['password'])
    #sending the email
    yag.send(to=row['email'],
             subject='Daily cryptocurrencies update',
             contents=email_form_personalized,
             attachments=attachments)

    print("Email sent successfully")



