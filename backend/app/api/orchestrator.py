import logging
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis
from app.core.config import settings
from app.services.orchestrator import Orchestrator
from app.schemas.orchestrator import ConversationContext
from app.services.storage_service import storage_service
from app.db.session import get_db
from app.models.document import Document
from app.models.user import User
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

def get_orchestrator():
    redis_conn = Redis.from_url(settings.REDIS_URL)
    return Orchestrator(redis_conn)

@router.post("/upload", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    orchestrator: Orchestrator = Depends(get_orchestrator)
):
    """
    Upload a document, save it securely, and start the processing workflow.
    """
    try:
        unique_filename = await storage_service.save_temporary_file(file)
        # This is a temporary solution for development until a proper auth system is in place.
        # It retrieves the first user from the database to act as the document owner.
        result = await db.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="No users found in the database. Please seed the database.")

        new_document = Document(
            user_id=user.id,
            filename=file.filename,
            file_path=storage_service.get_file_path(unique_filename),
            mime_type=file.content_type,
            file_size=file.size
        )
        db.add(new_document)
        await db.commit()
        await db.refresh(new_document)

        session_id = str(uuid.uuid4())
        context = orchestrator.start_workflow(session_id)
        context.current_document = {
            "id": str(new_document.id),
            "original_filename": new_document.filename
        }
        orchestrator.save_context(context)
        
        return {"session_id": session_id, "document_id": str(new_document.id)}
    except Exception as e:
        logger.exception("Error during document upload")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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

@router.post("/{session_id}/summarize", response_model=ConversationContext)
def summarize_document(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Request a summary for the document in the workflow session.
    """
    context = orchestrator.request_summary(session_id)
    if not context:
        raise HTTPException(status_code=404, detail="Session not found or not in a valid state for summarization.")
    return context

@router.post("/{session_id}/flashcards", response_model=ConversationContext)
def flashcards_document(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Request flashcards for the document in the workflow session.
    """
    context = orchestrator.request_flashcards(session_id)
    if not context:
        raise HTTPException(status_code=404, detail="Session not found or not in a valid state for flashcard generation.")
    return context

@router.post("/{session_id}/quiz", response_model=ConversationContext)
def quiz_document(session_id: str, orchestrator: Orchestrator = Depends(get_orchestrator)):
    """
    Request a quiz for the document in the workflow session.
    """
    context = orchestrator.request_quiz(session_id)
    if not context:
        raise HTTPException(status_code=404, detail="Session not found or not in a valid state for quiz generation.")
    return context
