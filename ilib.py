"""This file was used for testing purposes.
"""
import imaplib
import os
import email


def open_connection(verbose=False):
    connection = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    username = os.environ['E_READ_ACCOUNT']
    password = os.environ['E_READ_PASSWORD']

    connection.login(username, password)
    return connection

connection = imaplib.IMAP4_SSL('imap.gmail.com', '993')
username = os.environ['E_READ_ACCOUNT']
password = os.environ['E_READ_PASSWORD']

connection.login(username, password)
connection.select("inbox")
# result, unseen_email = connection.search(None, 'UNSEEN')

result, unseen_email = connection.uid('search', None, 'UNSEEN')

uids = unseen_email[0]
uid_list = uids.split(' ')

for uid in uid_list:
    result, data = connection.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')
    # if it was an unseen  and not threaded email, save the email
    if result == 'OK' and not data == '':
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        # The 1 index of the parseaddre gives us the email address
        senders_email = email.utils.parseaddr(email_message['From'])[1]

        subject = email_message.get('Subject')


if __name__ == '__main__':
    pass
