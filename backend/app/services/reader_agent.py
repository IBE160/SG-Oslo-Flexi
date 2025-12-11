from typing import List
from app.schemas.orchestrator import ConversationContext

class ReaderAgent:
    """
    Minimal viable reader agent that extracts basic structure,
    performs lightweight classification, and produces a summary.
    """

    def process(self, context: ConversationContext) -> ConversationContext:
        # Fetch document text from the real ConversationContext structure
        raw_text = context.current_document.get("text", "") if context.current_document else ""

        if not raw_text.strip():
            context.history.append({
                "agent": "reader_agent",
                "error": "No text found in document"
            })
            context.last_agent_used = "reader_agent"
            return context

        # Extract content
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        title = self._extract_title(lines)
        headings = self._extract_headings(lines)
        key_points = self._extract_key_points(lines)
        summary = self._generate_summary(raw_text)
        doc_type = self._classify_document(raw_text)

        analysis_result = {
            "title": title,
            "headings": headings,
            "summary": summary,
            "key_points": key_points,
            "doc_type": doc_type,
            "total_characters": len(raw_text),
        }

        # Update context
        context.history.append({
            "agent": "reader_agent",
            "analysis": analysis_result
        })
        context.last_agent_used = "reader_agent"

        return context

    # --- Internal helpers ---

    def _extract_title(self, lines: List[str]) -> str:
        if not lines:
            return ""
        return lines[0] if len(lines[0]) > 5 else ""

    def _extract_headings(self, lines: List[str]) -> List[str]:
        headings = []
        for line in lines:
            if line.isupper() or line.endswith(":"):
                headings.append(line)
        return headings[:10]

    def _extract_key_points(self, lines: List[str]) -> List[str]:
        points = []
        for line in lines:
            if line.startswith(("-", "•", "*")):
                points.append(line)
            elif any(keyword in line.lower() for keyword in ["must", "should", "important", "requires"]):
                points.append(line)
        return points[:5]

    def _generate_summary(self, text: str) -> str:
        sentences = text.split(".")
        if len(sentences) > 1:
            return ". ".join(sentences[:2]).strip() + "."
        return text[:200] + ("..." if len(text) > 200 else "")

    def _classify_document(self, text: str) -> str:
        lower = text.lower()
        if "invoice" in lower or "total" in lower:
            return "invoice"
        if "agreement" in lower or "contract" in lower:
            return "contract"
        if "report" in lower or "summary" in lower:
            return "report"
        return "document"
