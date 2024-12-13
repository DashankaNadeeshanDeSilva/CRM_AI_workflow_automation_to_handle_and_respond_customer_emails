import re
import email
from email.policy import default

def extract_email_details(email_data):
    # Extracting the Subject
    subject = re.search(r"Subject: (.+)", email_data)
    if subject:
        subject = subject.group(1)

    print(f"Subject: {subject}")

    # Extracting the Sender
    sender = re.search(r"From: (.+)", email_data)
    if sender:
        sender = sender.group(1).split("<")[1].strip(">")

    print(f"Sender: {sender}")

    # Extracting the Email Body
    # This regex captures text between the plain text declaration and the start of the HTML content
    pattern = re.compile(r"Content-Type: text/plain; charset=\"UTF-8\"\s*\n\n(.*?)\nContent-Type: text/html; charset=\"UTF-8\"", re.DOTALL)
    match = pattern.search(email_data)
    email_body = match.group(1).strip().replace('\n', ' ') if match else "No email body is found."
    email_body.replace("\n", "")

    return sender, subject, email_body


def parse_email(raw_email_content):
    # Parse the raw email content
    email_message = email.message_from_string(raw_email_content, policy=default)
    
    # Extract the sender's email address
    sender = email_message['From']
    
    # Extract the email subject
    subject = email_message['Subject']
    
    # Extract the email body
    body = None
    if email_message.is_multipart():
        # Iterate through email parts to find the plain text body
        for part in email_message.iter_parts():
            if part.get_content_type() == 'text/plain':
                body = part.get_content()
                break
    else:
        # If not multipart, directly get the payload
        body = email_message.get_content()

    email_data = {"email_id": sender, "email_subject": subject, "email_body": body}
    
    return email_data


def get_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content