import os
import uuid
from fastapi import UploadFile
from app.core.config import settings

class StorageService:
    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    async def save_temporary_file(self, file: UploadFile) -> str:
        """
        Saves an uploaded file to a temporary directory with a unique name.
        Returns the unique filename.
        """
        _, file_extension = os.path.splitext(file.filename)
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return unique_filename

    def get_file_path(self, filename: str) -> str:
        """
        Gets the full path to a stored file.
        """
        return os.path.join(self.upload_dir, filename)

    def delete_temporary_file(self, filename: str):
        """
        Deletes a file from the temporary directory.
        """
        try:
            os.remove(self.get_file_path(filename))
        except OSError:
            # Handle cases where file might not exist, etc.
            pass

storage_service = StorageService()
