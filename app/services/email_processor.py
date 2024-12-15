import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv() # load env var and keys

class EMail_Processor():
    def __init__(self):
        self.email_address = os.getenv("EMAIL_ADDRESS") # dashankaaitesting@gmail.com
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.smtp_server = os.getenv("SMTP_SERVER")

    
    def connect_imap(self):
        '''access to the email client  with email credentials'''
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            # login to the email client
            mail.login(self.email_address, self.email_password)
            return mail
        except Exception as e:
            raise Exception(f"Error connecting to IMAP: {str(e)}")
    

    def fetch_emails(self):
        '''read and get unseen emails'''
        try:
            mail = self.connect_imap()
            mail.select("inbox")
            # Searches the selected folder for specific emails
            _, data = mail.search(None, "UNSEEN")
            # ToDo: Add to do nothing if there are no emails in the inbox
            # Extracts the email IDs from the data object which contains all emial IDs 
            # as single byte string  and splits them into a list.
            email_ids = data[0].split()
            
            if not email_ids:
                return {"status": "success", "message": "No new emails.", "emails": []}
            
            emails = []
            for email_id in email_ids:
                # Retrieves the full content of an email by its email ID
                _, msg_data = mail.fetch(email_id, "(RFC822)")
                # Accesses the actual raw content of the email (skipping metadata)
                # and decode from bytes to string with UTF-8
                emails.append(msg_data[0][1].decode())
                # Mark fetched email as seen
                mail.store(email_id, '+FLAGS', '\\Seen')  
            
            mail.logout()
            
            return {"status": "success", "message": "Emails fetched successfully.", "emails": emails}

        except Exception as e:
            raise Exception(f"Error fetching emails: {str(e)}")
        

    def reply_email(self, email_data):
        '''send reply email to fetched and processed emails'''
        message = MIMEMultipart()
        
        message["From"] = self.email_address # dashankaaitesting@gmail.com
        message["To"] = email_data["email_id"] # customer email
        message["Subject"] = f"Re: {email_data['email_subject']}"
        email_body = email_data["reply_email"]
        
        if email_data["message_id"]:
            message_id = email_data["message_id"]
            references = email_data["message_id"]
        else:
            message_id=None
            references=None
        
        # Add threading headers
        if message_id:
            message["In-Reply-To"] = message_id
        if references:
            message["References"] = references

        message.attach(MIMEText(email_body, "plain"))

        with smtplib.SMTP_SSL(self.smtp_server) as server:
            server.login(self.email_address, self.email_password)
            server.send_message(message)



