# Product Requirements Document: AI Buddy

## 1. Vision and Strategy

### 1.1. Vision Alignment

The vision for AI Buddy is to create a personalized and adaptive learning companion that empowers students to study more effectively. It aims to transform static study materials into an interactive and engaging learning experience, helping students to not only learn but also to master their subjects.

### 1.2. Project Classification

*   **Project Type:** Web Application, SaaS
*   **Domain:** EdTech
*   **Complexity:** Medium

### 1.3. Product Magic Essence

The "magic" of AI Buddy is the seamless and instant transformation of a user's own study materials into a personalized and adaptive learning experience. It's the "wow" moment when a student uploads their messy lecture notes and gets back a structured summary, a set of smart flashcards, and a challenging quiz, all in one place.

## 2. Success Definition

### 2.1. Success Criteria

*   **User Adoption:** A significant number of users complete the onboarding process and become active users.
*   **Engagement:** Users consistently use the platform for their studying needs, as measured by session frequency and duration.
*   **Learning Efficacy:** Users show demonstrable improvement in their quiz scores and a reduction in "weak topics" over time.
*   **User Satisfaction:** Users report a high level of satisfaction with the platform and find it to be a valuable tool for their studies.

## 3. Scope Definition

### 3.1. MVP Scope

The Minimum Viable Product (MVP) will focus on delivering the core value proposition:

*   **User Authentication:** Secure sign-up and login.
*   **File Upload:** Allow users to upload a single document (PDF, DOCX, TXT) up to 20MB.
*   **OCR Text Extraction:** Use Google Cloud Vision to extract text from scanned documents.
*   **AI-Generated Content:**
    *   **Summaries:** Generate concise summaries of the uploaded document.
    *   **Flashcards:** Create question-and-answer flashcards.
    *   **Quizzes:** Generate a 5-question multiple-choice quiz.
*   **Basic Progress Tracking:** Store and display quiz results.
*   **Multi-Agent Backend:** A "Reader" agent to analyze content and a "Coach" agent to generate study materials.

### 3.2. Growth Features

These features are planned for after the MVP, to enhance the product's competitiveness and user engagement:

*   **Adaptive "Learn Your Way" Mode:** Adjust question difficulty and feedback based on user performance.
*   **Planner Agent:** Propose a study plan based on the user's goals and exam schedule.
*   **Voice Interaction:** Allow users to ask questions and receive explanations via voice.
*   **Advanced Gamification:** Full implementation of streaks, badges, leaderboards, and other motivational features.
*   **Deeper RAG Integration:** Use a vector database to enable more sophisticated Q&A and cross-document analysis. The IBE160 MVP will not include a vector database; this deeper RAG integration is a future enhancement.

### 3.3. Vision Features

These represent the long-term aspirations for AI Buddy, pushing the boundaries of personalized learning:

*   **Multi-document projects:** Support for analyzing and cross-referencing multiple documents.
*   **Collaborative learning:** Features for users to share content and study with peers.
*   **Integration with LMS:** Seamless integration with existing Learning Management Systems.
*   **AI-powered content creation:** Tools for teachers to generate course materials.

## 4. Innovation Discovery

### 4.1. Innovation Patterns

The core innovation of AI Buddy lies in its **multi-agent orchestration** combined with a **document-first prompting approach inspired by Retrieval-Augmented Generation (RAG)**. While the MVP uses direct prompting on extracted text without a vector database, the architectural vision is to evolve this into a full RAG stack as part of the growth roadmap. This allows for:

*   **Personalized Learning from Own Materials:** Unlike generic AI chatbots, AI Buddy directly leverages the user's specific study documents to generate highly relevant and accurate learning content.
*   **Structured Learning Loop:** The multi-agent system (Reader, Coach) creates a structured and adaptive learning path, moving beyond static summaries to interactive quizzes and personalized feedback.
*   **Motivation by Design:** Integrating gamification elements directly into the learning process to foster consistent engagement and habit formation.

### 4.2. Validation Approach

The validation of these innovations will involve:

*   **Pilot Programs:** Conducting pilot programs with university students to gather feedback on the effectiveness and usability of the personalized learning experience.
*   **A/B Testing:** Comparing engagement and learning outcomes between users with and without gamified features.
*   **Qualitative Feedback:** User interviews and surveys to understand the perceived value of the multi-agent system and document-first RAG.
*   **Technical Metrics:** Tracking LLM hallucination rates, and OCR accuracy to ensure the technical underpinnings are robust. RAG hit rates will become a key metric in future iterations once a vector-DB-based RAG pipeline is implemented.

## 5. Project-Specific Deep Dive

### 5.1. Project Type Requirements (Web Application)

*   **Browser Compatibility:** Support for modern web browsers (Chrome, Firefox, Edge, Safari).
*   **Responsive Design:** The user interface must adapt to various screen sizes (desktop, tablet, mobile).
*   **Performance:** Fast loading times and a smooth user experience.
*   **SEO:** Basic search engine optimization for discoverability (if applicable for public-facing pages).
*   **Accessibility:** Adherence to WCAG guidelines for accessibility.

### 5.2. SaaS B2B Considerations

These considerations describe how AI Buddy could evolve into a SaaS/B2B product beyond the IBE160 MVP.

