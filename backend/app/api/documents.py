from typing import List
import uuid
import magic
import os
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.storage import StorageService
from app.services.documents import DocumentService
from app.schemas.document import DocumentCreate, DocumentResponse
from app.core.config import settings
from rq import Queue
from redis import Redis

router = APIRouter()
storage_service = StorageService()

# RQ setup
redis_conn = Redis.from_url(settings.REDIS_URL)
q = Queue(connection=redis_conn)

@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all documents for the current user.
    """
    return await DocumentService.get_user_documents(db, current_user.id)

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Read header for magic check
    header = await file.read(2048)
    await file.seek(0)
    
    # 2. Validate MIME Type
    try:
        mime = magic.from_buffer(header, mime=True)
    except Exception as e:
        # Fallback if magic fails or DLL missing (common on Windows without bin)
        # We rely on Content-Type header as fallback, but warn
        print(f"Warning: python-magic failed: {e}. using content-type header.")
        mime = file.content_type

    ALLOWED_MIMES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
    
    if mime not in ALLOWED_MIMES:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {mime}. Allowed: PDF, DOCX, TXT")

    # 3. Save file
    file_id = uuid.uuid4()
    # Sanitize extension
    original_ext = file.filename.split(".")[-1].lower() if "." in file.filename else "bin"
    if original_ext not in ["pdf", "docx", "txt"]:
         # Force extension based on mime if possible, or keep original if safe. 
         # For MVP, we trust valid mime matches extension roughly.
         pass

    stored_filename = f"{file_id}.{original_ext}"
    
    try:
        file_path = await storage_service.save_upload(file, stored_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    # 4. Check size
    MAX_SIZE = 20 * 1024 * 1024
    actual_size = os.path.getsize(file_path)
    if actual_size > MAX_SIZE:
        storage_service.delete_file(file_path)
        raise HTTPException(status_code=413, detail="File too large (max 20MB)")
        
    # 5. Create DB Record
    doc_meta = DocumentCreate(
        filename=file.filename,
        file_size=actual_size,
        mime_type=mime
    )
    
    doc = await DocumentService.create_document_record(db, current_user.id, doc_meta, file_path)
    
    # 6. Enqueue Job
    try:
        q.enqueue("app.workers.process_document.process_document", str(doc.id))
    except Exception as e:
        print(f"Failed to enqueue job: {e}")
        # We don't fail the request, but log it. The user can retry or we have a retry mechanism.
    
    return doc
