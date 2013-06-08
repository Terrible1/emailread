import imaplib
import os


def open_connection(verbose=False):
    connection = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    username = os.environ['EMAIL_ACCOUNT']
    password = os.environ['EMAIL_PASSWORD']

    connection.login(username, password)
    return connection
