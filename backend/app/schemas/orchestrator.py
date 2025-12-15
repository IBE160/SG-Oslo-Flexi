from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class WorkflowState(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    OCR = "ocr"
    OCR_COMPLETED = "ocr_completed"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    SUMMARIZING = "summarizing"
    GENERATING_FLASHCARDS = "generating_flashcards"
    GENERATING_QUIZ = "generating_quiz"
    COMPLETED = "completed"
    FAILED = "failed"

class ConversationContext(BaseModel):
    session_id: str
    state: WorkflowState = WorkflowState.UPLOADED
    history: List[Dict[str, Any]] = Field(default_factory=list)
    current_document: Optional[Dict[str, Any]] = None
    last_agent_used: Optional[str] = None

