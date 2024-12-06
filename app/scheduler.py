from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tasks.email_processor import EMail_Processor
from ai_agent import AI_Agent

# Act as the centralized task manager to orchestrate tasks.
class Scheduler():
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.ai_agent = AI_Agent()

    def start(self): 
        self.scheduler.add_job(self.ai_agent.run_ai_agent, 'interval', minutes=3)
        self.scheduler.start()

    def shutdown(self):
        self.scheduler.shutdown()