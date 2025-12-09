import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from backend.worker import process_document_async
from app.models.document import DocumentStatus

@pytest.mark.asyncio
async def test_process_document_success():
    """Test successful document processing flow"""
    mock_doc = MagicMock()
    mock_doc.id = "123"
    mock_doc.file_path = "test.pdf"
    mock_doc.mime_type = "application/pdf"
    mock_doc.filename = "test.pdf"

    with patch("backend.worker.AsyncSessionLocal") as mock_session_cls:
        mock_db = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_db
        
        with patch("backend.worker.DocumentService") as mock_service:
            mock_service.get_document = AsyncMock(return_value=mock_doc)
            mock_service.update_status = AsyncMock()
            mock_service.update_extracted_text = AsyncMock()
            
            with patch("backend.worker.OCRService") as mock_ocr:
                mock_ocr.extract_text = AsyncMock(return_value="Extracted Content")
                
                await process_document_async("123")
                
                # Check status updates
                # 1. Processing
                mock_service.update_status.assert_any_call(mock_db, mock_doc, DocumentStatus.PROCESSING)
                # 2. Extracted Text saved
                mock_service.update_extracted_text.assert_called_with(mock_db, mock_doc, "Extracted Content")
                # 3. Completed
                mock_service.update_status.assert_called_with(mock_db, mock_doc, DocumentStatus.COMPLETED)

@pytest.mark.asyncio
async def test_process_document_failure():
    """Test error handling in processing flow"""
    mock_doc = MagicMock()
    mock_doc.id = "123"

    with patch("backend.worker.AsyncSessionLocal") as mock_session_cls:
        mock_db = AsyncMock()
        mock_session_cls.return_value.__aenter__.return_value = mock_db
        
        with patch("backend.worker.DocumentService") as mock_service:
            mock_service.get_document = AsyncMock(return_value=mock_doc)
            mock_service.update_status = AsyncMock()
            
            with patch("backend.worker.OCRService") as mock_ocr:
                # Simulate OCR failure
                mock_ocr.extract_text = AsyncMock(side_effect=Exception("OCR Failed"))
                
                await process_document_async("123")
                
                # Check status update to FAILED
                mock_service.update_status.assert_called_with(mock_db, mock_doc, DocumentStatus.FAILED)