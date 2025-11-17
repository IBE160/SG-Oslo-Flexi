# Product Brief: AI Buddy

## Executive Summary

AI Buddy is a web-based learning assistant that helps students and self-learners study more effectively. By leveraging a multi-agent AI system, AI Buddy transforms users' own study materials into a personalized and adaptive learning experience, including summaries, flashcards, and quizzes. The project aims to address the common challenges of cognitive overload, passive learning, and lack of motivation by providing an all-in-one, document-first platform. The MVP will focus on the core workflow of uploading a document, generating study materials, and tracking basic progress. Future versions will introduce more advanced features like adaptive learning, a planner agent, and deeper RAG integration.

## Initial Vision

The vision for AI Buddy is to create an all-in-one learning loop that takes a student's own materials and transforms them into a personalized study experience. This includes:

*   **Document-first approach:** The system will be built around the student's own documents (PDFs, notes, etc.), using a Retrieval-Augmented Generation (RAG) approach to ensure all generated content is grounded in the source material.
*   **Multi-agent workflow:** A series of specialized AI agents (e.g., "Reader", "Coach") will work together to analyze content, generate study materials, and provide personalized feedback.
*   **Adaptive learning:** The system will adapt to the user's learning style and progress, adjusting the difficulty of questions and providing targeted feedback.
*   **Motivation by design:** Gamification elements like streaks, badges, and progress tracking will be integrated to keep users engaged and motivated.

## Problem Statement

Students and self-learners are often overwhelmed by the volume of study material and struggle to stay organized and focused. They rely on passive review methods, which are less effective for long-term retention. Existing digital study tools are often fragmented, requiring users to switch between different applications for summarization, flashcards, and quizzes.

## Problem Impact

This lack of an integrated and adaptive learning process leads to:

*   **Cognitive overload:** Students are buried in information without a clear path to understanding.
*   **Inefficient studying:** Passive review of notes is less effective than active recall.
*   **Decreased motivation:** Without clear progress tracking and engagement loops, students are more likely to lose motivation.
*   **Fragmented workflows:** Juggling multiple tools for different study tasks is time-consuming and inefficient.

## Existing Solutions & Gaps

The current market for study tools is fragmented, with each tool addressing only a part of the learning process:

*   **Flashcard apps (e.g., Anki, Quizlet):** Powerful for spaced repetition, but often require manual creation of cards and lack deep integration with course materials.
*   **Note-taking apps with AI (e.g., Notion AI):** Good for organizing and summarizing notes, but lack structured learning paths, gamification, and progress tracking.
*   **Chat assistants (e.g., ChatGPT, Gemini):** Excellent for general Q&A, but not tailored for creating structured study materials or tracking mastery of a specific subject.

The key gap is the lack of a single, integrated platform that can take a user's own study materials and guide them through a complete, adaptive learning loop, from summarization to mastery.

## Proposed Solution

AI Buddy will be a web-based application that provides a seamless, end-to-end learning experience. The core workflow will be:

1.  **Upload:** Users upload their study materials (PDFs, DOCX, etc.).
2.  **Analyze:** A "Reader" agent will parse the document, extract key concepts, and create a summary.
3.  **Generate:** A "Coach" agent will use the analyzed content to generate flashcards and a multiple-choice quiz.
4.  **Study:** Users can study the flashcards and take the quiz.
5.  **Track:** The system will track the user's progress, identify areas of weakness, and provide personalized feedback.

## Key Differentiators

AI Buddy will differentiate itself from existing solutions through:

*   **All-in-one Learning Loop:** Combining summarization, flashcards, quizzes, and coaching in a single, unified experience.
*   **Document-First RAG:** All generated content will be directly tied to the user's own study materials, with clear citations to the source.
*   **Multi-Agent Orchestration:** A system of specialized AI agents will ensure a structured and high-quality output.
*   **Adaptive Coaching:** The "Coach" agent will provide personalized feedback and guidance based on the user's performance.
*   **Built-in Motivation:** Gamification features will be integrated to encourage consistent study habits.

## User Segments

### Primary User Segment: University & College Students

*   **Situation:** Overwhelmed by lecture notes, textbook chapters, and research papers. They need to study efficiently for exams and retain information throughout the semester.
*   **Frustrations:** Disorganized notes, passive rereading, and lack of a clear study plan.
*   **Valued Outcome:** A tool that can automatically structure their materials, create practice tests, and help them focus on what's most important.

### Secondary User Segment: Self-Learners & Professionals

*   **Situation:** Motivated individuals who are learning new skills for career advancement or personal interest. They are often time-constrained and need to maximize the effectiveness of their study sessions.
*   **Frustrations:** Finding high-quality, relevant study materials and staying motivated without the structure of a formal course.
*   **Valued Outcome:** A flexible tool that can adapt to any subject matter and provide a structured, engaging learning experience.

