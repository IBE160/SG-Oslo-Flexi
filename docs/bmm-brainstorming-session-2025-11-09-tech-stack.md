# Brainstorm – MVP Technology Stack & Infrastructure (2025-11-09)

- **Cloud Provider**
    - **Options:** Google Cloud Platform (GCP), Amazon Web Services (AWS), Microsoft Azure.
    - **Analysis:** All three are viable. However, GCP offers native and seamless integration with high-quality AI/ML services like Gemini and Google Cloud Vision, which are central to our product. This can simplify development and improve performance.
    - **Decision:** **Google Cloud Platform (GCP)**.

- **Frontend**
    - **Framework:**
        - **Options:** React, Vue, Svelte.
        - **Decision:** **React (with TypeScript)** using the **Vite** build tool. This provides a robust, type-safe foundation with a massive ecosystem and a fast development experience.
    - **Styling:**
        - **Options:** Tailwind CSS, Material-UI, CSS-in-JS.
        - **Decision:** **Tailwind CSS**. It allows for rapid, utility-first development, which is ideal for building a clean, custom MVP interface without being locked into a specific design system's aesthetic.
    - **Hosting:**
        - **Options:** Vercel, Netlify, Google Cloud Storage.
        - **Decision:** **Vercel**. Its integration with GitHub for CI/CD, preview deployments, and optimization for React/Next.js frameworks make it the superior choice for frontend hosting.

- **Backend (Orchestrator & Agents)**
    - **Runtime & Framework:**
        - **Options:** Python with FastAPI/Flask, Node.js with Express/Fastify.
        - **Decision:** **Python with FastAPI**. Python has superior libraries for AI, ML, and document processing. FastAPI provides a modern, high-performance framework with automatic API documentation, which is perfect for our agent-based architecture.
    - **Compute:**
        - **Options:** Google Cloud Functions (Gen2), Google Cloud Run.
        - **Decision:** **Google Cloud Run**. It offers more flexibility than Cloud Functions regarding dependencies, containerization, and longer execution timeouts (up to 60 minutes), which is crucial for potentially long-running OCR and LLM generation tasks.

- **Data, Storage, & Messaging**
    - **File Storage (Ephemeral):**
        - **Decision:** **Google Cloud Storage (GCS)**. It's the native, scalable solution for storing user-uploaded files temporarily. A strict lifecycle policy will be set on the bucket to auto-delete files after 24 hours.
    - **Asynchronous Messaging:**
        - **Decision:** **Google Cloud Pub/Sub**. It will be used to decouple the initial file upload from the backend processing, triggering the Cloud Run service asynchronously. This is key to providing a responsive UI.

- **AI & OCR Services**
    - **OCR Engine:**
        - **Decision:** **Tesseract OCR** (open-source). This will be integrated and run within the Cloud Run container. While potentially less accurate and more complex to manage than a managed cloud service, it is free and avoids direct OCR costs.
    - **Language Model (LLM):**
        - **Decision:** **Google Gemini API (e.g., Gemini 1.5 Pro)**. We will leverage its free tier for initial development and MVP usage. If free tier limits are exceeded, future consideration will be given to self-hosting open-source LLMs (e.g., Llama 3, Mistral) on a free-tier VM, which would introduce significant operational complexity.

- **DevOps & Observability**
    - **Infrastructure as Code (IaC):**
        - **Decision:** **Terraform**. It's the industry standard for defining and managing cloud infrastructure declaratively, ensuring our setup is reproducible and version-controlled.
    - **CI/CD:**
        - **Decision:** **GitHub Actions**. For backend, it will be used to run tests, build the container image, push it to Google Artifact Registry, and deploy to Cloud Run. Vercel handles frontend CI/CD automatically.
    - **Observability:**
        - **Decision:** **Google Cloud's operations suite**. Natively integrated **Cloud Logging** for structured logs and **Cloud Trace** for distributed tracing via the `trace_id` will be used, relying on their free tiers for MVP usage.

- **Proposed Decision**
The MVP will be built on a serverless-first architecture using **GCP**, prioritizing free and open-source services. The backend will be a **Python/FastAPI** application (leveraging **Pydantic** for data validation) running on **Cloud Run's free tier**. For OCR, we will integrate **Tesseract OCR** within the Cloud Run container. The LLM will utilize the **Google Gemini API's free tier** for initial development, with a future consideration for self-hosting open-source LLMs if free tier limits are exceeded. The frontend will be a **React/TypeScript** application hosted on **Vercel's free tier**. Infrastructure will be managed with **Terraform**, and CI/CD with **GitHub Actions**. This approach minimizes initial cost but introduces increased complexity for OCR and LLM management.
