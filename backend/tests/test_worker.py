import pytest
import worker
from worker import schedule_jobs

def test_schedule_cleanup_job(mocker):
    """
    Tests that the cleanup_old_documents job is scheduled correctly.
    """
    # Mock the scheduler instance in the worker module
    mock_scheduler = mocker.patch('worker.scheduler')
    
    # Run the function
    schedule_jobs()

    # Verify schedule was called
    assert mock_scheduler.schedule.call_count == 1
    
    # Get the arguments passed to schedule
    # schedule is called with keyword arguments in worker.py
    call_kwargs = mock_scheduler.schedule.call_args.kwargs
    
    # Verify the arguments
    assert call_kwargs['func'] == worker.cleanup_old_documents
    assert call_kwargs['interval'] == 60 * 60 * 24
