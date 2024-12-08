# email_agent.py
import requests
import json
import os
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain_core.runnables import RunnableSequence

from utils import get_text_from_md

# LLM reasoning invokation class
class Reasoning_LLM():
    def __init__(self):
        self.REASONING_LLM = os.getenv("REASONING_LLM")
        self.OPENROUTER_URL = os.getenv("OPENROUTER_URL")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    def get_llm_reasoning(self, reasoning_prompt):
        if not isinstance(reasoning_prompt, str):
            raise ValueError(f"reasoning_prompt must be a string, got {type(reasoning_prompt)}")

        payload = {
            "model": self.REASONING_LLM,
            "messages": [{"role": "reasoning-ai-agent", "content": reasoning_prompt}]
        }

        try:
            response = requests.post(
                url= self.OPENROUTER_URL,
                headers={"Authorization": f"Bearer {self.OPENROUTER_API_KEY}"},
                data= json.dumps(payload)
            )

            # Check if the response is successful
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
                # Log the error and raise it
                raise Exception(f"Request failed: {str(e)}") from e

        # handle response output
        response_data = response.json()
        content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No content found")
    
        return content
# --------------------------------------------------------------------------    

def reasoning_engine(email_data):
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