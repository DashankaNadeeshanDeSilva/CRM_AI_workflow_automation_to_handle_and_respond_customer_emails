import chromadb
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain_core.runnables import RunnableSequence
from app.services.utils import get_text_from_md
from app.knowledge_base.knowledge_base import Knowledge_Base
from app.reasoning_engine.llm import LLM
from app.services.create_ticket import Database_Manager
from pathlib import Path
import os

# Retrive context from knowledge base
def retrieve_context(input_data):
    email_body = input_data["email_body"]
    intent = input_data["intent"]
    query = f"{email_body} Intent: {intent}"
    
    knowledge_base = Knowledge_Base()
    knowledge_base_collection = knowledge_base.get_collection()
    context =knowledge_base.query(collection=knowledge_base_collection, query=query)
    return context

# Prompt to decide to create tickets 
def ticket_decision_prompt(input_data):
    # Get the root directory of the project
    base_dir = Path(__file__).resolve().parent.parent
    TICKET_DECISION_TEMPLATE = get_text_from_md(base_dir / "prompts/ticket_decision_template.md")
    ticket_decision_prompt_temp = PromptTemplate(template=TICKET_DECISION_TEMPLATE, input_variable=["email_body", "intent", "context"])
    ticket_decision_prompt = ticket_decision_prompt_temp.format(email_body=input_data["email_body"], intent=input_data["intent"], context=input_data["context"])
    return ticket_decision_prompt

# LLM Decision Task to Create a Ticket
def invoke_LLM(prompt):
    llm = LLM()
    llm_output = llm.invoke_llm(prompt)
    return llm_output

# Interact with Database to Create a Ticket
def create_ticket_in_db(input_data):
    db_manager = Database_Manager()
    ticket_id = db_manager.add_ticket(input_data)
    return ticket_id

# Prompt to decide to create tickets
def reply_email_prompt(input_data):
    base_dir = Path(__file__).resolve().parent.parent
    REPLY_EMAIL_TEMPLATE = get_text_from_md(base_dir / "prompts/reply_email_template.md")
    reply_email_prompt_temp = PromptTemplate(template=REPLY_EMAIL_TEMPLATE, input_variable=["email_body", "email_subject", "intent", "context", "ticket_no"])
    reply_email_prompt = reply_email_prompt_temp.format(email_body=input_data["email_body"], email_subject=input_data["email_subject"], intent=input_data["intent"], context=input_data["context"], ticket_no=input_data["ticket_no"])
    return reply_email_prompt
