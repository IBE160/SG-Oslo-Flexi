# Brainstorm – Quiz Engine (2025-11-09) — MVP aligned

## Scope (MVP)
- Render and score **exactly 5 MCQs**
- Ground every item in `sections[].text` via `source_span`
- English-only UI

## Data model (TS hint)
```ts
export type QuizItem = {
  itemType: "MCQ";
  question: string;
  options: [string, string, string, string];
  correctAnswerIndex: 0 | 1 | 2 | 3;
  source_span: string[]; // section_id refs from Reader→Coach
};

export type QuizPayload = {
  trace_id: string;
  quiz_items: QuizItem[];
  // optional
  flashcards?: { front: string; back: string; source_span: string[] }[];
};
```

## Backend validator (rules)
- `quiz_items.length === 5`
- Each item: 4 unique `options`
- `correctAnswerIndex ∈ {0,1,2,3}`
- `source_span.length ≥ 1` and each id exists in `sections[].section_id`
- If any item fails: drop it (or single retry). If fewer than 5 remain → **502**

## Scoring
- Client: store selected index per item
- On Submit: compare to `correctAnswerIndex`; compute total correct (0–5)
- Results page: display per-item correctness and the correct option

## UI states
- Initial: questions with disabled Submit until all answered
- Submitting: loading state; prevent double submit
- Results: score + breakdown

## Non-goals (MVP)
- Adaptive difficulty
- Partial credit / open-ended answers
- Export/share

## Sample valid payload (abridged)
```json
{
  "trace_id": "uuid",
  "quiz_items": [
    {
      "itemType": "MCQ",
      "question": "Which organelle is known as the powerhouse of the cell?",
      "options": ["Nucleus", "Ribosome", "Mitochondrion", "Golgi apparatus"],
      "correctAnswerIndex": 2,
      "source_span": ["page_1_para_1"]
    }
  ]
}
```

## Acceptance checks
- 100% JSON parse success
- 5 items with unique options and valid `source_span`
- Correct score calculated client-side; accurate per-item feedback
```