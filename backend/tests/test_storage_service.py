import os
import shutil
import pytest
from fastapi import UploadFile
from app.services.storage_service import StorageService
from app.core.config import settings
from io import BytesIO

TEST_UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "test_temp")

@pytest.fixture(scope="module")
def storage_service():
    # Setup: create a temporary test directory
    if not os.path.exists(TEST_UPLOAD_DIR):
        os.makedirs(TEST_UPLOAD_DIR)
    
    service = StorageService(upload_dir=TEST_UPLOAD_DIR)
    
    yield service
    
    # Teardown: remove the temporary test directory
    if os.path.exists(TEST_UPLOAD_DIR):
        shutil.rmtree(TEST_UPLOAD_DIR)

@pytest.mark.asyncio
async def test_save_and_delete_temporary_file(storage_service: StorageService):
    # Create a dummy file in memory
    file_content = b"hello world"
    file_object = BytesIO(file_content)
    upload_file = UploadFile(filename="test.txt", file=file_object)

    # Save the file
    unique_filename = await storage_service.save_temporary_file(upload_file)
    
    # Assert the file was created
    file_path = storage_service.get_file_path(unique_filename)
    assert os.path.exists(file_path)
    
    # Assert the content is correct
    with open(file_path, "rb") as f:
        content = f.read()
        assert content == file_content
        
    # Delete the file
    storage_service.delete_temporary_file(unique_filename)
    
    # Assert the file was deleted
    assert not os.path.exists(file_path)

def test_get_file_path(storage_service: StorageService):
    filename = "my-test-file.txt"
    expected_path = os.path.join(TEST_UPLOAD_DIR, filename)
    assert storage_service.get_file_path(filename) == expected_path
