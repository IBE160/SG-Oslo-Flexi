import time
from app.services.reader_agent import ReaderAgent
from app.schemas.orchestrator import ConversationContext

def test_reader_agent_performance_under_500ms():
    # Create a large synthetic document (~5MB of text)
    large_text = ("This is a test sentence. " * 20000)  # ~5.2 MB

    ctx = ConversationContext(
        session_id="perf-test",
        current_document={"text": large_text},
        history=[]
    )

    agent = ReaderAgent()

    start = time.perf_counter()
    updated = agent.process(ctx)
    end = time.perf_counter()

    duration_ms = (end - start) * 1000

    # Must be under 500ms according to NFR8.1.1
    assert duration_ms <= 500, f"ReaderAgent took too long: {duration_ms:.2f} ms"

    # Make sure output was updated (sanity check)
    assert updated.last_agent_used == "reader_agent"
    assert "analysis" in updated.history[-1]
