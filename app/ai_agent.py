import logging

from services.email_processor import EMail_Processor
from services.intent_classification import Intent_Classifier
from services.utils import extract_email_details


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
            logger.info(f"Processing email")
            sender, subject, email_body = extract_email_details(email)
            
            # get intent classification
            classification = self.indent_classifier.get_classification(email_body)
            intent_class = classification["Class"]
            intent_class_reasoning = classification["Reason"]

            # Response generator
            '''
            inputs: sender, subject, email_body, intent_class, intent_class_reasoning
            Tasks:
                - Check if required to get info from knowlege based (vector db)
                - Create tickets if requires (for general inquaries, only generate repsonse with knwoledge base) 
                - Generate response email including:
                    - Initial greeting and overview answer
                    - Actual response for the customer inquiry including ticket no if exists
                    - Next steps for the customer inqury if a ticket is involved
                    - closing remarks with thanking or apology  
                - Log activities including email data and actions taken
                
            '''




         

