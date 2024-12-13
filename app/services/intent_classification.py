import requests
import json
from dotenv import load_dotenv
from app.services.utils import get_text_from_md
from pathlib import Path
import os

# Load the .env file
load_dotenv()

class Intent_Classifier():
    def __init__(self):
        self.OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        self.APP_NAME = os.getenv("APP_NAME")

        self.INTEND_CLASS_LLM = os.getenv("INTEND_CLASS_LLM")
        self.OPENROUTER_URL = os.getenv("OPENROUTER_URL")

        # Get the root directory of the project
        base_dir = Path(__file__).resolve().parent.parent

        self.CLASSFICATION_PROMPT_HEAD = get_text_from_md(base_dir / "prompts/intent_classification_head.md")
        self.CLASSFICATION_GUIDE = get_text_from_md(base_dir / "prompts/email_classification_guide.md")

    def get_classification(self, email_body):

        classfication_prompt = f"{self.CLASSFICATION_PROMPT_HEAD}; \n Find detailed classification guidance: {self.CLASSFICATION_GUIDE}; \n Find email body: {email_body}"

        try:
            response = requests.post(
                url= self.OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
                    "X-Title": f"{self.APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
                },
                data= json.dumps({
                    "model": self.INTEND_CLASS_LLM, # optional
                    "messages": [{"role": "user", 'content': classfication_prompt}]
                })
            )

            # Check if the response is successful
            response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            # Log the error and raise it
            raise Exception(f"Request failed: {str(e)}") from e

        response_data = response.json()
        #response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No content found")

        response_content = json.loads(response_data['choices'][0]['message']['content'])

        return response_content
    
        '''
        except ValueError:
            raise Exception(f"Failed to parse JSON response: {response.text}")
        except ValueError:
            raise Exception(f"Unexpected response format: {response_content}")
        '''
