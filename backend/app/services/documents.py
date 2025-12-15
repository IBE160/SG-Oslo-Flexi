from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentCreate
from uuid import UUID
from fastapi import HTTPException, status
from app.services.storage import StorageService
from datetime import datetime, timedelta
import os

storage_service = StorageService()

class DocumentService:
    @staticmethod
    async def create_document_record(
        db: AsyncSession, 
        user_id: UUID, 
        meta: DocumentCreate, 
        file_path: str
    ) -> Document:
        db_obj = Document(
            user_id=user_id,
            filename=meta.filename,
            file_path=file_path,
            mime_type=meta.mime_type,
            file_size=meta.file_size,
            status=DocumentStatus.PENDING
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def get_document(db: AsyncSession, document_id: UUID) -> Document | None:
        return await db.get(Document, document_id)

    @staticmethod
    async def get_user_documents(db: AsyncSession, user_id: UUID) -> List[Document]:
        result = await db.execute(select(Document).where(Document.user_id == user_id).order_by(Document.created_at.desc()))
        return result.scalars().all()

    @staticmethod
    async def update_status(db: AsyncSession, doc: Document, status: DocumentStatus) -> Document:
        doc.status = status
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return doc

    @staticmethod
    async def update_extracted_text(db: AsyncSession, doc: Document, text: str) -> Document:
        doc.extracted_text = text
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        return doc

    @staticmethod
    async def _perform_document_deletion(db: AsyncSession, doc: Document) -> bool:
        """
        Internal method to delete a document and its file.
        Returns True if successful (or if file was missing but DB record deleted), False on critical error.
        This method handles exceptions internally for file deletion to ensuring DB cleanup proceeds.
        """
        # 1. Delete the physical file from storage
        try:
            if doc.file_path and os.path.exists(doc.file_path):
                storage_service.delete_file(doc.file_path)
        except Exception as e:
            # Log the error but proceed to delete the DB record
            print(f"Error deleting file {doc.file_path}: {e}")

        # 2. Delete the database record (cascades to flashcards, etc.)
        await db.delete(doc)
        # Note: Caller is responsible for commit() to allow batching or transaction control
        return True
    
    @staticmethod
    async def delete_document(db: AsyncSession, document_id: UUID, user_id: UUID):
        # 1. Fetch the document
        doc = await db.get(Document, document_id)

        # 2. Check existence and ownership
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        if doc.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this document")

        # 3. Perform deletion using shared logic
        await DocumentService._perform_document_deletion(db, doc)
        await db.commit()

    @staticmethod
    async def get_document_flashcards(db: AsyncSession, document_id: UUID, user_id: UUID) -> List:
        # 1. Fetch the document and its flashcards
        doc = await db.get(Document, document_id)

        # 2. Check existence and ownership
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        if doc.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this document")

        # 3. Return the flashcards
        return doc.flashcards

    @staticmethod
    async def get_document_quiz(db: AsyncSession, document_id: UUID, user_id: UUID):
        # 1. Fetch the document and its quiz
        doc = await db.get(Document, document_id)

        # 2. Check existence and ownership
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
        if doc.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this document")

        # 3. Return the quiz
        return doc.quiz

    @staticmethod
    async def delete_old_documents(db: AsyncSession, ttl_hours: int = 24) -> int:
        """
        Deletes documents older than the specified TTL in hours.
        """
        cutoff_date = datetime.utcnow() - timedelta(hours=ttl_hours)
        
        # Find documents older than the cutoff date
        result = await db.execute(
            select(Document).where(Document.created_at < cutoff_date)
        )
        documents_to_delete = result.scalars().all()
        
        count = 0
        for doc in documents_to_delete:
            await DocumentService._perform_document_deletion(db, doc)
            count += 1
        
        if count > 0:
            await db.commit()
            print(f"Successfully deleted {count} old document(s).")
        else:
            print("No old documents to delete.")
            
        return count