## Case Title
AI Buddy – The Multi-Agent Learning Companion

## Background
Students often spend large amounts of time reviewing lecture notes, slides, and textbooks, yet struggle to stay organized and focus on the right material. Existing study tools mainly provide static summaries or flashcards and do not adapt to different learning styles or preferences.  
With recent advances in Artificial Intelligence and Large Language Models, it is now possible to combine multiple AI “agents” that analyze content, create exercises, and guide learning. This project explores how AI can support students by generating personalized learning materials and feedback from their own study resources.

## Purpose
The goal of this project is to design and implement a simple but functional web-based learning assistant that demonstrates how multiple AI agents can collaborate to help students study more effectively.  
The application, called **AI Buddy**, will allow users to upload lecture notes or short recordings and automatically receive summaries, flashcards, and quiz questions.  
The main learning objective for the project team is to apply the **BMAD method** to describe, model, analyze, and design this system using the AI tools introduced in IBE160.

## Target Users
- University and college students preparing for exams  
- Self-learners using digital study materials  
- Teachers who wish to generate review material automatically  

## Core Functionality
- Secure login and user sessions  
- Upload of simple study materials (text, scanned notes, or short audio clips)  
- Automatic generation of summaries, flashcards, and quiz questions  
- Overview of study progress and quiz results  
- Web interface suitable for both desktop and mobile  
- Demonstration of a small multi-agent setup: “Reader Agent” + “Coach Agent”  

### Must Have (MVP)
- **User authentication** (sign-up / login / local secure storage)  
- **File and media upload** for content analysis:  
  - Text documents (PDF, Word, or plain text)  
  - **Scanned or handwritten notes** (processed via OCR or Gemini Vision)  
  - **Short voice recordings** (converted to text with Whisper or Gemini Audio)  
- **AI-generated study output:**  
  - Short summaries  
  - Flashcards (question–answer pairs)  
  - Multiple-choice quiz questions with simple scoring  
- **Progress tracking:** store and display quiz results and completion rate  
- **Multi-Agent setup:**  
  - *Reader Agent* → extracts and summarizes content  
  - *Coach Agent* → generates questions and feedback  

### Nice to Have (Optional Extensions)
- **Adaptive “Learn Your Way” mode** – adjusts question difficulty and feedback  
- **Planner Agent** – proposes a short study plan before exams  
- **Voice interaction** – “Explain this section in simpler terms”  
- **Gamification** – daily challenge or progress streaks  

## Data Requirements
- **Users:** ID, email, hashed password, language preference  
- **Uploaded materials:** file type, title, subject, upload timestamp  
- **Generated content:** summaries, flashcards, quizzes, feedback  
- **Progress data:** quiz score, completion %, session logs  

## User Stories
1. As a student, I can upload my notes or handwritten images and get an AI summary.  
2. As a learner, I can generate flashcards and quizzes to test myself.  
3. As a user, I can see my quiz results and track progress over time.  
4. As a teacher, I can upload course notes to generate simple review questions.  
5. As a user, I can communicate with my AI Buddy in text to clarify answers.  

## Technical Constraints
- Web application developed using the course’s **GitHub BMAD template**  
- **Backend:** Python FastAPI (API and multi-agent coordination)  
- **Frontend:** NextJS (web interface and user interaction)  
- **AI Integration:** Gemini CLI for text, image, and audio processing  
- **Database:** PostgreSQL for storing users, uploaded files, and results  
- **Security:** Encrypted file upload (max 15 MB), GDPR compliant  
- **Architecture:** Two-agent logic (Reader + Coach) simulated in backend  
- **Scope:** Focus on a minimal working prototype, not full production features  

## Success Criteria
- The user can complete one full flow (upload → summarize → quiz → feedback)  
- Summaries are generated in under 10 seconds for small files  
- At least 70–80% of pilot users find the AI output useful for learning  
- The prototype demonstrates collaboration between at least two AI agents  
- The system is feasible to develop and document within the IBE160 course period  
- The BMAD method is applied consistently through all project phases
