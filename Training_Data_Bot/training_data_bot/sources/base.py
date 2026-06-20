import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Union
from uuid import uuid4

from ..models import Document, DocumentType
from ..core.logging import get_logger

class BaseLoader(ABC):
    """The Master Blueprint for all document loaders."""
    
    def __init__(self):
        self.logger = get_logger(f"loader.{self.__class__.__name__}")
        self.supported_formats: List[DocumentType] = []

    @abstractmethod
    async def load_single(self, source: Union[str, Path], **kwargs) -> Document:
        """Every loader MUST know how to load one document."""
        pass

    async def load_multiple(self, sources: List[Union[str, Path]], max_workers: int = 4) -> List[Document]:
        """Traffic Control: Parallel Loading with Semaphores."""
        semaphore = asyncio.Semaphore(max_workers)

        async def load_with_semaphore(source):
            async with semaphore:
                return await self.load_single(source)

        tasks = [load_with_semaphore(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid documents
        return [res for res in results if isinstance(res, Document)]

    def get_document_type(self, source: Union[str, Path]) -> DocumentType:
        """Format Detection."""
        source_str = str(source)
        if source_str.startswith('http'):
            return DocumentType.URL
        
        source_path = Path(source)
        suffix = source_path.suffix.lower().strip('.')
        return DocumentType(suffix)

    def create_document(self, title: str, content: str, source: Union[str, Path], doc_type: DocumentType, **kwargs) -> Document:
        """Document Creation Factory."""
        return Document(
            id=uuid4(),
            title=title,
            content=content,
            source=str(source),
            doc_type=doc_type,
            word_count=len(content.split()),
            char_count=len(content),
            created_at=datetime.utcnow(),
            **kwargs
        )