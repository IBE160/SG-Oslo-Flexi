from unittest import mock
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from app.main import app

client = TestClient(app)

@mock.patch("app.api.health.Redis.from_url")
def test_health_redis(mock_redis_from_url):
    # Mock successful connection
    mock_redis_instance = mock.Mock()
    mock_redis_instance.ping.return_value = True
    mock_redis_from_url.return_value = mock_redis_instance

    response = client.get("/health/redis")
    assert response.status_code == 200
    assert response.json() == {"status": "connected"}

@mock.patch("app.api.health.Redis.from_url")
def test_health_redis_failure(mock_redis_from_url):
    # Mock failure
    mock_redis_from_url.side_effect = Exception("Connection refused")

    response = client.get("/health/redis")
    assert response.status_code == 503
    assert "Redis connection failed" in response.json()["detail"]

@mock.patch("app.api.queue.Queue")
@mock.patch("app.api.queue.Redis.from_url")
def test_enqueue_task(mock_redis, mock_queue):
    # Mock queue enqueue
    mock_job = mock.Mock()
    mock_job.get_id.return_value = "job-123"
    
    mock_queue_instance = mock.Mock()
    mock_queue_instance.enqueue.return_value = mock_job
    mock_queue.return_value = mock_queue_instance

    response = client.post("/queue/test-task?seconds=2")
    assert response.status_code == 201
    assert response.json() == {"job_id": "job-123", "status": "queued"}
    
    mock_queue_instance.enqueue.assert_called_once()
