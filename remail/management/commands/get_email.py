import os
import imaplib
import email
from django.core.management.base import BaseCommand
from remail.models import Email


class Command(BaseCommand):
    def handle(self, *args, **options):
        # imap protocol docs:
        # http://tools.ietf.org/html/rfc3501

        obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
        username = os.environ['EMAIL_ACCOUNT']
        password = os.environ['EMAIL_PASSWORD']

        obj.login(username, password)
        obj.select("inbox")
        result, unseen_email = obj.search(None, "UNSEEN")

        # if there are unseen emails get unseen emails and parse
        # and save info
        if result == 'OK' and not unseen_email[0] == '':
            ids = unseen_email[0]
            id_list = ids.split(' ')
            parse_ids_and_save_emails(id_list, obj)


def parse_ids_and_save_emails(id_list, obj):
    for email_id in id_list:
        result, data = obj.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        # The 1 index of the parseaddr gives us the address
        senders_email = email.utils.parseaddr(email_message['From'])[1]

        # Subject does not get parsed like email since
        # I'm only interested in the whole subject string.
        subject = email_message.get('Subject')

        e = Email(subject=subject,
                  senders_email=senders_email,
                  body=raw_email)
        e.save()
