import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.services.ocr_service import OCRService

@pytest.mark.asyncio
async def test_extract_text_pdf_native():
    """Test PDF native extraction (high density) - No GCV call"""
    with patch("app.services.ocr_service.pypdf.PdfReader") as mock_reader:
        # Mock PDF page with lots of text
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "A" * 1000 # High density
        mock_reader.return_value.pages = [mock_page]
        
        # Mock GCV to ensure it's NOT called
        with patch("app.services.ocr_service.OCRService._extract_with_gcv") as mock_gcv:
            text = await OCRService.extract_text("dummy.pdf", "application/pdf")
            
            assert len(text) == 1000
            mock_gcv.assert_not_called()

@pytest.mark.asyncio
async def test_extract_text_pdf_scanned_fallback():
    """Test PDF scanned extraction (low density) - GCV call"""
    with patch("app.services.ocr_service.pypdf.PdfReader") as mock_reader:
        # Mock PDF page with very little text (scanned)
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "   " # Low density
        mock_reader.return_value.pages = [mock_page]
        
        # Mock GCV to return result
        with patch("app.services.ocr_service.OCRService._extract_with_gcv", new_callable=AsyncMock) as mock_gcv:
            mock_gcv.return_value = "OCR Result"
            
            text = await OCRService.extract_text("dummy.pdf", "application/pdf")
            
            assert text == "OCR Result"
            mock_gcv.assert_called_once()

@pytest.mark.asyncio
async def test_extract_text_image():
    """Test Image extraction - Always GCV"""
    with patch("app.services.ocr_service.OCRService._extract_with_gcv", new_callable=AsyncMock) as mock_gcv:
        mock_gcv.return_value = "Image Text"
        
        text = await OCRService.extract_text("dummy.jpg", "image/jpeg")
        
        assert text == "Image Text"
        mock_gcv.assert_called_once()

@pytest.mark.asyncio
async def test_extract_text_docx():
    """Test DOCX extraction"""
    with patch("app.services.ocr_service.DocxDocument") as mock_doc:
        mock_para = MagicMock()
        mock_para.text = "Docx Text"
        mock_doc.return_value.paragraphs = [mock_para]
        
        text = await OCRService.extract_text("dummy.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        
        assert text == "Docx Text"

@pytest.mark.asyncio
async def test_unsupported_mime():
    with pytest.raises(ValueError):
        await OCRService.extract_text("dummy.exe", "application/x-msdownload")
