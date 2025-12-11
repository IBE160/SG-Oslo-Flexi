import os
import aiofiles
from fastapi import UploadFile
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    async def save_upload(self, file: UploadFile, filename: str) -> str:
        file_path = os.path.join(self.upload_dir, filename)
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # Read 1MB chunks
                await out_file.write(content)
        
        return file_path

    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
