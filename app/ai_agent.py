from services.email_processor import EMail_Processor
from services.intent_classification import Intent_Classifier
import logging


logger = logging.getLogger("AI_Agent")

class AI_Agent():
    def __init__(self):
        self.email_processor = EMail_Processor()
        self.indent_classifier = Intent_Classifier()

    def run_ai_agent(self):
        '''
        This function orchestrate the AI agent's workflow
        - fetch emails
        - classify intent
        - ticket creation (if required)
        '''

        # Step 1: fetch emails
        logger.info("Fetching emails")
        emails = self.email_processor.fetch_emails()
        # {"status": "success", "message": "Emails fetched successfully.", "emails": emails}
        # handle if no new emails are found
        if emails["message"] == "No new emails.":
            logger.info("No new emails to process")
            return

        # Step 2: indent classification
        for email in emails["emails"]:
            
         

