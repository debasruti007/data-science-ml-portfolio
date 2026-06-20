from typing import Dict, Iterable, List

from .generators import QAGenerator, ClassificationGenerator, SummarizationGenerator
from ..models import TaskType, TextChunk


class TaskManager:
    def __init__(self):
        self.qa_generator = QAGenerator()
        self.classification_generator = ClassificationGenerator()
        self.summarization_generator = SummarizationGenerator()

    async def execute(self, chunks: Iterable[TextChunk], task_types: List[TaskType]) -> List[Dict[str, object]]:
        results: List[Dict[str, object]] = []

        for chunk in chunks:
            for task_type in task_types:
                if task_type == TaskType.QA_GENERATION:
                    input_text, output_text = self.qa_generator.generate(chunk.content)
                elif task_type == TaskType.CLASSIFICATION:
                    input_text, output_text = self.classification_generator.generate(chunk.content)
                elif task_type == TaskType.SUMMARIZATION:
                    input_text, output_text = self.summarization_generator.generate(chunk.content)
                else:
                    input_text = f"Task '{task_type.value}' requested for text: {chunk.content[:300]}"
                    output_text = "Not implemented task type"

                results.append(
                    {
                        "chunk": chunk,
                        "task_type": task_type,
                        "input_text": input_text,
                        "output_text": output_text,
                    }
                )

        return results