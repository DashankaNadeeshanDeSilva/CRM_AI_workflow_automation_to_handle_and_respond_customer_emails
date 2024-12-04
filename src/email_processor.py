import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multpart import MIMEMultipart
import os
from dotnev import load_dotenv

load_dotenv() # load env var and keys

class EMail_Processor():
    def __init__(self):
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_passowrd = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.smtp_server = os.gentenv("SMTP_SEVRVER")

    
    def connect_imap(self):
        '''access to the email client  with email credentials'''
        mail = imaplib.IMAP4_SSL(self.imap_server)
        # login to the email client
        mail.login(self.email_address, self.email_passowrd)
        return mail  
    

    def read_emails(self):
        '''read and get unseen emails'''
        mail = self.conect_imap()
        mail.select("inbox")
        # Searches the selected folder for specific emails
        _, data = mail.search(None, "UNSEEN")
        # Extracts the email IDs from the data object which contains all emial IDs 
        # as single byte string  and splits them into a list.
        email_ids = data[0].split()
        emails = []
        for email_id in email_ids:
            # Retrieves the full content of an email by its email ID
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            # Accesses the actual raw content of the email (skipping metadata)
            # and decode from bytes to string with UTF-8
            emails.append(msg_data[0][1].decode())
        mail.logout()
        return emails


