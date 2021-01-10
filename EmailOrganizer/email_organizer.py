import imaplib, email
import json
import os


credentials_path = os.path.join('..', 'Data', 'Input', 'authentication_email.txt')
with open(credentials_path) as json_file:
    credentials = json.load(json_file)

user = credentials['user']
password = credentials['password']
imap_url = 'imap.gmail.com'


# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


con = imaplib.IMAP4_SSL(imap_url)

con.login(user, password)

con.select('Inbox')

_, [msgs_id] = con.search(None, 'FROM', '"*"')

for msg_id in msgs_id.split():
    _, msg = con.fetch(msg_id, '(RFC822)')
    for sent in msg:
        if type(sent) is tuple:

            content = str(sent[1], 'utf-8')
            data = str(content)

            try:
                index_start = data.find("Name")
                data_beginning = data[index_start:len(data)]
                index_end = data_beginning.find("Type:")

                info = data_beginning[0: index_end+12]
                print(info)

            except UnicodeEncodeError as e:
                pass

    instruction = info[index_end+5:]
    instruction = instruction.replace(" ", "")
    print(instruction)

#con.store(msgs_id, '+FLAGS', r'(\Deleted)')
