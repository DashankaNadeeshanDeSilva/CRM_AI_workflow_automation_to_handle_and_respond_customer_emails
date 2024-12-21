import logging
from app.services.email_processor import EMail_Processor
from app.services.intent_classification import Intent_Classifier
from app.services.utils import parse_email
from app.reasoning_engine.reasoning_engine import reasoning_engine
from app.services.log_activity import log_activity_to_google_sheet

logger = logging.getLogger("AI_Agent")

class AI_Agent():
    def __init__(self):
        self.email_processor = EMail_Processor()
        self.intent_classifier = Intent_Classifier()

    def run_ai_agent(self):
        '''Orchestrate the AI agent's workflow'''
        # fetch emails {Tools}
        logger.info("Fetching emails")
        emails = self.email_processor.fetch_emails()
        # {"status": "success", "message": "Emails fetched successfully.", "emails": emails}
        # handle if no new emails are found
        if emails["message"] == "No new emails.":
            logger.info("No new emails to process")
            return

        for email in emails["emails"]:
            logger.info(f"Processing email")
            # get email data
            email_data = parse_email(email)
            
            # Get intent classification
            classification = self.intent_classifier.get_classification(email_data["email_body"])
            email_data.update(classification)
            
            # Use the reasoning engine to generate reply
            email_data['reply_email'], email_data["ticket_no"] = reasoning_engine(email_data)
             
            # Send reply to the customer
            if email_data['reply_email']:
                self.email_processor.reply_email(email_data)
            
            # Log the activity to Google sheet
            log_activity_to_google_sheet(email_data)



         

