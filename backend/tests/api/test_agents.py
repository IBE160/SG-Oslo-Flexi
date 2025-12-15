from httpx import AsyncClient
from app.schemas.orchestrator import ConversationContext, WorkflowState

async def test_generate_summary_success(client: AsyncClient, mocker):
    # 1. Mock the CoachAgent
    mock_coach_agent = mocker.patch("app.api.agents.coach_agent")
    mock_coach_agent.process.return_value = ConversationContext(
        session_id="test-session",
        state=WorkflowState.COMPLETED,
        history=[{"agent": "coach_agent", "summary": "This is a test summary."}]
    )

    # 2. Call the endpoint
    response = await client.post(
        "/api/v1/agents/coach/generate/summary",
        json={"session_id": "test-session", "state": "analyzed"}
    )

    # 3. Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session"
    assert data["state"] == "completed"
    assert data["history"][-1]["summary"] == "This is a test summary."

async def test_generate_flashcards_success(client: AsyncClient, mocker):
    # 1. Mock the CoachAgent
    mock_coach_agent = mocker.patch("app.api.agents.coach_agent")
    mock_coach_agent.process.return_value = ConversationContext(
        session_id="test-session",
        state=WorkflowState.COMPLETED,
        history=[{"agent": "coach_agent", "flashcards": [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 2 + 2?", "answer": "4"}
        ]}]
    )

    # 2. Call the endpoint
    response = await client.post(
        "/api/v1/agents/coach/generate/flashcards",
        json={"session_id": "test-session", "state": "analyzed"}
    )

    # 3. Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session"
    assert data["state"] == "completed"
    assert data["history"][-1]["flashcards"] == [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "What is 2 + 2?", "answer": "4"}
    ]

async def test_generate_quiz_success(client: AsyncClient, mocker):
    # 1. Mock the CoachAgent
    mock_coach_agent = mocker.patch("app.api.agents.coach_agent")
    mock_coach_agent.process.return_value = ConversationContext(
        session_id="test-session",
        state=WorkflowState.COMPLETED,
        history=[{"agent": "coach_agent", "quiz": [
            {
                "question": "What is the capital of France?",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris"
            },
            {
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4"
            }
        ]}]
    )

    # 2. Call the endpoint
    response = await client.post(
        "/api/v1/agents/coach/generate/quiz",
        json={"session_id": "test-session", "state": "analyzed"}
    )

    # 3. Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session"
    assert data["state"] == "completed"
    assert data["history"][-1]["quiz"] == [
        {
            "question": "What is the capital of France?",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correct_answer": "Paris"
        },
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "4"
        }
    ]
