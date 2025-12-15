from redis import Redis
from rq_scheduler.scheduler import Scheduler
from datetime import timedelta
from app.services.documents import DocumentService
from app.db.session import SessionLocal
import asyncio

def delete_old_documents_job():
    """
    A scheduled job to delete documents older than a certain number of days.
    """
    async def run():
        db = SessionLocal()
        try:
            # The TTL is currently hardcoded to 30 days.
            # In a real application, this should be configurable.
            await DocumentService.delete_old_documents(db, days=30)
        finally:
            await db.close()

    asyncio.run(run())


def main():
    # Note: Ensure REDIS_URL is configured in your environment.
    # The URL is loaded via `settings.REDIS_URL` in the main app, 
    # but you might need to load it explicitly if running this script directly.
    from app.core.config import settings
    
    redis_conn = Redis.from_url(settings.REDIS_URL)
    scheduler = Scheduler(connection=redis_conn)

    # Schedule the job to run every day
    scheduler.schedule(
        scheduled_time=timedelta(days=1),
        func=delete_old_documents_job,
        interval=timedelta(days=1).total_seconds(),
        repeat=None, # Run indefinitely
    )

if __name__ == "__main__":
    main()