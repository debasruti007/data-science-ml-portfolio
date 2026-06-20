from typing import Dict

from ..models import Dataset, QualityMetric, QualityReport, TrainingExample


class QualityEvaluator:
    def score_example(self, example: TrainingExample) -> Dict[str, float]:
        input_len = max(1, len(example.input_text.split()))
        output_len = max(1, len(example.output_text.split()))

        relevance = 1.0 if output_len > 2 else 0.4
        coherence = 1.0 if output_len >= 5 else 0.5
        diversity = min(1.0, len(set(example.output_text.lower().split())) / output_len)
        bias = 0.95
        toxicity = 0.98

        return {
            QualityMetric.RELEVANCE.value: round(relevance, 3),
            QualityMetric.COHERENCE.value: round(coherence, 3),
            QualityMetric.DIVERSITY.value: round(diversity, 3),
            QualityMetric.BIAS.value: round(bias, 3),
            QualityMetric.TOXICITY.value: round(toxicity, 3),
            "length_ratio": round(min(2.0, output_len / input_len), 3),
        }

    async def evaluate(self, dataset: Dataset) -> QualityReport:
        if not dataset.examples:
            return QualityReport(
                target_id=dataset.id,
                overall_score=0.0,
                passed=False,
                metric_scores={metric.value: 0.0 for metric in QualityMetric},
                issues=["Dataset has no examples"],
                warnings=["Add more source documents and rerun processing"],
            )

        aggregate = {metric.value: 0.0 for metric in QualityMetric}
        issues = []
        warnings = []

        for example in dataset.examples:
            scores = self.score_example(example)
            example.quality_scores = scores
            for metric in QualityMetric:
                aggregate[metric.value] += scores.get(metric.value, 0.0)

            if scores[QualityMetric.COHERENCE.value] < 0.7:
                warnings.append("Low coherence found in at least one example")

        total = float(len(dataset.examples))
        metric_scores = {key: round(value / total, 3) for key, value in aggregate.items()}
        overall_score = round(sum(metric_scores.values()) / len(metric_scores), 3)
        passed = overall_score >= 0.7

        if not passed:
            issues.append("Overall quality score below threshold")

        return QualityReport(
            target_id=dataset.id,
            overall_score=overall_score,
            passed=passed,
            metric_scores=metric_scores,
            issues=issues,
            warnings=warnings,
        )