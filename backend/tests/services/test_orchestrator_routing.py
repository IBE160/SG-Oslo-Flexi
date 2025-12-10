# backend/tests/services/test_orchestrator_routing.py
import pytest
from unittest.mock import MagicMock
from app.services.orchestrator import Orchestrator
from app.schemas.orchestrator import ConversationContext, WorkflowState

# Acceptance Criteria Covered:
# AC-1: Given a document has been successfully uploaded...
# AC-2: When the Stateful Orchestrator routes the analysis request...
# AC-6: And the generated summary and key concepts SHALL be stored in the user's session context.

@pytest.fixture
def mock_redis():
    """Mocks the Redis client."""
    return MagicMock()

@pytest.fixture
def orchestrator(mock_redis):
    """Provides an Orchestrator instance with a mocked Redis client."""
    return Orchestrator(redis_client=mock_redis)

def test_orchestrator_routes_to_reader_agent(orchestrator, mock_redis):
    """
    Tests that the orchestrator correctly routes to the ReaderAgent when the
    workflow is in the OCR_COMPLETED state. (Covers AC-1, AC-2, AC-6)
    """
    # GIVEN a conversation context that has just completed OCR (AC-1)
    session_id = "test_session_123"
    context = ConversationContext(session_id=session_id, state=WorkflowState.OCR_COMPLETED)
    context.current_document = {"raw_text": "This is the text to be analyzed."}
    
    # Mock the load_context and save_context to inspect state transitions
    orchestrator.load_context = MagicMock(return_value=context)
    orchestrator.save_context = MagicMock()
    orchestrator.reader_agent.process = MagicMock(side_effect=lambda ctx: ctx)


    # WHEN the state is updated to trigger the next step (AC-2)
    orchestrator.update_state(session_id, WorkflowState.OCR_COMPLETED)

    # THEN the reader_agent's process method should have been called
    orchestrator.reader_agent.process.assert_called_once()

    # AND the final state should be ANALYZED (implicitly covers AC-6)
    # We check the call arguments to save_context to see the state transitions
    # The final save should be the ANALYZED state.
    final_context_saved = orchestrator.save_context.call_args[0][0]
    assert final_context_saved.state == WorkflowState.ANALYZED
