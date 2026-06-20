from typing import List

from ..models import Document, TextChunk


class TextPreprocessor:
    def chunk_document(self, document: Document, chunk_size: int = 800, overlap: int = 120) -> List[TextChunk]:
        content = (document.content or "").strip()
        if not content:
            return []

        if chunk_size <= 0:
            chunk_size = 800
        if overlap < 0:
            overlap = 0
        if overlap >= chunk_size:
            overlap = chunk_size // 4

        chunks: List[TextChunk] = []
        start = 0
        chunk_index = 0

        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk_text = content[start:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        document_id=document.id,
                        content=chunk_text,
                        start_index=start,
                        end_index=end,
                        chunk_index=chunk_index,
                        token_count=max(1, len(chunk_text.split())),
                    )
                )
                chunk_index += 1

            if end >= len(content):
                break
            start = max(0, end - overlap)

        return chunks