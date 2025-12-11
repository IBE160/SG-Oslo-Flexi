import time

def process_document(document_id: str):
    """
    Stub worker for document processing.
    Story 3.2 will implement OCR here.
    """
    print(f"Processing document {document_id}...")
    # Simulate work
    time.sleep(2)
    print(f"Finished processing document {document_id}")
