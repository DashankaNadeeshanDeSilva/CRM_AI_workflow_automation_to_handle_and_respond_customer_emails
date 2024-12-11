from fastapi import FastAPI
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ai_agent import AI_Agent

logger = logging.getLogger("CRM AI Agent")

app = FastAPI(
    title="CRM AI Agent",
    description="Processes recieved emails and provide responses including creating tickets",
    version="1.0.0",
)

# Act as the centralized task manager to orchestrate scheduler tasks.
class Scheduler():
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.ai_agent = AI_Agent()

    def start(self): 
        self.scheduler.add_job(self.ai_agent.run_ai_agent, 'interval', minutes=2)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()


scheduler = Scheduler()

# scheduler events
@app.on_event("startup")
def start_app():
    logger.info("Starting CRM AI Agent...")
    scheduler.start()


@app.on_event("shutdown")
def shutdown_app():
    logger.info("Shutting down CRM AI Agent...")
    scheduler.shutdown()


@app.get("/")
def root():
    return {"message": "Welcome to the CRM AI Agent"}