*   **Tenant Model:** For a future B2B offering, the platform would need to support a multi-tenant architecture, allowing different educational institutions or groups to manage their users and data securely and independently. This is not part of the IBE160 MVP.
*   **Permission Matrix:** A future version would require a robust role-based access control (RBAC) system to define granular permissions for different user roles (e.g., Student, Teacher, Administrator). This is not implemented in the MVP.

## 6. UX Principles

### 6.1. Core UX Principles

*   **Simplicity & Clarity:** The interface should be intuitive and easy to navigate, minimizing cognitive load for users.
*   **Feedback & Transparency:** Users should always understand what the system is doing (e.g., "Processing document...", "Generating quiz...") and receive clear feedback on their actions.
*   **Consistency:** Maintain a consistent visual design and interaction patterns across the entire application.
*   **Motivation & Engagement:** Design elements that encourage continuous use and provide a sense of accomplishment.

### 6.2. Key Interactions

*   **File Upload:** A prominent drag-and-drop area with clear instructions and visual feedback on upload progress.
*   **Quiz Interface:** Clean and uncluttered layout for multiple-choice questions, with clear selection and submission mechanisms.
*   **Progress Dashboard:** An easy-to-understand visual representation of learning progress, streaks, and mastery levels.
*   **Error Handling:** User-friendly error messages with actionable guidance, avoiding technical jargon.

## 7. Functional Requirements

### 7.1. User Management

*   **FR1.1:** The system SHALL allow users to register for a new account using email and password.
*   **FR1.2:** The system SHALL allow users to log in and log out securely.
*   **FR1.3:** The system SHALL support password reset functionality.
*   **FR1.4 (Future):** The system SHOULD be designed to allow administrators to manage user roles and permissions (for SaaS B2B tenants) in later phases. For the IBE160 MVP we assume a single ‘Student’ role (plus a simple admin account for configuration if needed).

### 7.2. Document Management

*   **FR2.1:** The system SHALL allow users to upload single documents (PDF, DOCX, TXT) up to 20MB.
*   **FR2.2:** The system SHALL perform OCR on uploaded image-based documents (e.g., scanned PDFs) using Google Cloud Vision.
*   **FR2.3:** The system SHALL store uploaded documents securely and temporarily.
*   **FR2.4:** The system SHALL delete uploaded documents and generated content upon user request or after a defined TTL (Time-To-Live).

### 7.3. AI-Powered Content Generation

*   **FR3.1:** The system SHALL generate a concise summary from the uploaded document.
*   **FR3.2:** The system SHALL generate a set of flashcards (question-answer pairs) from the document content.
*   **FR3.3:** The system SHALL generate a 5-question multiple-choice quiz from the document content, with one correct answer and three plausible distractors.
*   **FR3.4:** All generated content (summaries, flashcards, quizzes) SHALL be grounded in the original uploaded document.

### 7.4. Learning & Assessment

*   **FR4.1:** The system SHALL present flashcards for review.
*   **FR4.2:** The system SHALL allow users to take the generated multiple-choice quiz.
*   **FR4.3:** The system SHALL score the quiz and provide immediate feedback on correct/incorrect answers.
*   **FR4.4:** The system SHALL display the correct answer for incorrect responses.

### 7.5. Progress Tracking

*   **FR5.1:** The system SHALL store quiz results for each user.
*   **FR5.2:** The system SHALL display a user's quiz history and scores.
*   **FR5.3:** The system SHALL track and display basic learning progress (e.g., completion rate for a document).

### 7.6. Multi-Agent Orchestration

*   **FR6.1:** The backend SHALL orchestrate a "Reader" agent to process and analyze uploaded documents.
*   **FR6.2:** The backend SHALL orchestrate a "Coach" agent to generate study materials (flashcards, quizzes) and provide feedback.
*   **FR6.3:** The system SHALL ensure a structured data exchange between agents (e.g., Reader to Coach payload).

## 8. Non-Functional Requirements

### 8.1. Performance

*   **NFR8.1.1:** Summaries SHALL be generated within 10 seconds for documents up to 20MB.
*   **NFR8.1.2:** Quiz and flashcard generation SHALL be completed within 15 seconds for documents up to 20MB.
*   **NFR8.1.3:** The application SHALL load within 3 seconds on a standard broadband connection.

### 8.2. Security

*   **NFR8.2.1:** All data in transit SHALL be encrypted using TLS 1.2 or higher.
*   **NFR8.2.2:** All user data at rest SHALL be encrypted (e.g., AES-256).
*   **NFR8.2.3:** The system SHALL implement strong password policies.
*   **NFR8.2.4:** The system SHALL be designed with data privacy regulations (e.g., GDPR, CCPA) in mind, including data minimization and user rights.

### 8.3. Scalability

*   **NFR8.3.1:** The system SHALL be able to support up to 1,000 concurrent users without degradation in performance.
*   **NFR8.3.2:** The system architecture SHALL allow for horizontal scaling of backend services.

### 8.4. Accessibility

*   **NFR8.4.1:** The web application SHALL conform to WCAG 2.1 Level AA guidelines.

## 9. Product Magic Summary

The magic of AI Buddy is the seamless and instant transformation of a user's own study materials into a personalized and adaptive learning experience. It's the "wow" moment when a student uploads their messy lecture notes and gets back a structured summary, a set of smart flashcards, and a challenging quiz, all in one place. This empowers them to study more effectively and master their subjects with confidence.

