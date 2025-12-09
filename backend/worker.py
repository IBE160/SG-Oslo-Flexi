import asyncio
from app.db.session import AsyncSessionLocal
from app.services.documents import DocumentService
from app.services.ocr_service import OCRService
from app.models.document import DocumentStatus
from app.core.config import settings
from redis import Redis
from rq import Queue

# Setup Redis connection for RQ
redis_conn = Redis.from_url(settings.REDIS_URL)

async def process_document_async(document_id: str):
    """
    Async implementation of document processing logic.
    """
    async with AsyncSessionLocal() as db:
        # 1. Fetch Document
        doc = await DocumentService.get_document(db, document_id)
        if not doc:
            print(f"Document {document_id} not found.")
            return

        # 2. Update Status -> PROCESSING
        await DocumentService.update_status(db, doc, DocumentStatus.PROCESSING)
        print(f"Processing document {document_id} ({doc.filename})...")

        try:
            # 3. Extract Text (OCR)
            extracted_text = await OCRService.extract_text(doc.file_path, doc.mime_type)
            
            # 4. Save Text & Update Status -> COMPLETED
            await DocumentService.update_extracted_text(db, doc, extracted_text)
            await DocumentService.update_status(db, doc, DocumentStatus.COMPLETED)
            print(f"Document {document_id} processed successfully.")

        except Exception as e:
            print(f"Error processing document {document_id}: {e}")
            await DocumentService.update_status(db, doc, DocumentStatus.FAILED)

def process_document(document_id: str):
    """
    RQ Task Entry Point (Synchronous wrapper for async code).
    """
    asyncio.run(process_document_async(document_id))