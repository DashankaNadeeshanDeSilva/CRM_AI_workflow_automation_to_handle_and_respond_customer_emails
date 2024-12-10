import requests
import json
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# LLM reasoning invokation class
class LLM():
    def __init__(self):
        self.REASONING_LLM = os.getenv("REASONING_LLM")
        self.OPENROUTER_URL = os.getenv("OPENROUTER_URL")
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

    def invoke_llm(self, prompt):
        if not isinstance(prompt, str):
            raise ValueError(f"reasoning_prompt must be a string, got {type(prompt)}")

        payload = {
            "model": self.REASONING_LLM,
            "messages": [{"role": "customer-handling-agent", "content": prompt}]
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