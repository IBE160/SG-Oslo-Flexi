# Brainstorm – Core features (2025-11-09)

- **Must-haves**
    - User can upload a document (e.g., PDF, PNG, JPG).
    - Document text is extracted via an OCR pipeline.
    - User can ask clarifying questions about the uploaded document.
    - AI provides answers grounded in the document's content.
    - User can request a quiz based on the document.
    - A simple quiz (e.g., 5 multiple-choice questions) is generated.
    - User receives a score upon quiz completion.

- **Should-haves**
    - Support for a wider range of document formats (DOCX, TXT).
    - Ability to select specific sections of a document for quiz generation.
    - Conversation and quiz history saved for the user.
    - More varied quiz question types (e.g., true/false, open-ended).
    - Ability to share quiz results.

- **Dependencies**
    - **OCR Service:** A reliable OCR engine (e.g., Google Cloud Vision, Tesseract) to accurately extract text.
    - **Language Model (LLM):** A powerful LLM (e.g., Gemini) for Q&A and quiz generation.
    - **Vector Database:** For storing document embeddings to enable efficient, context-aware Q&A (RAG).
    - **Cloud Infrastructure:** Scalable hosting for the backend, frontend, and document storage.

- **Risks & mitigations**
    - **Risk:** Inaccurate OCR output corrupts the context for the LLM.
        - **Mitigation:** Use high-quality OCR services. Implement image pre-processing to enhance quality. Allow users to review and correct extracted text as a "should-have" feature.
    - **Risk:** LLM generates irrelevant or incorrect ("hallucinated") quiz questions/answers.
        - **Mitigation:** Employ a strong RAG (Retrieval-Augmented Generation) pattern to ensure the LLM is strictly grounded in the document's content. Fine-tune prompts for accuracy.
    - **Risk:** Poor user experience from a slow or confusing interface.
        - **Mitigation:** Focus on a simple, clean UI. Implement asynchronous processing for document uploads and quiz generation with clear status indicators.
    - **Risk:** Data privacy concerns with user-uploaded documents.
        - **Mitigation:** Implement strict data handling policies, encrypt documents at rest and in transit, and be transparent with users.

- **Proposed decision**
The MVP will focus on the single-document "upload-and-quiz" workflow. This provides a complete, testable user journey that validates the core value proposition of turning static documents into interactive learning tools.
