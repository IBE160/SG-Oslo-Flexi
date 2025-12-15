import asyncio
from datetime import datetime, timedelta
from app.db.session import AsyncSessionLocal
from app.services.documents import DocumentService
from app.services.ocr_service import OCRService
from app.models.document import DocumentStatus, Document
from app.core.config import settings
from redis import Redis
from sqlalchemy import select
from rq_scheduler import Scheduler

# Setup Redis connection for RQ
redis_conn = Redis.from_url(settings.REDIS_URL)
scheduler = Scheduler(connection=redis_conn)

def schedule_jobs():
    """
    Schedules the periodic jobs.
    """
    # Schedule the cleanup job to run daily
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=cleanup_old_documents,
        interval=60 * 60 * 24,  # daily
        repeat=None # repeat indefinitely
    )

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

async def cleanup_old_documents_async():
    """
    Async implementation of the cleanup logic for old documents.
    """
    print("Starting cleanup of old documents...")
    async with AsyncSessionLocal() as db:
        # Define the TTL (e.g., 30 days)
        ttl_limit = datetime.utcnow() - timedelta(days=30)
        
        # Find old documents
        result = await db.execute(
            select(Document).where(Document.created_at < ttl_limit)
        )
        old_documents = result.scalars().all()
        
        if not old_documents:
            print("No old documents to clean up.")
            return

        print(f"Found {len(old_documents)} old documents to delete.")
        
        # Delete each old document
        for doc in old_documents:
            try:
                print(f"Deleting document {doc.id} (owner: {doc.user_id})...")
                # Note: The user_id is passed to enforce ownership checks if any,
                # but for a system cleanup task, we might have different rules.
                # Assuming the service method can handle system-level deletions.
                await DocumentService.delete_document(db, doc.id, doc.user_id)
                print(f"Successfully deleted document {doc.id}.")
            except Exception as e:
                print(f"Failed to delete document {doc.id}: {e}")
    
    print("Finished cleanup of old documents.")

def cleanup_old_documents():
    """
    RQ Task Entry Point for cleaning up old documents.
    """
    asyncio.run(cleanup_old_documents_async())

if __name__ == "__main__":
    schedule_jobs()