from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class WorkflowState(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    OCR = "ocr"
    ANALYZED = "analyzed"
    COMPLETED = "completed"
    FAILED = "failed"

class ConversationContext(BaseModel):
    session_id: str
    state: WorkflowState = WorkflowState.UPLOADED
    history: List[Dict[str, Any]] = Field(default_factory=list)
    current_document: Optional[Dict[str, Any]] = None
    last_agent_used: Optional[str] = None

