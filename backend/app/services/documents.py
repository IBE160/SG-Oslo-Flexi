from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentCreate
from uuid import UUID

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
