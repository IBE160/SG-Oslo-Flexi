import pytest
from redis import Redis
from rq_scheduler import Scheduler
from app.core.config import settings
import worker
from worker import schedule_jobs

@pytest.fixture
def scheduler():
    """
    Provides a scheduler instance with a clean Redis connection.
    """
    redis_conn = Redis.from_url(settings.REDIS_URL)
    # Clear any existing schedules
    redis_conn.delete("rq:scheduler:scheduled_jobs")
    return Scheduler(connection=redis_conn)

def test_schedule_cleanup_job(scheduler: Scheduler):
    """
    Tests that the cleanup_old_documents job is scheduled correctly.
    """
    # Schedule the jobs
    schedule_jobs()

    # Get the scheduled jobs
    jobs = scheduler.get_jobs()

    # Check that there is one scheduled job
    assert len(jobs) == 1

    # Check that the scheduled job is the cleanup job
    job = jobs[0]
    # The function is in the 'worker' module, so the name should be 'worker.cleanup_old_documents'
    assert job.func_name == "worker.cleanup_old_documents"
    assert job.meta["interval"] == 60 * 60 * 24