# backend/tests/services/test_reader_agent.py

import pytest

from app.services.reader_agent import ReaderAgent
from app.schemas.orchestrator import ConversationContext, WorkflowState


@pytest.fixture
def reader_agent() -> ReaderAgent:
    return ReaderAgent()


def make_context(text: str) -> ConversationContext:
    """
    Helper to construct a ConversationContext in the same shape the
    orchestrator would use in production.
    """
    return ConversationContext(
        session_id="test-session",
        state=WorkflowState.UPLOADED,
        current_document={"text": text},
        history=[],
        last_agent_used=None,
    )


def test_reader_agent_produces_analysis_entry(reader_agent: ReaderAgent) -> None:
    """
    ReaderAgent should add an analysis entry to the context history and mark
    itself as the last agent used.
    """

    raw_text = """My Sample Document

INTRODUCTION:
- First key point
- Second key point
This report must be completed by Friday.
"""

    ctx = make_context(raw_text)

    updated = reader_agent.process(ctx)

    # ReaderAgent should have been recorded as last agent
    assert updated.last_agent_used == "reader_agent"

    # History should contain at least one entry
    assert updated.history, "Expected at least one history entry"
    last_entry = updated.history[-1]

    assert last_entry.get("agent") == "reader_agent"
    analysis = last_entry.get("analysis")
    assert isinstance(analysis, dict), "Expected 'analysis' dict in history entry"

    # Basic structure checks
    assert analysis.get("title") == "My Sample Document"
    assert "INTRODUCTION:" in analysis.get("headings", [])
    assert analysis.get("doc_type") == "report"
    assert isinstance(analysis.get("summary"), str)
    assert analysis.get("summary"), "Summary should not be empty"

    key_points = analysis.get("key_points", [])
    assert len(key_points) > 0
    # We truncate at 5, so it should never exceed 5
    assert len(key_points) <= 5


def test_reader_agent_handles_empty_text(reader_agent: ReaderAgent) -> None:
    """
    When there is no text in the current_document, the agent should not crash
    and should record an error entry instead.
    """

    ctx = make_context("")

    updated = reader_agent.process(ctx)

    assert updated.last_agent_used == "reader_agent"
    assert updated.history, "Expected an error entry in history"

    last_entry = updated.history[-1]
    assert last_entry.get("agent") == "reader_agent"
    assert "error" in last_entry
    assert "No text found" in last_entry["error"]
