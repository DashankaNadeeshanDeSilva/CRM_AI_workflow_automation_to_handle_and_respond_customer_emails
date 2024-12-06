from fastapi import FastAPI
from scheduler import Scheduler
import logging

logger = logging.getLogger("CRM AI Agent")

app = FastAPI(
    title="CRM AI Agent",
    description="Processes recieved emails and provide responses including creating tickets",
    version="1.0.0",
)

scheduler = Scheduler()

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