from fastapi import APIRouter, HTTPException, Depends
from redis import Redis
from app.core.config import settings
from app.services.orchestrator import Orchestrator
from app.schemas.orchestrator import ConversationContext
import uuid

router = APIRouter()

def get_orchestrator():
    redis_conn = Redis.from_url(settings.REDIS_URL)
    return Orchestrator(redis_conn)

@router.post("/start", response_model=ConversationContext)
def start_workflow(orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Start a new document processing workflow.
    """
    session_id = str(uuid.uuid4())
    return orchestrator.start_workflow(session_id)

@router.get("/{session_id}", response_model=ConversationContext)
def get_workflow_status(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Get the current status of a workflow session.
    """
    context = orchestrator.load_context(session_id)
    if not context:
        raise HTTPException(status_code=404, detail="Session not found")
    return context
