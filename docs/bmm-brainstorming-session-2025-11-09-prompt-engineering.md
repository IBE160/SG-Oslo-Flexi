# Brainstorm – Prompt Engineering & LLM Strategy (2025-11-09) — MVP aligned

## Core principles
- **Strict grounding:** Alt innhold skal være avledet KUN fra `sections[].text` (Reader→Coach v0). Ingen ekstern kunnskap.
- **Structured output:** LLM må svare med gyldig **JSON** (bruk “JSON mode” hvis tilgjengelig). Ingen kodeblokker, ingen ekstra tekst.
- **Role clarity:** Tydelige roller: **Reader** (analyse/kondensering) → **Coach** (quiz/flashcards).
- **Token control:** Kortfattet prompt, input-caps via filstørrelse (≤ 20 MB), og eventuelt side-/seksjonsutvalg før generering.
- **Determinism (nok til MVP):** Temperatur lav, eksplisitte regler for format og kvalitet.

---

## Reader prompt (MVP)
> Mål: Kondenser råtekst fra OCR/parsing til nøkkeltermer og bullets **uten** å introdusere ny informasjon.

```
System:
You are a text analysis expert. Produce strictly valid JSON.

User:
Context:
<<INSERT concatenated page texts from OCR/parsing>>

Rules:
1) Use ONLY the text in Context. No outside knowledge.
2) Return a single JSON object with these keys:
   - "summary_bullets": array of 3–5 concise strings (max 20 words each)
   - "key_terms": array of 5–10 salient terms/phrases (strings)
3) Do NOT include code fences or any extra text.

Output JSON schema (informative):
{
  "summary_bullets": ["..."],
  "key_terms": ["...", "..."]
}
```

**Orchestrator note:** Reader-output **blandes ikke** inn i kildeteksten; det sendes som hints til Coach sammen med `sections[]` fra kontrakten (v0).

---

## Coach prompt (MVP) — Quiz generation
> Mål: Generere 5 MCQ som peker til konkrete kildespan.

```
System:
You are an expert quiz designer. Output strictly valid JSON.

User:
Context JSON (Reader→Coach v0):
{
  "contract_version": "v0",
  "trace_id": "<uuid>",
  "doc_meta": {...},
  "quality": {...},
  "sections": [ { "section_id": "page_1_para_1", "page_number": 1, "text": "..." }, ... ],
  "summary_bullets": [...],
  "key_terms": [...]
}

Rules:
1) Grounding: Every question, option, and answer must be supported by the text in sections[].text.
2) Cite support: For each item, set "source_span" to an array of section_id(s) backing the correct answer.
3) Format:
   - Exactly 5 questions, each with 4 options (1 correct + 3 plausible distractors).
   - Options must be mutually exclusive; avoid “All of the above”.
   - English language (MVP constraint).
4) JSON only. No markdown, no prose.

Output JSON schema (authoritative):
{
  "trace_id": "<uuid>",
  "quiz_items": [
    {
      "itemType": "MCQ",
      "question": "string",
      "options": ["string","string","string","string"],
      "correctAnswerIndex": 0,
      "source_span": ["section_id", "..."]
    }
  ],
  "flashcards": [
    { "front": "string", "back": "string", "source_span": ["section_id"] }
  ]
}
```

**Validator-regler (Coach-output):**
- `quiz_items.length === 5`
- Alle `options` unike per spørsmål; `correctAnswerIndex ∈ {0,1,2,3}`
- Hver `source_span[]` refererer til gyldig `sections[].section_id`
- (Valgfritt i MVP) Dropp `flashcards` hvis tomt

---

## Failure handling (prompt-nivå)
- **Ugyldig JSON:** Bruk leverandørens JSON-modus. Ved parse-feil: én automatisk retry med samme prompt; deretter 502 “generation failure”.
- **Ubegrunnet innhold (hallusinasjon):** Hard-regel i prompt + verifikasjon i backend: dropp items uten gyldig `source_span`.
- **Tomt/tynt grunnlag:** Hvis `sections[].text` < terskel (f.eks. < 500 tegn), aborter før Coach med 422 (quality gate).

---

## Token & kost-kontroll
- **Input-caps:** Maks 20 MB og eventuelt sidebegrensning (topp N sider) i MVP.
- **Kondensering:** Reader gir “summary_bullets”/“key_terms” for orientering; Coach bruker fortsatt `sections[].text` som sannhetskilde.
- **Lav temperatur:** Reduserer varians og resirkulerer “prompt budget”.

---

## Prompt QA (golden set)
- Et lite sett (3–5) dokumenter med kjente fasit-quiz. Kjør nattlig smoke: parse-sjekk + regler over.
- Aksepteringskriterier (MVP):
  - 100 % JSON-parsbarhet
  - 5/5 items oppfyller validator-regler
  - Ingen “All of the above”-mønstre
  - Hver item har minst én `source_span`

---

## Proposed decision
Bruke to-trinns prompting (Reader→Coach) med **streng JSON-håndheving**, **kildeknytning via `source_span`**, lav temperatur og enkel retry. Dette gir stabil MCQ-generering innenfor MVP-rammene, og danner grunnlag for senere verifikasjonssteg og utvidede oppgavetyper.