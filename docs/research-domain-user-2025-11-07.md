# Domain & User Research – AI Buddy: The Multi-Agent Learning Companion
**Date:** 2025-11-07  
**Phase:** 1 – Analysis (BMAD)  
**Focus:** Learning science, study behaviors, and user needs for adaptive AI learning tools.

---

## 1) Research Objective
Understand the **user domain (students)** and their **learning challenges** to design AI Buddy as a tool that aligns with effective study habits, educational psychology, and digital learning trends.

---

## 2) Target Users
| User Type | Description | Main Goals | Pain Points |
|------------|--------------|-------------|--------------|
| **Undergraduate students** | First-year and second-year university students | Learn complex content efficiently, prepare for exams | Overwhelm, disorganization, lack of focus |
| **Adult learners** | Working professionals taking part-time courses | Time-efficient revision, concept clarity | Limited study time, motivation |
| **STEM students** | Technical disciplines (engineering, IT, science) | Concept mastery, formula memorization | Volume of content, abstract topics |
| **Language & social science students** | Theory-heavy programs | Retention and recall | Dense readings, terminology overload |

---

## 3) Observed Learning Challenges
1. **Cognitive overload:** Too much material, not enough structure.  
2. **Passive review:** Students reread instead of testing knowledge actively.  
3. **Fragmented resources:** Notes, PDFs, and recordings spread across devices.  
4. **Time management:** Difficulty maintaining consistent study habits.  
5. **Motivation dips:** Lack of progress tracking and rewards.  

---

## 4) User Needs
- **Summarization:** Convert lecture notes into concise, structured content.  
- **Active recall:** Provide flashcards and quick quizzes.  
- **Explanations:** Offer clarifications and examples on-demand.  
- **Progress visibility:** Show learning streaks, mastery levels, and weaknesses.  
- **Personalization:** Adapt difficulty and topic focus to user history.  
- **Guidance:** Recommend next study steps (“Coach” behavior).  

---

## 5) Learning Science Insights
### a) **Active Recall & Spaced Repetition**
- Testing oneself improves long-term retention more than rereading (Roediger & Karpicke, 2006).  
- Flashcards and quizzes are ideal for activating recall and building durable memory.

### b) **Chunking & Dual Coding**
- Grouping information into logical “chunks” aids comprehension.  
- Combining text with visuals improves learning outcomes (Mayer, 2014).

### c) **Feedback Loops**
- Immediate feedback helps correct misconceptions quickly (Hattie & Timperley, 2007).  
- The Coach Agent can reinforce this through quick hints and motivational tips.

### d) **Metacognitive Support**
- Tools that help students plan, monitor, and evaluate their learning improve performance.  
- Dashboards showing mastery and weak topics promote self-regulated learning.

---

## 6) Competitive Landscape
| Product | Features | Gaps (Opportunity) |
|----------|-----------|--------------------|
| **Quizlet** | Flashcards, spaced repetition | No adaptive summaries or quizzes from custom notes |
| **Notion Q&A / AI** | Content understanding | No gamification, limited memory |
| **ChatGPT / Gemini Chat** | Q&A and summarization | Lacks learning structure and progress tracking |
| **Anki** | Strong spaced repetition | Manual setup; poor UX for beginners |
| **Obsidian + plugins** | Personal knowledge base | Complex setup; not student-friendly |

→ **Opportunity:** Combine the *best of all*: adaptive learning + summarization + motivation in one platform.

---

## 7) Domain Trends
- Rise of **AI-powered edtech** (ChatGPT Edu, Notion AI, Quizlet AI).  
- Emphasis on **personalized learning paths** and adaptive feedback.  
- Integration of **learning analytics** for progress tracking.  
- **Gamification** improving user engagement (XP, badges, streaks).  
- Focus on **privacy-first education tools** compliant with GDPR and FERPA.

---

## 8) User Journey (Example)
1. Student uploads lecture slides → gets **AI summary**.  
2. AI Buddy generates **10 flashcards + 5 quiz questions**.  
3. Student takes a quick test → **Coach Agent** highlights weak areas.  
4. Dashboard updates with **progress bar** and motivational tip.  
5. AI Buddy recommends next topic or review session.

---

## 9) Personas

### Persona 1: “Emma the Efficient Learner”
- Age: 21, 2nd-year IT student  
- Motivation: Stay on top of multiple courses  
- Pain: Time pressure and messy notes  
- AI Buddy value: Auto-organized summaries, quick review before exams

### Persona 2: “Jonas the Working Student”
- Age: 28, part-time MBA student  
- Motivation: Maximize limited study time  
- Pain: Hard to maintain motivation after work  
- AI Buddy value: Personalized quiz sets and short learning sessions

### Persona 3: “Sara the Slow Reader”
- Age: 19, humanities student  
- Motivation: Understand dense theory texts  
- Pain: Overwhelmed by reading volume  
- AI Buddy value: Simplified summaries, keyword explanations, progress guidance

---

## 10) User Value Map
| Need | AI Buddy Feature | Benefit |
|------|------------------|----------|
| Structure & focus | Summarizer Agent | Saves time, clarifies key ideas |
| Recall practice | Flashcard Agent | Improves retention |
| Self-testing | Quiz Agent | Builds confidence |
| Guidance | Coach Agent | Keeps motivation high |
| Memory over time | Supabase embeddings | Personalized review sessions |

---

## 11) Key Insights
- Students want **simplicity + motivation + personalization**.  
- Most tools focus on **content**, not **learning progress**.  
- Emotional support (encouragement, feedback) is surprisingly important.  
- Multi-agent design fits natural study phases: *learn → test → reflect → plan.*  

---

## 12) Design Implications for AI Buddy
1. Keep the **UI lightweight** — one dashboard, no clutter.  
2. Add **micro-feedback** (tips, badges, streaks).  
3. Use **adaptive difficulty** — quizzes get harder as skill improves.  
4. Visualize learning progress clearly.  
5. Offer short study modes (5–10 min micro-sessions).  
6. Always include a motivational or reflective element in outputs.  

---

## 13) Next Steps
- [ ] Validate needs with 3–5 real students (survey/interview)  
- [ ] Prototype dashboard wireframes and test clarity of flow  
- [ ] Simulate one learning cycle (upload → summary → quiz → feedback)  
- [ ] Track emotional response and perceived motivation  

---

**Summary:**  
AI Buddy can position itself as a **next-generation personal learning assistant** — blending the structure of Anki, the interactivity of ChatGPT, and the motivation design of Duolingo — with transparency, context awareness, and multi-agent intelligence.

