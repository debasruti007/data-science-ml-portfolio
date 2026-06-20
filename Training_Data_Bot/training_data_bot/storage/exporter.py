import asyncio
import csv
import json
from pathlib import Path
from typing import Dict, List

from ..models import Dataset, TrainingExample


class DatasetExporter:
    async def export(self, dataset: Dataset, path, format: str, split_data: bool = True):
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        export_format = (format or "jsonl").lower()
        examples = dataset.examples

        if split_data and examples:
            train, validation, test = self._split_examples(examples, dataset.train_split, dataset.validation_split)
            base = output_path.with_suffix("")
            if export_format == "jsonl":
                await asyncio.gather(
                    asyncio.to_thread(self._write_jsonl, base.with_name(f"{base.name}_train.jsonl"), train),
                    asyncio.to_thread(self._write_jsonl, base.with_name(f"{base.name}_validation.jsonl"), validation),
                    asyncio.to_thread(self._write_jsonl, base.with_name(f"{base.name}_test.jsonl"), test),
                )
                return output_path

        if export_format == "jsonl":
            await asyncio.to_thread(self._write_jsonl, output_path, examples)
            return output_path
        if export_format == "json":
            await asyncio.to_thread(self._write_json, output_path, dataset)
            return output_path
        if export_format == "csv":
            await asyncio.to_thread(self._write_csv, output_path, examples)
            return output_path

        raise ValueError(f"Unsupported export format: {format}")

    def _split_examples(self, examples: List[TrainingExample], train_split: float, validation_split: float):
        total = len(examples)
        train_end = int(total * train_split)
        validation_end = train_end + int(total * validation_split)
        return examples[:train_end], examples[train_end:validation_end], examples[validation_end:]

    def _example_to_record(self, example: TrainingExample) -> Dict[str, object]:
        return {
            "id": str(example.id),
            "input_text": example.input_text,
            "output_text": example.output_text,
            "task_type": example.task_type.value,
            "source_document_id": str(example.source_document_id),
            "quality_scores": example.quality_scores,
            "created_at": example.created_at.isoformat(),
        }

    def _write_jsonl(self, path: Path, examples: List[TrainingExample]):
        with path.open("w", encoding="utf-8") as file_obj:
            for example in examples:
                file_obj.write(json.dumps(self._example_to_record(example), ensure_ascii=False) + "\n")

    def _write_json(self, path: Path, dataset: Dataset):
        payload = {
            "id": str(dataset.id),
            "name": dataset.name,
            "description": dataset.description,
            "total_examples": dataset.total_examples,
            "train_split": dataset.train_split,
            "validation_split": dataset.validation_split,
            "test_split": dataset.test_split,
            "examples": [self._example_to_record(example) for example in dataset.examples],
        }
        with path.open("w", encoding="utf-8") as file_obj:
            json.dump(payload, file_obj, indent=2, ensure_ascii=False)

    def _write_csv(self, path: Path, examples: List[TrainingExample]):
        with path.open("w", encoding="utf-8", newline="") as file_obj:
            writer = csv.DictWriter(
                file_obj,
                fieldnames=["id", "input_text", "output_text", "task_type", "source_document_id", "quality_scores", "created_at"],
            )
            writer.writeheader()
            for example in examples:
                writer.writerow(self._example_to_record(example))