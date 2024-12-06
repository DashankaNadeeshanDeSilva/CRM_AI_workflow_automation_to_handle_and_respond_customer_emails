import re

def extract_email_details(email_data):
    # Extracting the Subject
    subject = re.search(r"Subject: (.+)", email_data)
    if subject:
        subject = subject.group(1)

    # Extracting the Sender
    sender = re.search(r"From: (.+)", email_data)
    if sender:
        sender = sender.group(1).split("<")[1].strip(">")

    # Extracting the Email Body
    # This regex captures text between the plain text declaration and the start of the HTML content
    pattern = re.compile(r"Content-Type: text/plain; charset=\"UTF-8\"\s*\n\n(.*?)\nContent-Type: text/html; charset=\"UTF-8\"", re.DOTALL)
    match = pattern.search(email_data)
    email_body = match.group(1).strip().replace('\n', ' ') if match else "No email body is found."
    email_body.replace("\n", "")

    return sender, subject, email_body


def get_text_from_md(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content