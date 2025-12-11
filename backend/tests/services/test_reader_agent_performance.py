# backend/tests/services/test_reader_agent_performance.py

import time

import pytest

from app.services.reader_agent import ReaderAgent
from app.schemas.orchestrator import ConversationContext, WorkflowState

LARGE_TEXT_SAMPLE = "This is a test sentence. " * 10_000  # ~2.6MB of text


@pytest.fixture
def reader_agent_with_simulated_delay() -> ReaderAgent:
    """
    For now the ReaderAgent is purely CPU-bound and fast, so we just
    use the real implementation. If we later introduce network calls
    to an LLM, this fixture can be extended to patch those out.
    """
    return ReaderAgent()


def make_context(text: str) -> ConversationContext:
    return ConversationContext(
        session_id="perf-test-session",
        state=WorkflowState.UPLOADED,
        current_document={"text": text},
        history=[],
        last_agent_used=None,
    )


def test_reader_agent_performance(reader_agent_with_simulated_delay: ReaderAgent) -> None:
    """
    Validates that the ReaderAgent completes its analysis within the
    non-functional requirement NFR8.1.1 (under 500ms for a multi-MB document).

    This complements the dedicated performance test in
    tests/performance/test_reader_agent_performance.py by exercising
    the same path through the service layer.
    """

    ctx = make_context(LARGE_TEXT_SAMPLE)

    start = time.perf_counter()
    updated = reader_agent_with_simulated_delay.process(ctx)
    duration_ms = (time.perf_counter() - start) * 1000

    # Core NFR: under 500 ms
    assert duration_ms < 500, f"ReaderAgent took {duration_ms:.2f}ms, exceeding 500ms budget"

    # Basic sanity: we should have an analysis entry
    assert updated.history, "Expected at least one history entry"
    last_entry = updated.history[-1]
    assert last_entry.get("agent") == "reader_agent"
    assert "analysis" in last_entry
