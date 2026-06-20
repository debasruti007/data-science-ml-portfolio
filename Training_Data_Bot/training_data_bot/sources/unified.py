import asyncio
from pathlib import Path
from typing import List, Union, Optional

from .base import BaseLoader
from .document import DocumentLoader
from .pdf import PDFLoader
from .web import WebLoader
from ..models import Document, DocumentType
from ..core.exceptions import DocumentLoadError

class UnifiedLoader(BaseLoader):
    def __init__(self):
        super().__init__()
        # Initialize all our specialized vehicles
        self.document_loader = DocumentLoader()  # Text vehicle
        self.pdf_loader = PDFLoader()            # PDF vehicle
        self.web_loader = WebLoader()            # Internet vehicle
        
        # List of all formats we can handle
        self.supported_formats = list(DocumentType) # Everything!

    def validate_source(self, source: Union[str, Path]) -> bool:
        if isinstance(source, str) and source.startswith('http'):
            return DocumentType.URL in self.supported_formats
            
        source_path = Path(source)
        if not source_path.exists():
            return False
            
        suffix = source_path.suffix.lower().strip('.')
        try:
            return DocumentType(suffix) in self.supported_formats
        except ValueError:
            return False

    async def load_single(self, source: Union[str, Path], **kwargs) -> Optional[Document]:
        try:
            source_str = str(source)
            
            # Step 1: Is it a Website?
            if source_str.startswith(('http://', 'https://')):
                return await self.web_loader.load_single(source)

            # Step 2: Is it a File?
            source_path = Path(source)
            if not source_path.exists():
                return None  # File doesn't exist!

            # Step 3: What Type of File?
            suffix = source_path.suffix.lower().strip('.')
            doc_type = DocumentType(suffix)

            if doc_type == DocumentType.PDF:
                loader = self.pdf_loader
            elif doc_type in [DocumentType.TXT, DocumentType.DOCX, DocumentType.MD, DocumentType.HTML, DocumentType.JSON, DocumentType.CSV]:
                loader = self.document_loader
            else:
                raise DocumentLoadError(f"Unsupported format: {suffix}")

            return await loader.load_single(source)
            
        except Exception as e:
            raise DocumentLoadError(
                f"Failed to load document from {source}",
                file_path=str(source),
                cause=e
            )

    def _find_supported_files(self, directory: Union[str, Path]) -> List[Path]:
        directory = Path(directory)
        files = []
        patterns = ["*.pdf", "*.txt", "*.md", "*.html", "*.docx", "*.json", "*.csv"]
        
        for pattern in patterns:
            files.extend(directory.rglob(pattern))
        return files

    async def load_directory(self, directory: Union[str, Path], recursive: bool = True) -> List[Document]:
        sources = self._find_supported_files(directory)
        return await self.load_multiple(sources)