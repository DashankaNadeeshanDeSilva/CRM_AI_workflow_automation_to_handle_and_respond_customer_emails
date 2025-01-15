# CRM AI Agent to handle and respond to customer emails

AI agent to handle and respond to customer emails using an internal knowledge base.

## 01. Motivation and Goals
Businesses often receive many emails from customers inquiring about products, reporting issues, or requesting assistance. Responding to, or escalating inquiries efficiently requires significant effort. This project leverages AI to automate email management, providing timely responses and improving customer satisfaction.

The goal is to develop an AI agent that can:
1. Read and classify emails based on intent or actionable categories.
2. Generate responses using a company knowledge base.
3. Escalate by creating tickets when necessary.
4. Log actions and maintain reports.

## 02. AI Agent Workflow

![AI_Agent_workflow](resources/ai_agent_workflow.png)


The AI agent checks emails at regular intervals using a scheduler. Once new emails are received, they are fetched from the client. After fetching new email(s), the **reasoning engine** is activated. The reasoning engine read the email, take actions, and generates a response email. Then the AI agent reply to the customer

### Reasoning Engine tasks:

#### The reasoning engine is responsible for the core functionalities and actions of the AI agent.

1. Read the email body to classify intent and reason from the input data.
2. Decide actions using an LLM:
    - Determine if knowledge from the vector database (Chromadb) is required to generate a reply email.
    - Identify if a ticket should be created and create tickets in a remote SQL Database.
    - Gather relevant ticket information, including problem description, intent class, reason, and email metadata.
3. Generate a response email using LLM based on the email body, intent, and gathered context (including ticket numbers if created).
4. Log activities in Google Sheets.

### Actions taken:
- Create tickets via a remote database connection if required.
- Send customer response emails, including the gathered context and ticket number if applicable.
- Log activities into a database for tracking and reporting.

### Tools involved:
- Email client: fetching emails and replying to them.
- Vector Database:  Extracting context from the knowledge base.
- Remote SQL Database: Create tickets.
- Google Sheets: Log AI Agent activities.

### Technologies utilized
- Python 3.10 and related libs.
- FastAPI: REST API Application.
- Docker: Deploy the containerised application.
- LangChain: To create a chain to run LLM, prompt and tools.
- OpenRouter API (keys) for LLMs: LLM invokation are done with API endopoints (Llama 3.2 30b).
- Google APIs: Build connections to Google Gmail client and app API to Google Sheets.

## 03. How to Run

### <ins>Run Locally</ins>

#### (a) Using Docker
1. Install Docker:

2. Build the Docker image:
   ```bash
   docker build -t crm-ai-agent .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 --env-file .env --name crm-ai-agent crm-ai-agent
   ```
4. Access the application at `http://localhost:8000`.

#### (b) Without Docker
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
### <ins>Deploy in Cloud (AWS EC2 instance)</ins>

#### Prerequisites
- AWS EC2 Instance: Ensure you have an EC2 instance running with SSH access.
- SSH Key Pair: A key pair (.pem file) associated with your EC2 instance.
- Docker and Docker Compose: Installed on your local machine and EC2 instance.

#### (a) Deploy (automated) with CI/CD pipeline (GitHub Actions)

1. Configure SSH access: Get the Key Pair credentials file (.pem) and add it as a GitHub secret named `EC2_SSH_KEY`
2. Setup GitHub Secrets: Add `EC2_HOST` (Public IP or DNS of the EC2 instance) and `EC2_USER` (SSH username such as `ubuntu` for Ubuntu instance)
3.  When changes are pushed to the `deploy` branch (or your desired branch), the GitHub Actions workflow is triggered (located in `.github/workflows/deploy.yml`).

#### The CI/CD pipeline performs the following actions:
- Check out to code/repo.
- Set up SSH access to EC2 instance.
- Copy files to the EC2 instance (Volumes).
- Install Docker on the EC2 instance.
- Deploy the AI Agent by building (image) and running the Docker container.

#### (b) Deploy (manual) with Docker (for Linux/macOS):

1. Create an IAM Role with `AmazonEC2ContainerRegistryFullAccess` policy and attach with the EC2 instance.
2. Configure the local machine: Adjust permissions of the Key Pair file (navigate to its location).
   ```bash 
   chmod 400 your-key.pem
   ``` 
3. Connect to the EC2 instance using SSH.
   ```bash 
   ssh -i "your-key.pem" ubuntu@<EC2-Public-IP>
   ``` 
4. Navigate to the project in your local machine and transfer files to the EC2 instance.
   ```bash 
   scp -i "your-key.pem" -r <my_project> ubuntu@<EC2-Public-IP>:/home/ubuntu/
   ```
5. Verify transferred files by SSH back to the EC2 instance and check in `/home/ubuntu` dir.
6. Build and Run the Dockerized App: Build the Docker images and run the Docker container (port 80 is the default HTTP port in EC2 instance).
   ```bash 
   docker build -t crm-ai-agent .
   docker run -p 80:8000 --env-file .env --name crm-ai-agent crm-ai-agent
   ```
7. The AI Agent is now running in the EC2 instance as a Docker container. Access it via `http://<EC2-Public-IP>:80`

## 04. Future Work
- Enhance the knowledge base with additional sources.
- Integrate with advanced ticketing systems.
- Add a dashboard for analytics and reporting.
- Add memory functions to maintain email conversations with back-and-forth communication.
- Add a control panel to monitor agent activities.

---
Remarks:
This project was conducted as a learning exercise to build a basic AI Agent. Feel free to create an issue if you find any problems or feedback (both positive and negative). Feel free to reach out for any clarifications or suggestions. Thank you for checking this repository out



