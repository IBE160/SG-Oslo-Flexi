from fastapi import APIRouter, HTTPException
from redis import Redis
from rq import Queue
from app.core.config import settings
from app.workers.tasks import test_task

router = APIRouter()

@router.post("/queue/test-task", status_code=201)
def enqueue_test_task(seconds: int = 5):
    """
    Enqueue a test task.
    """
    try:
        redis_conn = Redis.from_url(settings.REDIS_URL)
        q = Queue(connection=redis_conn)
        job = q.enqueue(test_task, seconds)
        return {"job_id": job.get_id(), "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enqueue task: {str(e)}")
