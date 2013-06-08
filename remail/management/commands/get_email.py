import os
import imaplib
import email
from django.core.management.base import BaseCommand
from remail.models import Email


class Command(BaseCommand):
    def handle(self, *args, **options):
        # imap protocol docs:
        # http://tools.ietf.org/html/rfc3501
        connection = create_connection()

        connection.select("inbox")

        result, unseen_email = connection.search(None, "UNSEEN")

        # if there are unseen emails parse and save info
        if result == 'OK' and not unseen_email[0] == '':
            parse_ids_and_save_emails(unseen_email, connection)

        close_connection(connection)


def create_connection():
    connection = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    username = os.environ['EMAIL_ACCOUNT']
    password = os.environ['EMAIL_PASSWORD']
    connection.login(username, password)
    return connection


def close_connection(connection):
    connection.close()
    connection.logout()


def parse_ids_and_save_emails(unseen_email, obj):
    ids = unseen_email[0]
    id_list = ids.split(' ')

    for email_id in id_list:
        result, data = obj.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        # Save the message if the message does not have a thread
        if not email_message.is_multipart():
            # The 1 index of the parseaddr gives us the address
            senders_email = email.utils.parseaddr(email_message['From'])[1]

            # Subject does not get parsed like email since
            # I'm only interested in the whole subject string.
            subject = email_message.get('Subject')

            e = Email(subject=subject,
                      senders_email=senders_email,
                      body=raw_email)
            e.save()
