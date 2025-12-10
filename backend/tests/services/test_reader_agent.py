import pytest
from unittest.mock import patch
from backend.app.services.reader_agent import ReaderAgent, ConversationContext
import json

# Acceptance Criteria Covered:
# AC-4: And the agent SHALL generate a concise summary of the document.
# AC-5: And the agent SHALL extract a list of key concepts from the document.
# AC-6: And the generated summary and key concepts SHALL be stored in the user's session context.

@pytest.fixture
def reader_agent():
    """Provides a ReaderAgent instance for testing."""
    return ReaderAgent()

@patch('backend.app.services.reader_agent.ReaderAgent._call_llm')
def test_reader_agent_parses_llm_response(mock_call_llm, reader_agent):
    """
    Tests that the ReaderAgent correctly parses the simulated LLM response
    and updates the context object. (Covers AC-4, AC-5, AC-6)
    """
    # GIVEN a mock LLM response
    mock_response = {
        "analysis": {
            "summary": "This is a mock summary.",
            "key_concepts": ["MockConcept1", "MockConcept2"]
        }
    }
    mock_call_llm.return_value = json.dumps(mock_response)
    
    # AND raw text is available in the context
    raw_text = "This text will be sent to the mocked LLM."
    context = ConversationContext(raw_text=raw_text)

    # WHEN the ReaderAgent processes the context
    updated_context = reader_agent.process(context)

    # THEN the _call_llm method should have been called
    mock_call_llm.assert_called_once_with(raw_text)

    # AND the context should be updated with data from the mock response
    assert updated_context.summary == "This is a mock summary."
    assert updated_context.key_concepts == ["MockConcept1", "MockConcept2"]

def test_reader_agent_handles_empty_text(reader_agent):
    """
    Tests that the ReaderAgent handles empty input gracefully without errors.
    """
    # GIVEN the context has no raw text
    context = ConversationContext(raw_text="")

    # WHEN the ReaderAgent processes the context
    updated_context = reader_agent.process(context)

    # THEN the summary and key concepts should be empty
    assert updated_context.summary == ""
    assert len(updated_context.key_concepts) == 0
