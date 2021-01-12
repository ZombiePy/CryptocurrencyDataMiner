import os
import getpass
import sys


print('Welcome to Crypto Project installation guide.')
print('')
print('Creating needed directories...   0/5')

os.mkdir('Data')
print('Data created...                  1/5')

os.mkdir('Data/Input')
print('Data/Input created...            2/5')

os.mkdir('Data/Output')
print('Data/Output created...           3/5')

os.mkdir('Data/Output/Plots')
print('Data/Output/Plots created...     4/5')

os.mkdir('Data/Output/Prices')
print('Data/Output/Prices created...    5/5')

print('')

print('Creating needed files...')
os.system("echo 'email,name' >> Data/Input/subscribers.csv")
print('Subscribers list created...              1/4')

name = input('Please give me Your name: ')
email = input('And your email (gmail) address: ')
authentication = True
while authentication:
    password = getpass.getpass('Email password (only stored in your local memory): ')
    password_retype = getpass.getpass('Retype it again: ')
    if password == password_retype:
        authentication = False
        print('Passwords match...')
    else:
        print("Passwords doesn't match...")

print('Adding your address to subscribers list...')
os.system("echo '{email},{name}' >> Data/Input/subscribers.csv".format(name=name, email=email))

authentication_email_form = '{"user": "{email}","password":"{password}"}'
authentication_email_form_personalized = authentication_email_form.format(user=email, password=password)
os.system("echo '{}' >> Data/Input/authentication_email.json".format(authentication_email_form_personalized))
print('Authentication file for email created... 2/4')

os.system('mv Resources/email_form.txt Data/Input')
print('Email form created...                    3/4')

authentication_cmc_form = '{"Accepts": "application/json","X-CMC_PRO_API_KEY": "{}"}'
cmc_key = input("Coin Marker Cap api key: ")
authentication_cmc_form_personalized = authentication_cmc_form.format(cmc_key)
os.system("echo '{}' >> Data/Input/authentication.json".format(authentication_cmc_form_personalized))
print('Authentication file for api created... 4/4')

print('Installing needed libraries...')
os.system('pip3 install -r requirements.txt')

print('Now copy content of Resources/add_to_cron.txt file to your crontab.')
input("If you finished press enter.")

print('')
print('Installation complete')
sys.exit()
