import os
import tempfile
import pytest
from app.services.storage import StorageService

@pytest.fixture
def storage_service():
    """Pytest fixture to provide a StorageService instance."""
    # To avoid interfering with actual uploads, point to a test-specific dir
    # This assumes the StorageService will create it if it doesn't exist
    original_upload_dir = StorageService().upload_dir
    test_upload_dir = os.path.join(os.path.dirname(original_upload_dir), 'test_uploads')
    
    # Temporarily change the upload_dir for the service instance
    service = StorageService()
    service.upload_dir = test_upload_dir
    os.makedirs(service.upload_dir, exist_ok=True)
    
    yield service
    
    # Teardown: Clean up the test upload directory
    import shutil
    if os.path.exists(test_upload_dir):
        shutil.rmtree(test_upload_dir)


def test_delete_file_success(storage_service: StorageService):
    """
    Tests that the delete_file method successfully removes a file.
    """
    # 1. Create a temporary file in the service's test upload directory
    with tempfile.NamedTemporaryFile(delete=False, dir=storage_service.upload_dir) as tmp_file:
        temp_path = tmp_file.name
    
    assert os.path.exists(temp_path), "Precondition: Temp file should exist."

    # 2. Call the delete method
    storage_service.delete_file(temp_path)

    # 3. Assert the file is deleted
    assert not os.path.exists(temp_path), "Postcondition: Temp file should not exist."

def test_delete_non_existent_file(storage_service: StorageService):
    """
    Tests that calling delete_file on a non-existent file does not raise an error.
    """
    non_existent_path = os.path.join(storage_service.upload_dir, "non_existent_file.tmp")
    
    try:
        storage_service.delete_file(non_existent_path)
    except Exception as e:
        pytest.fail(f"delete_file raised an unexpected exception for a non-existent file: {e}")
