from __future__ import annotations

"""Module 3: Reranking — Cross-encoder top-20 → top-3 + latency benchmark."""

import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import RERANK_TOP_K


@dataclass
class RerankResult:
    text: str
    original_score: float
    rerank_score: float
    metadata: dict
    rank: int


_CROSS_ENCODER_CACHE = {}


def _get_cross_encoder(model_name: str):
    """Cache loaded CrossEncoder models to avoid reloading 2.2GB model on every call."""
    if model_name not in _CROSS_ENCODER_CACHE:
        from sentence_transformers import CrossEncoder
        _CROSS_ENCODER_CACHE[model_name] = CrossEncoder(model_name)
    return _CROSS_ENCODER_CACHE[model_name]


class CrossEncoderReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if self._model is None:
            self._model = _get_cross_encoder(self.model_name)
        return self._model

    def rerank(self, query: str, documents: list[dict], top_k: int = RERANK_TOP_K) -> list[RerankResult]:
        """Rerank documents: top-20 → top-k."""
        if not documents:
            return []

        model = self._load_model()
        pairs = [
            (query, doc.get("text", "") if isinstance(doc, dict) else getattr(doc, "text", ""))
            for doc in documents
        ]
        scores = model.predict(pairs)
        if hasattr(scores, "tolist"):
            scores = scores.tolist()
        elif isinstance(scores, (int, float)):
            scores = [float(scores)]
        else:
            scores = [float(s) for s in scores]

        scored = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
        return [
            RerankResult(
                text=doc.get("text", "") if isinstance(doc, dict) else getattr(doc, "text", ""),
                original_score=float(doc.get("score", 0.0) if isinstance(doc, dict) else getattr(doc, "score", 0.0)),
                rerank_score=float(score),
                metadata=doc.get("metadata", {}) if isinstance(doc, dict) else getattr(doc, "metadata", {}),
                rank=i
            )
            for i, (score, doc) in enumerate(scored[:top_k])
        ]


class FlashrankReranker:
    """Lightweight alternative (<5ms). Optional."""
    def __init__(self):
        self._model = None

    def _load_model(self):
        if self._model is None:
            from flashrank import Ranker
            self._model = Ranker()
        return self._model

    def rerank(self, query: str, documents: list[dict], top_k: int = RERANK_TOP_K) -> list[RerankResult]:
        if not documents:
            return []
        from flashrank import RerankRequest
        model = self._load_model()
        passages = [
            {
                "id": i,
                "text": d.get("text", "") if isinstance(d, dict) else getattr(d, "text", ""),
                "meta": d.get("metadata", {}) if isinstance(d, dict) else getattr(d, "metadata", {}),
                "score": float(d.get("score", 0.0) if isinstance(d, dict) else getattr(d, "score", 0.0)),
            }
            for i, d in enumerate(documents)
        ]
        results = model.rerank(RerankRequest(query=query, passages=passages))
        return [
            RerankResult(
                text=r["text"],
                original_score=float(r.get("score", 0.0)),
                rerank_score=float(r.get("score", 0.0)),
                metadata=r.get("meta", {}),
                rank=rank
            )
            for rank, r in enumerate(results[:top_k])
        ]


def benchmark_reranker(reranker, query: str, documents: list[dict], n_runs: int = 5) -> dict:
    """Benchmark latency over n_runs. (Đã implement sẵn)"""
    times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        reranker.rerank(query, documents)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
    return {"avg_ms": sum(times) / len(times), "min_ms": min(times), "max_ms": max(times)}


if __name__ == "__main__":
    query = "Nhân viên được nghỉ phép bao nhiêu ngày?"
    docs = [
        {"text": "Nhân viên được nghỉ 12 ngày/năm.", "score": 0.8, "metadata": {}},
        {"text": "Mật khẩu thay đổi mỗi 90 ngày.", "score": 0.7, "metadata": {}},
        {"text": "Thời gian thử việc là 60 ngày.", "score": 0.75, "metadata": {}},
    ]
    reranker = CrossEncoderReranker()
    for r in reranker.rerank(query, docs):
        print(f"[{r.rank}] {r.rerank_score:.4f} | {r.text}")
