import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def log_activity_to_google_sheet(email_data, sheet_name="CRM AI Agent Activity Log"):
    try:
        # Get the credentials file path from the .env file
        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
        if not credentials_file:
            raise ValueError("GOOGLE_CREDENTIALS_FILE path not found in .env file")

       # Define the scope for Google Sheets API
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Authenticare using the service account
        credentials = Credentials.from_service_account_file(credentials_file, scopes=scope)
        client = gspread.authorize(credentials)

        # Open google sheet
        sheet = client.open(sheet_name).sheet1 # access sheet the first sheet

        # Prepare the data to append (ensure order matches the sheet's columns)
        row = [
            email_data.get("email_id", "N/A"),
            email_data.get("email_subject", "N/A"),
            email_data.get("email_body", "N/A"),
            email_data.get("message_id", "N/A"),
            email_data.get("intent", "N/A"),
            email_data.get("reply_email", "N/A"),
            email_data.get("ticket_no", "N/A"),
            email_data.get("status", "Replied to the customer")  # Add a status column
        ]

        # Append the row to the sheet
        sheet.append_row(row)
        print("Activity logged successfully.")

    except Exception as e:
        print(f"Error logging activity to Google Sheet: {e}")


if __name__ == "__main__":

    email_data = {
    "recipient": "example@gmail.com",
    "subject": "Order Inquiry",
    "body": "Can you help me with my delayed order?",
    "message_id": "<abc123@example.com>",
    "intent": "Warranty and Service",
    "reply_email": "we are sorry for your inconvinece"
    }
    
    log_activity_to_google_sheet(
        sheet_name="CRM AI Agent Activity Log", 
        email_data=email_data)
     
    
    

        