import logging

from app.services.email_processor import EMail_Processor
from app.services.intent_classification import Intent_Classifier
from app.services.utils import parse_email

from app.reasoning_engine.reasoning_engine import reasoning_engine


logger = logging.getLogger("AI_Agent")

class AI_Agent():
    def __init__(self):
        self.email_processor = EMail_Processor()
        self.intent_classifier = Intent_Classifier()

    def run_ai_agent(self):
        '''
        This function orchestrate the AI agent's workflow
        - fetch emails
        - classify intent
        - run reasoning engine (core functionalities of agent)
        '''

        # Step 1: fetch emails {Tools}
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
            email_data = parse_email(email)
            
            # get intent classification
            classification = self.intent_classifier.get_classification(email_data["email_body"])
            email_data.update(classification)

            """
            email_data = {'email_id': 'Dashanka Nadeeshan <dashankadesilva@gmail.com>', 
                         'email_subject': 'Defect with product and claiming warranty.', 
                         'email_body': "Dear Sir/Madam,\r\n\r\nI bought a TV from you last week (ordered online). I have been using it for\r\none month now. However, it suddenly stopped working. I want to repair this\r\nor get a new one as a replacement since it's within the warranty period.\r\nThank you.\r\n\r\n-- \r\nBest Regards,\r\n*Dashanka Nadeeshan De Silva.*\r\n", 
                         'intent': 'Technical Support and Warranty', 
                         'reason': 'The customer is reporting an issue with their product (the TV stopped working) and is seeking assistance or claiming warranty within the warranty period.'}
            """

            reply_email = reasoning_engine(email_data)
            
            ## Send reply to the customer
            self.email_processor.reply_emails(email_id, email_subject, reply_email)

            # Response generator
            '''
            AI agent actions with tools:  create tickets, send emails and log activity in DB

            Input data:
                - inputs dict keys: customer_email, email_subject, email_body, email_intent_class, intent_class_reasoning
                - Access the knowldege base (vector db) that contains information and data about products, prices, inventory, processes, policies and more.
            Resoning Engine Tasks/Instructions:
                1. Read the emal body and intend class & reason from input data
                2. Think and decide following:
                    - Think and decide if it requires to get info from knowlege base to generate the reply email. 
                        - If reasonable and requires, gather knowledge from {KNOWLEDGE_BASE}.
                    - Think and decide if it requires and reasonable to create tickets (for general inquaries except sales opportunities or issues/problems, only generate repsonse with knwoledge base)
                        - If requires gather data to create ticket including problem/issue, intent class and reason, all email data (email id and email body)
                3. Generate response email based on following:
                    - Initial greeting and overview answer.
                    - Actual response for the customer inquiry including ticket no if exists.
                    - Next steps for the customer inqury if a ticket is involved.
                    - closing remarks with thanking or apology.  
                4 Log activities including email data and actions taken and store in {DB}.
            Actions to take:
                - Ticket creation, if required using {TICKET_TOOL}
                - Generate a response email to the customer including knowledge gather earlier for that, and ticket number if one has been created, then 
                - Activity logging into {DB}




            output json:
            {
            ticket_creation: YES
            ticket_info: Problem, intent class and reason, all email data (within limited characters)
            respond_email_subject: respond email subject
            respond_email_body: respond_email_body
            cutomer_email: customer email (or sender's email)
            }
            '''




         

