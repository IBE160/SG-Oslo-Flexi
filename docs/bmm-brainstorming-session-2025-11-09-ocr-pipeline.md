# Brainstorm – OCR Pipeline (2025-11-09)

- **Must-haves**
    - Accept PDF, PNG, and JPG file formats for upload.
    - Process multi-page documents (specifically PDFs).
    - Apply basic image pre-processing (e.g., auto-rotation, scaling) to normalize inputs.
    - Use an OCR engine to extract textual content from the documents.
    - Return extracted text in a structured format, associating text with its page number.
    - Handle processing asynchronously to avoid blocking the user interface.

- **Should-haves**
    - A "pass-through" for text-based files like TXT or DOCX that don't require OCR.
    - Confidence scoring for extracted text to identify low-quality regions.
    - Bounding box information to potentially link text back to its location in the original document.
    - Automatic language detection to handle non-English documents.
    - A review interface where users can correct obvious OCR errors.

- **Dependencies**
    - **Cloud Storage:** A bucket (e.g., S3, GCS) to receive and store uploaded user documents.
    - **OCR Service:** A chosen OCR provider. A high-accuracy, managed service (e.g., Google Cloud Vision, Azure AI Vision) is preferable for the MVP over a self-hosted solution to reduce initial complexity.
    - **Serverless Functions:** For creating a scalable, event-driven architecture (e.g., AWS Lambda, Google Cloud Functions) that triggers on new file uploads.
    - **Queueing System:** To manage the flow of documents into the processing pipeline and handle retries (e.g., SQS, Pub/Sub).

- **Risks & mitigations**
    - **Risk:** High cost associated with using third-party cloud OCR services at scale.
        - **Mitigation:** For the MVP, costs will be contained. For future scaling, introduce a hybrid model (e.g., use open-source Tesseract for simple documents, cloud services for complex ones) and implement rate limiting.
    - **Risk:** Poor extraction accuracy on documents with complex layouts (multi-column, tables, diagrams).
        - **Mitigation:** Initially, focus on and document support for simple, single-column text layouts. Use a state-of-the-art OCR engine known for better layout analysis.
    - **Risk:** Long processing times for large, high-resolution documents.
        - **Mitigation:** The asynchronous architecture is the primary mitigation. Clearly communicate processing status to the user (e.g., "Processing your 50-page document..."). Implement timeouts and down-sampling for excessively large images.
    - **Risk:** The pipeline fails for a specific document, leaving the user blocked.
        - **Mitigation:** Implement comprehensive error logging. Provide a clear error message to the user (e.g., "Could not process this file, please try a different format or a clearer copy").

- **Proposed decision**
For the MVP, we will implement the OCR pipeline as a serverless function that triggers upon file upload to a cloud storage bucket. We will use a high-accuracy managed service like Google Cloud Vision to minimize initial development overhead and ensure a quality user experience, with a focus on processing single-column PDFs and common image types.
