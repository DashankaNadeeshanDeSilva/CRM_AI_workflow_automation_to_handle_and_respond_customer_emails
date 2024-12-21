# CRM-AI-Agent-to-handle-and-respond-customer-emails

AI agent to handle and respond to customer emails using an internal knowledge base.

## Motivation
Businesses often receive a large volume of emails from customers inquiring about products, reporting issues, or requesting assistance. This requires significant effort to classify, respond, or escalate inquiries efficiently. This project leverages AI to automate email management, providing timely responses and improving customer satisfaction.

## Goal and Objectives
The goal is to develop an AI agent that can:
1. Read and classify emails based on intent or actionable categories.
2. Generate responses using a company knowledge base.
3. Escalate by creating tickets when necessary.
4. Log actions and maintain reports.

## AI Agent Workflow

![AI_Agent_workflow](images/ai_agent_workflow.png)

### Input Data:
- The AI agent checks emails in regulare intervals
- Once new emails are recived, they are fetched from the email client.

### Reasoning Engine Tasks:
1. Read the email body to classify intent and reason from the input data.
2. Decide actions using an LLM:
    - Determine if knowledge from the vector database (Chromadb) is required to generate a reply email.
    - Identify if a ticket should be created and creat tickets in remote SQL Database.
    - Gather relevant information for tickets, including problem description, intent class, reason, and email metadata.
3. Generate a response email using LLM based on the email body, intent, and gathered context (including ticket numbers if created).
4. Log activities in Google Sheets.

### Actions:
- Create tickets via a remote database connection if required.
- Send response emails to customers, including the gathered context and ticket number if applicable.
- Log activities into a database for tracking and reporting.

### Tools Involved:
- Email client: fetching emails and replying them
- Vector Database:  Extracting context from knowledge base
- Remote SQL Database: Create tickets
- Google Sheets: Log AI Agent activities 

## Project Structure
- `app/`: Contains the application code.
- `requirements.txt`: Lists the dependencies.
- `.env`: Stores environment variables.
- `Dockerfile`: Used to containerize the application.

### Main Functionality Dependencies
- Python 3.10
- FastAPI: 
- Docker: Deploy containerised application
- LangChain: To create LLM, prompt and function chains
- OpenRouter API for LLMs: LLM invokation are done with API endopoints (Llama 3.2 30b)
- Google APIs: Build connections to Google Gmail client and app api to Google Sheets 

## How to Run
### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t crm-ai-agent .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 --env-file .env crm-ai-agent
   ```
3. Access the application at `http://localhost:8000`.

### Without Docker
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Future Work
- Enhance the knowledge base with additional sources.
- Integrate with advanced ticketing systems.
- Add a dashboard for analytics and reporting.

---

Feel free to reach out for any clarifications or suggestions. Enjoy using the CRM AI Agent!



