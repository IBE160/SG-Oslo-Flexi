from fastapi import APIRouter
from app.schemas.orchestrator import ConversationContext
from app.services.coach_agent import CoachAgent

router = APIRouter()
coach_agent = CoachAgent()

@router.post("/coach/generate/summary")
def generate_summary(
    context: ConversationContext,
) -> ConversationContext:
    """
    Generates a summary for the document in the conversation context.
    """
    return coach_agent.process(context, "generate_summary")

@router.post("/coach/generate/flashcards")
def generate_flashcards(
    context: ConversationContext,
) -> ConversationContext:
    """
    Generates flashcards for the document in the conversation context.
    """
    return coach_agent.process(context, "generate_flashcards")

@router.post("/coach/generate/quiz")
def generate_quiz(
    context: ConversationContext,
) -> ConversationContext:
    """
    Generates a quiz for the document in the conversation context.
    """
    return coach_agent.process(context, "generate_quiz")
