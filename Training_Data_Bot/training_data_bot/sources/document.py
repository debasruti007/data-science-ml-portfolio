import asyncio
import csv
import json
from pathlib import Path
from typing import Union

from .base import BaseLoader
from ..models import Document, DocumentType
from ..core.exceptions import DocumentLoadError

class DocumentLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        self.supported_formats = [
            DocumentType.TXT,
            DocumentType.MD,
            DocumentType.HTML,
            DocumentType.JSON,
            DocumentType.CSV,
            DocumentType.DOCX,
        ]

    async def load_single(self, source: Union[str, Path], encoding: str = "utf-8", **kwargs) -> Document:
        source_path = Path(source)
        doc_type = self.get_document_type(source_path)
        
        if doc_type == DocumentType.TXT:
            content = await self._load_text(source_path, encoding)
        elif doc_type == DocumentType.MD:
            content = await self._load_markdown(source_path, encoding)
        elif doc_type == DocumentType.HTML:
            content = await self._load_html(source_path, encoding)
        elif doc_type == DocumentType.JSON:
            content = await self._load_json(source_path, encoding)
        elif doc_type == DocumentType.CSV:
            content = await self._load_csv(source_path, encoding)
        elif doc_type == DocumentType.DOCX:
            content = await self._load_docx(source_path)
        else:
            raise DocumentLoadError(f"Unsupported format for DocumentLoader: {doc_type}")

        return self.create_document(
            title=source_path.stem,
            content=content,
            source=source_path,
            doc_type=doc_type
        )

    async def _load_text(self, path: Path, encoding: str) -> str:
        return await asyncio.to_thread(path.read_text, encoding=encoding)

    async def _load_markdown(self, path: Path, encoding: str) -> str:
        return await asyncio.to_thread(path.read_text, encoding=encoding)

    async def _load_html(self, path: Path, encoding: str) -> str:
        try:
            from bs4 import BeautifulSoup
            with open(path, 'r', encoding=encoding) as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            return '\n'.join(chunk for chunk in chunks if chunk)
        except ImportError:
            return path.read_text(encoding=encoding)

    async def _load_json(self, path: Path, encoding: str) -> str:
        with open(path, 'r', encoding=encoding) as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            lines = [f"{key}: {value}" for key, value in data.items()]
            return "\n".join(lines)
        elif isinstance(data, list):
            lines = [f"Item {i+1}: {item}" for i, item in enumerate(data)]
            return "\n".join(lines)
        return str(data)

    async def _load_csv(self, path: Path, encoding: str) -> str:
        lines = []
        with open(path, 'r', encoding=encoding, newline='') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            if headers:
                lines.append("Headers: " + ", ".join(headers))
                lines.append("")
                
            for row_num, row in enumerate(reader, 1):
                if row_num > 1000:
                    lines.append("... (truncated, too many rows)")
                    break
                    
                if headers and len(row) == len(headers):
                    row_data = [f"{header}: {value}" for header, value in zip(headers, row)]
                    lines.append(f"Row {row_num}: {', '.join(row_data)}")
        return "\n".join(lines)

    async def _load_docx(self, path: Path) -> str:
        try:
            from docx import Document as DocxDocument
            doc = DocxDocument(path)
            text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(text_parts)
        except ImportError:
            raise DocumentLoadError("python-docx package required for DOCX files")