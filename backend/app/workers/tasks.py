import time
import logging
from redis import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

def test_task(seconds: int = 5):
    """
    A simple task to verify the worker is running.
    """
    logger.info(f"Starting test_task, sleeping for {seconds} seconds...")
    time.sleep(seconds)
    logger.info("Finished test_task.")
    return "Task Completed"

def process_ocr_task(session_id: str):
    """
    Simulates OCR processing.
    """
    logger.info(f"Starting OCR for session {session_id}")
    time.sleep(2) # Simulate work
    
    # Update state to ANALYZED (skipping generic 'processing' for now, or moving to next step)
    # In a real app, we might update to "OCR_DONE" then trigger "ANALYSIS"
    # For this skeleton, let's assume this task does the OCR part.
    
    # We need to update the state in Redis.
    # We can't easily inject the Orchestrator service here without circular imports or setup complexity,
    # so we'll do a quick manual update or a fresh service instance.
    
    from app.services.orchestrator import Orchestrator
    from app.schemas.orchestrator import WorkflowState
    
    redis_conn = Redis.from_url(settings.REDIS_URL)
    orchestrator = Orchestrator(redis_conn)
    
    # Update state
    orchestrator.update_state(session_id, WorkflowState.ANALYZED)
    logger.info(f"OCR completed for session {session_id}, state updated to ANALYZED")
    return "OCR Completed"