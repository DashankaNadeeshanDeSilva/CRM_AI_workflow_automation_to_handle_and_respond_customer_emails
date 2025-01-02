from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# load env varaiable
load_dotenv()

# Load DB URL from .env
DATABASE_URL = os.getenv("TICKET_DATABASE_URL")

# SQLALchemy setuo
Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    email_body = Column(String, nullable=False)
    intent = Column(String, nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

class Database_Manager():
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_table(self):
        try:
            Base.metadata.create_all(self.engine)
            '''SQLAlchemy scans all models registered under Base and creates tables for them, including the Ticket table.
                The Ticket class above defined is already registered with Base.metadata because it inherits from Base'''
        except Exception as e:
            raise Exception(f"Error creating table: {str(e)}")
        
    def add_ticket(self, email_data) -> int:
        '''Add a new ticket to the database and return the unique ticket ID.'''
        session = self.SessionLocal()
        try:
            new_ticket = Ticket(
                customer_email=email_data["email_id"], 
                subject=email_data["email_subject"],
                email_body=email_data["email_body"],
                intent=email_data["intent"])
            
            session.add(new_ticket)
            session.commit()
            session.refresh(new_ticket)
            print(f"New ticket created with ID: {new_ticket.id}")
            return new_ticket.id  # Return the unique ticket number
        
        except Exception as e:
            session.rollback()
            print(f"Error adding ticket: {str(e)}")
            raise
        
        finally:
            session.close()


if __name__ == "__main__":
    '''Test the Database_manager class'''
    db_manager = Database_Manager()
    
    email_data = {
        "email_id": "dashankadesilva@gmail.com",
        "email_subject": "Help with the product I ordered",
        "email_body": "Hello, I ordered a TurboDry 3000 hair dryer a week ago. It still has not delivered though it suppose to be delivered in 3 days. Can you please help me with this. The order number is LD3362763. Thank you. Best Dashnaka",
        "intent": "Order Inquiries"
    }

    ticket_id = db_manager.add_ticket(email_data)
    print(f"Ticket successfully created with Ticket No: {ticket_id}")

