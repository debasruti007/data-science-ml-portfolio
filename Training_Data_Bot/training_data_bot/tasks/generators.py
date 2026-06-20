from typing import Tuple


class QAGenerator:
    def generate(self, text: str) -> Tuple[str, str]:
        cleaned = " ".join(text.split())
        prompt = f"Create a question and answer from this passage: {cleaned[:350]}"
        answer = cleaned[:220] if cleaned else "No content available"
        output = f"Q: What is the key point of this passage?\nA: {answer}"
        return prompt, output


class ClassificationGenerator:
    def generate(self, text: str) -> Tuple[str, str]:
        cleaned = " ".join(text.split())
        prompt = f"Classify this text by content type: {cleaned[:350]}"

        lowered = cleaned.lower()
        label = "general"
        if any(token in lowered for token in ["error", "bug", "exception", "stack trace"]):
            label = "technical-support"
        elif any(token in lowered for token in ["invoice", "payment", "price", "billing"]):
            label = "finance"
        elif any(token in lowered for token in ["policy", "compliance", "regulation", "legal"]):
            label = "compliance"

        output = f"label: {label}"
        return prompt, output


class SummarizationGenerator:
    def generate(self, text: str) -> Tuple[str, str]:
        cleaned = " ".join(text.split())
        prompt = f"Summarize this passage in 1-2 sentences: {cleaned[:500]}"
        summary = cleaned[:260] if cleaned else "No content available"
        output = f"Summary: {summary}"
        return prompt, output