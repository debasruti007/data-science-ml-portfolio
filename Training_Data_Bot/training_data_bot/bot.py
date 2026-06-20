import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from uuid import UUID

from .core.config import settings
from .core.logging import get_logger, LogContext
from .core.exceptions import TrainingDataBotError, ConfigurationError

from .sources.unified import UnifiedLoader
from .decodo.client import DecodoClient
from .ai.client import AIClient
from .tasks.manager import TaskManager
from .preprocessing.text_preprocessor import TextPreprocessor
from .evaluation.quality_evaluator import QualityEvaluator
from .storage.exporter import DatasetExporter
from .storage.database import DatabaseManager

from .models import Document, Dataset, ProcessingJob, TaskType, QualityReport, DocumentType, TrainingExample

class TrainingDataBot:
    """
    Main Training Data Bot class.
    This class provides a high-level interface for:
    - Loading documents from various sources
    - Processing text with task templates
    - Quality assessment and filtering
    - Dataset creation and export
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Training Data Bot.
        Args:
            config: Optional configuration overrides
        """
        self.logger = get_logger("training_data_bot")
        self.config = config or {}
        self._init_components()
        self.logger.info("Training Data Bot initialized successfully")

    def _init_components(self):
        """Initialize all bot components."""
        try:
            self.loader = UnifiedLoader()
            self.decodo_client = DecodoClient()
            self.ai_client = AIClient()
            self.task_manager = TaskManager()
            self.preprocessor = TextPreprocessor()
            self.evaluator = QualityEvaluator()
            self.exporter = DatasetExporter()
            self.db_manager = DatabaseManager()

            # State (Memory boxes)
            self.documents: Dict[UUID, Document] = {}
            self.datasets: Dict[UUID, Dataset] = {}
            self.jobs: Dict[UUID, ProcessingJob] = {}

        except Exception as e:
            raise ConfigurationError("Failed to initialize bot components", e)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()

    async def load_documents(
        self,
        sources: Union[str, Path, List[Union[str, Path]]],
        doc_types: Optional[List[DocumentType]] = None,
        **kwargs
    ) -> List[Document]:
        
        if isinstance(sources, (str, Path)):
            sources = [sources]
            
        loaded_documents = []
        
        for source in sources:
            source_path = Path(source) if not str(source).startswith('http') else str(source)
            
            if isinstance(source_path, Path) and source_path.is_dir():
                dir_docs = await self.loader.load_directory(source_path)
                loaded_documents.extend(dir_docs)
            else:
                doc = await self.loader.load_single(source)
                if doc:
                    loaded_documents.append(doc)
                    
        for doc in loaded_documents:
            self.documents[doc.id] = doc
            
        return loaded_documents

    async def process_documents(
        self,
        documents: Optional[List[Document]] = None,
        task_types: Optional[List[TaskType]] = None,
        quality_filter: bool = True,
        **kwargs
    ) -> Dataset:
        documents = documents or list(self.documents.values())
        if not documents:
            raise TrainingDataBotError("No documents provided for processing")

        task_types = task_types or [
            TaskType.QA_GENERATION,
            TaskType.CLASSIFICATION,
            TaskType.SUMMARIZATION,
        ]

        chunk_size = int(kwargs.get("chunk_size", 800))
        overlap = int(kwargs.get("overlap", 120))
        quality_threshold = float(kwargs.get("quality_threshold", 0.65))

        job = ProcessingJob(
            name=f"document_processing_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            job_type="document_processing",
            status="running",
            total_items=len(documents),
            processed_items=0,
            started_at=datetime.utcnow(),
            estimated_completion=datetime.utcnow() + timedelta(minutes=max(1, len(documents))),
        )
        self.jobs[job.id] = job

        try:
            training_examples: List[TrainingExample] = []

            for document in documents:
                chunks = self.preprocessor.chunk_document(document, chunk_size=chunk_size, overlap=overlap)
                if not chunks:
                    job.processed_items += 1
                    continue

                task_outputs = await self.task_manager.execute(chunks, task_types)
                for item in task_outputs:
                    candidate = TrainingExample(
                        input_text=item["input_text"],
                        output_text=item["output_text"],
                        task_type=item["task_type"],
                        source_document_id=document.id,
                        quality_scores={},
                    )

                    if quality_filter:
                        scores = self.evaluator.score_example(candidate)
                        candidate.quality_scores = scores
                        score = scores.get("coherence", 0.0)
                        if score < quality_threshold:
                            continue

                    training_examples.append(candidate)

                job.processed_items += 1

            dataset = Dataset(
                name=kwargs.get("dataset_name", "training_dataset"),
                description=kwargs.get("dataset_description", "Generated training dataset from source documents"),
                examples=training_examples,
                total_examples=len(training_examples),
                train_split=float(kwargs.get("train_split", 0.8)),
                validation_split=float(kwargs.get("validation_split", 0.1)),
                test_split=float(kwargs.get("test_split", 0.1)),
            )

            self.datasets[dataset.id] = dataset
            job.status = "completed"
            return dataset
        except Exception:
            job.status = "failed"
            raise

    async def evaluate_dataset(self, dataset: Dataset, detailed_report: bool = True) -> QualityReport:
        report = await self.evaluator.evaluate(dataset)
        if detailed_report:
            self.logger.info(
                "Dataset quality report generated | score=%.3f | passed=%s | issues=%d",
                report.overall_score,
                report.passed,
                len(report.issues),
            )
        return report

    async def export_dataset(
        self,
        dataset: Dataset,
        output_path: Union[str, Path],
        format: str = "jsonl",
        split_data: bool = True,
        **kwargs
    ) -> Path:
        exported_path = await self.exporter.export(
            dataset=dataset,
            path=output_path,
            format=format,
            split_data=split_data,
        )
        self.logger.info("Dataset exported: %s", exported_path)
        return Path(exported_path)

    async def quick_process(
        self,
        source: Union[str, Path],
        output_path: Union[str, Path],
        task_types: Optional[List[TaskType]] = None,
        export_format: str = "jsonl"
    ) -> Dataset:
        documents = await self.load_documents([source])
        dataset = await self.process_documents(documents=documents, task_types=task_types)
        await self.export_dataset(dataset=dataset, output_path=output_path, format=export_format)
        return dataset

    def get_statistics(self) -> Dict[str, Any]:
        return {
            "documents": {
                "total": len(self.documents),
                "by_type": self._count_documents_by_type(),
                "total_size": sum(doc.word_count for doc in self.documents.values())
            },
            "datasets": {
                "total": len(self.datasets),
                "total_examples": sum(len(ds.examples) for ds in self.datasets.values()),
                "by_task_type": self._count_examples_by_task_type()
            },
            "jobs": {
                "total": len(self.jobs),
                "active": len([j for j in self.jobs.values() if j.status in {'active', 'running'}]),
                "by_status": self._count_jobs_by_status()
            }
        }

    def _count_documents_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for doc in self.documents.values():
            key = doc.doc_type.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    def _count_examples_by_task_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for dataset in self.datasets.values():
            for example in dataset.examples:
                key = example.task_type.value
                counts[key] = counts.get(key, 0) + 1
        return counts

    def _count_jobs_by_status(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for job in self.jobs.values():
            counts[job.status] = counts.get(job.status, 0) + 1
        return counts

    async def cleanup(self):
        """Cleanup resources and close connections."""
        try:
            await self.db_manager.close()
            if hasattr(self.decodo_client, 'close'):
                await self.decodo_client.close()
            if hasattr(self.ai_client, 'close'):
                await self.ai_client.close()
            self.logger.info("Bot cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")