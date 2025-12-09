import os
import pypdf
import io
from docx import Document as DocxDocument
from google.cloud import vision
from app.core.config import settings

class OCRService:
    @staticmethod
    async def extract_text(file_path: str, mime_type: str) -> str:
        """
        Extracts text from a file based on its MIME type.
        Uses a hybrid approach for PDFs: native extraction first, fallback to GCV if low density.
        """
        if mime_type == "application/pdf":
            return await OCRService._extract_from_pdf(file_path)
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await OCRService._extract_from_docx(file_path)
        elif mime_type == "text/plain":
            return await OCRService._extract_from_txt(file_path)
        elif mime_type in ["image/jpeg", "image/png"]:
            return await OCRService._extract_from_image(file_path)
        else:
            raise ValueError(f"Unsupported MIME type: {mime_type}")

    @staticmethod
    async def _extract_from_pdf(file_path: str) -> str:
        """
        Attempts native extraction. Checks density. If low, falls back to OCR.
        Density heuristic: extracted_chars / num_pages. If < 50, assume scanned.
        """
        text = ""
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
             # If pypdf fails completely, we might want to try OCR, or just fail.
             # For now, let's log and re-raise or try OCR?
             # Let's try OCR if pypdf fails to read valid structure but file exists.
             print(f"pypdf extraction failed: {e}. Attempting OCR fallback.")
             return await OCRService._extract_from_image(file_path) # GCV handles PDFs too, but as images/files

        # Density Check
        num_pages = len(reader.pages) if reader.pages else 1
        density = len(text.strip()) / num_pages if num_pages > 0 else 0
        
        # Configurable threshold could go in settings, hardcoded 50 for now per validation recommendation
        DENSITY_THRESHOLD = 50 

        if density < DENSITY_THRESHOLD:
            print(f"Low text density ({density:.2f} chars/page). Falling back to Google Cloud Vision OCR.")
            return await OCRService._extract_with_gcv(file_path, is_pdf=True)
        
        return text

    @staticmethod
    async def _extract_from_docx(file_path: str) -> str:
        doc = DocxDocument(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    async def _extract_from_txt(file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    async def _extract_from_image(file_path: str) -> str:
        return await OCRService._extract_with_gcv(file_path, is_pdf=False)

    @staticmethod
    async def _extract_with_gcv(file_path: str, is_pdf: bool = False) -> str:
        """
        Uses Google Cloud Vision API to extract text.
        Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
        """
        client = vision.ImageAnnotatorClient()

        if is_pdf:
            # GCV for PDF/TIFF is async and requires GCS usually, OR use `document_text_detection` on pages converted to images.
            # However, `async_batch_annotate_files` works for local files if we read bytes? 
            # Actually, for local PDF OCR with GCV, the standard `image_annotator` supports `mime_type` in `annotate_file` 
            # BUT efficient GCV PDF OCR usually recommends GCS.
            # FASTEST IMPLEMENTATION for MVP without GCS bucket dependency:
            # Convert PDF pages to images (using pdf2image) -> send to GCV. 
            # OR use GCV's synchronous file support if file is small (up to 5 pages/10MB).
            # Given MVP constraints (20MB max), we might hit sync limits.
            # Let's try to treat it as a "file" request if supported, or fallback to the simpler:
            # "We assume for MVP scanned PDFs are reasonably small or we just error if GCV rejects large local payloads."
            
            # Re-reading docs: GCV `document_text_detection` supports images. 
            # `async_batch_annotate_files` is for PDF/TIFF but output goes to GCS.
            # To avoid GCS dependency: Use `pdf2image` to convert first? 
            # Or use `pypdf` to extract images from PDF and OCR them?
            
            # DECISION for MVP: To keep it simple and avoid adding `pdf2image` (requires poppler),
            # we will throw a "NotImplemented" or handle only 1st page if we treat as image?
            # Better: Use `mime_type` application/pdf in the request if the client supports it for small files.
            # The python client usually expects `content` for images.
            
            # ACTUALLY: Let's assume for this MVP step that "Scanned PDF" via GCV might need GCS.
            # Workaround: Read file bytes, send as `content` with mime_type `application/pdf` to `batch_annotate_files`.
            # Supported for small files (up to 5 pages) in sync mode? 
            # Documentation says PDF is supported in `async_batch_annotate_files` (output to GCS).
            
            # Alternative: Since we claim to support it, let's use the `pypdf` extraction of IMAGES from the pages,
            # and OCR those images.
            
            # Let's try reading bytes and sending to GCV first.
            pass
        
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        
        # For PDF, we need to use `AnnotateFileRequest` if we send bytes, but that's for async mostly.
        # Let's stick to images for now. If is_pdf, we might fail here if we just send PDF bytes as 'image'.
        
        # Correction: If is_pdf, we need to handle it. 
        # For this MVP iteration, let's implement the IMAGE path fully. 
        # For PDF fallback, we will implement a basic "extract images from PDF" loop using pypdf if possible, 
        # or warn that GCV PDF requires GCS.
        # Let's try to assume the PDF *is* just a wrapper for images and `pypdf` image extraction works?
        
        # SIMPLIFICATION: If PDF density is low, we assume it's scanned. 
        # We will try to send the bytes to GCV as an 'image' if it's a single page? No.
        # Let's leave PDF OCR Placeholder or use a simplified approach: 
        # If is_pdf, we skip GCV for now unless we add `pdf2image`. 
        # Wait, `pypdf` has `extract_images`.
        
        if is_pdf:
             # Extract images from PDF pages and OCR them individually
             text_accum = ""
             reader = pypdf.PdfReader(file_path)
             for page in reader.pages:
                 for image_file_object in page.images:
                     # image_file_object.data is bytes
                     vision_image = vision.Image(content=image_file_object.data)
                     response = client.document_text_detection(image=vision_image)
                     if response.full_text_annotation:
                         text_accum += response.full_text_annotation.text + "\n"
             return text_accum

        # Standard Image OCR
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            raise Exception(f'{response.error.message}')

        return response.full_text_annotation.text
