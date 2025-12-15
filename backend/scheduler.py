from redis import Redis
from rq_scheduler.scheduler import Scheduler
from datetime import datetime, timedelta
from app.services.documents import DocumentService
from app.db.session import SessionLocal
import asyncio
from app.core.config import settings

def delete_old_documents_job():
    """
    A scheduled job to delete documents older than configured TTL.
    """
    async def run():
        db = SessionLocal()
        try:
            await DocumentService.delete_old_documents(db, ttl_hours=settings.DOCUMENT_TTL_HOURS)
        finally:
            await db.close()

    asyncio.run(run())


def main():
    redis_conn = Redis.from_url(settings.REDIS_URL)
    scheduler = Scheduler(connection=redis_conn)

    # Schedule the job to run every hour
    # Start immediately (UTC now)
    scheduler.schedule(
        scheduled_time=datetime.utcnow(), 
        func=delete_old_documents_job,
        interval=3600, # 1 hour in seconds
        repeat=None, # Run indefinitely
    )

if __name__ == "__main__":
    main()
