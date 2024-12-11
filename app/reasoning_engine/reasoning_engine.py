# email_agent.py
import requests
import json
import os
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain_core.runnables import RunnableSequence

from utils import get_text_from_md
from reasoning_engine_helpers import *
from app.services.knowledge_base import Knowldge_DB
from llm import LLM


# Reasoning engine chain
def reasoning_engine(email_data):
    # Reasoning chain
    chain = RunnableSequence(
        # Retrive context from RAG system
        RunnableLambda(lambda input_data_init:{
            **input_data_init,
            "context": retrieve_context(input_data_init)}
        ),
        # Prompt to decide to create tickets
        RunnableLambda(lambda input_data:{
            **input_data, 
            "ticket_decision_prompt": ticket_decision_prompt(input_data)}
        ),
        # Invoke LLM for Ticket Decision
        RunnableLambda(lambda input_data:{
            **input_data,
            "ticket_create": invoke_LLM(input_data["ticket_deision_prompt"], input_data["llm"])}
        ),
        # Create reference ticket
        RunnableLambda(lambda input_data:{
            **input_data, 
            "ticket_no": create_ticket_in_db(input_data) if input_data["ticket_create"] == "Yes" else None}
        ),
        # Prompt to create reply email
        RunnableLambda(lambda input_data:{
            **input_data,
            "reply_email_prompt": reply_email_prompt(input_data)} 
        ),
        # Invoke LLM for generate reply email
        RunnableLambda(lambda input_data:{
            **input_data,
            "reply_email": invoke_LLM(input_data["reply_email_prompt"], input_data["llm"])}
        )
    )

    ## Inputs
    # email_data = {"email_id":email_id, "email_subject": email_subject, "email_body": email_body, "intent": intent, "intent_reason": intent_reason}
    # LLM 
    llm = LLM()
    

    # Run the Chain
    input_data_init = {
        "email_body": "I need help with my product.",
        "collection": collection,
        "intent": "Product Support",
        "llm": llm  # Pass the LLM object
    }

    reply_email = chain.invoke(input_data_init)

    return reply_email

def reasoning_engine_old(email_data):
    '''Create LLM for reasoning using wrapper and RunnableLambda object'''
    reasoning_llm = Reasoning_LLM()

    # wrapper for reasoning LLM
    def llm_reasoning(prompt_text):
        return reasoning_llm.get_llm_reasoning(prompt_text.to_string())

    # Langchain RunnableLambda object for llm
    llm = RunnableLambda(llm_reasoning)
    
    '''Create prompt template'''
    template = "{reasoning_prompt_head} \n {email_data}"
    prompt = PromptTemplate(template=template, input_variable=["reasoning_prompt_head", "email_data"])

    # Create Langchain reasoning chain
    reasoning_chain = RunnableSequence(prompt, llm)

    # Input data prep
    REASONING_PROMPT_HEAD = get_text_from_md("prompts/reasoning_prompt_head.md")
    email_data = json.dumps(email_data)
    input_data = {"reasoning_prompt_head": REASONING_PROMPT_HEAD, "email_data": email_data}

    # invoke reasoning engine to get response
    reasoning_engine_response = reasoning_chain.invoke(input_data)

    # response should match reasoning engine output criteria
    # return reasoning_engine_response