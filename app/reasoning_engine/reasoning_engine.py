from langchain.schema.runnable import RunnableLambda
from langchain_core.runnables import RunnableSequence

from app.reasoning_engine.reasoning_engine_helpers import *
from app.reasoning_engine.llm import LLM


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
            "ticket_create": invoke_LLM(input_data["ticket_decision_prompt"])}
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
            "reply_email": invoke_LLM(input_data["reply_email_prompt"])}
        )
    )

    # Run the Chain
    input_data_init = email_data
    output = chain.invoke(input_data_init)

    if output["reply_email"]: 
        reply_email = output["reply_email"] 
    
    else: reply_email = None

    return reply_email, output["ticket_no"]