## User Journey (Happy Path)

1.  **Upload:** A student uploads a PDF of their lecture notes.
2.  **Summarize:** The "Reader" agent provides a concise summary of the key topics.
3.  **Generate:** The "Coach" agent creates a set of flashcards and a 5-question multiple-choice quiz.
4.  **Practice:** The student reviews the flashcards to reinforce key concepts.
5.  **Assess:** The student takes the quiz and receives a score.
6.  **Feedback:** The "Coach" agent provides feedback on the student's performance, highlighting areas for improvement and suggesting the next topic to focus on.
7.  **Track:** The student's progress is saved to their dashboard, where they can see their mastery level for the subject and track their study streak.

## Success Metrics

### Product & User Success

*   **Activation Rate:** % of new users who complete one full learning loop (upload -> summarize -> quiz -> feedback) within 24 hours of signing up.
*   **Engagement:**
    *   Weekly Active Users (WAU)
    *   Average number of study sessions per week
    *   Average length of study streaks
*   **Learning Impact:**
    *   Improvement in quiz scores over time
    *   Number of "weak topics" resolved
*   **Retention:** Week 4 retention rate.

### Business Success

*   **Conversion Rate:** % of free users who upgrade to a paid plan.
*   **Customer Acquisition Cost (CAC):** Cost to acquire a new paying customer.
*   **Lifetime Value (LTV):** Total revenue generated from a single customer.
*   **Virality:** Number of new users acquired through referrals or shared content.

## Core Features (MVP)

*   **User Authentication:** Secure sign-up and login.
*   **File Upload:** Allow users to upload a single document (PDF, DOCX, TXT) up to 20MB.
*   **OCR Text Extraction:** Use Google Cloud Vision to extract text from scanned documents.
*   **AI-Generated Content:**
    *   **Summaries:** Generate concise summaries of the uploaded document.
    *   **Flashcards:** Create question-and-answer flashcards.
    *   **Quizzes:** Generate a 5-question multiple-choice quiz.
*   **Basic Progress Tracking:** Store and display quiz results.
*   **Multi-Agent Backend:** A "Reader" agent to analyze content and a "Coach" agent to generate study materials.

## Out of Scope (for MVP)

*   **RAG / Vector Database:** The initial version will not use a vector database for retrieval-augmented generation.
*   **Multi-document projects:** The MVP will only support single-document analysis.
*   **Asynchronous pipelines:** All processing will be synchronous.
*   **Advanced Gamification:** The MVP will have basic progress tracking, but no badges, leaderboards, or complex rewards.
*   **Social Features:** No ability to share content or collaborate with other users.

## Future Vision Features

*   **Adaptive "Learn Your Way" Mode:** Adjust question difficulty and feedback based on user performance.
*   **Planner Agent:** Propose a study plan based on the user's goals and exam schedule.
*   **Voice Interaction:** Allow users to ask questions and receive explanations via voice.
*   **Advanced Gamification:** Full implementation of streaks, badges, leaderboards, and other motivational features.
*   **Deeper RAG Integration:** Use a vector database to enable more sophisticated Q&A and cross-document analysis.

## Market Analysis

The market for AI-powered study tools is growing rapidly, but is still fragmented. Key competitors include:

*   **Quizlet:** Strong in flashcards and simple quizzes, but lacks deep personalization from user documents.
*   **Notion AI:** Excellent for organizing notes, but not purpose-built for learning workflows.
*   **ChatGPT/Gemini:** Powerful for general Q&A, but lack the structure and progress tracking needed for effective studying.

AI Buddy's opportunity is to provide a unified, document-first platform that combines the best features of these tools into a single, cohesive learning experience.

## Technical Preferences

*   **Frontend:** Next.js with TypeScript and TailwindCSS.
*   **Backend:** Python with FastAPI for the orchestration layer.
*   **AI:** Gemini CLI for interacting with the LLM.
*   **Database:** PostgreSQL for storing user data and progress.
*   **Agent Framework:** Microsoft AutoGen is recommended for orchestrating the multi-agent workflow, with LlamaIndex used for data-intensive tasks.

## Risks and Assumptions

*   **LLM Hallucination:** The risk of the AI generating incorrect or misleading information. This will be mitigated by grounding all generated content in the source documents (RAG) and implementing a self-check mechanism in the prompts.
*   **OCR Accuracy:** The accuracy of the OCR process will be critical for the quality of the generated content. This will be addressed by using a high-quality OCR service (Google Cloud Vision) and implementing a quality gate to reject low-quality scans.
*   **User Adoption:** The success of the project depends on users being willing to adopt a new study tool. This will be addressed by focusing on a smooth onboarding experience and demonstrating clear value to the user.
