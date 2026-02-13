from typing import Protocol, List, Optional
import numpy as np


class SemanticEncoder(Protocol):
    def encode(self, texts: List[str]) -> np.ndarray:
        ...

    def get_dimension(self) -> int:
        ...


class SemanticMatcher:
    def __init__(self, encoder: SemanticEncoder, threshold: float = 0.3):
        self.encoder = encoder
        self.threshold = threshold

    def compute_similarity(self, query_embeddings: np.ndarray, key_embeddings: np.ndarray) -> np.ndarray:
        query_norm = query_embeddings / (np.linalg.norm(query_embeddings, axis=1, keepdims=True) + 1e-8)
        key_norm = key_embeddings / (np.linalg.norm(key_embeddings, axis=1, keepdims=True) + 1e-8)
        return np.dot(query_norm, key_norm.T)

    def match(self, queries: List[str], keys: List[str]) -> List[tuple[int, int, float]]:
        if not queries or not keys:
            return []

        query_embeddings = self.encoder.encode(queries)
        key_embeddings = self.encoder.encode(keys)

        similarity_matrix = self.compute_similarity(query_embeddings, key_embeddings)

        matches = []
        for q_idx in range(len(queries)):
            for k_idx in range(len(keys)):
                score = similarity_matrix[q_idx, k_idx]
                if score >= self.threshold:
                    matches.append((q_idx, k_idx, float(score)))

        matches.sort(key=lambda x: x[2], reverse=True)
        return matches

    def build_adjacency(self, queries: List[str], keys: List[str]) -> np.ndarray:
        matches = self.match(queries, keys)
        n = len(queries)
        adj = np.zeros((n, n))
        for q_idx, k_idx, score in matches:
            adj[k_idx, q_idx] = score
        return adj
