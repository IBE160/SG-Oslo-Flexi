from app.workers.tasks import test_task

def test_test_task_execution():
    # Verify the task function runs successfully (without queue)
    result = test_task(seconds=0)
    assert result == "Task Completed"
