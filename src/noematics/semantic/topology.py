from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np
from noematics.core import Noema, Message, RoundContext
from noematics.semantic import SimpleEncoder, SemanticMatcher


@dataclass
class TopologyConfig:
    similarity_threshold: float = 0.3
    max_edges_per_node: Optional[int] = None
    retain_top_k: Optional[int] = None


class DynamicTopology:
    def __init__(self, config: TopologyConfig = TopologyConfig()):
        self.config = config
        self.encoder = SimpleEncoder()
        self.matcher = SemanticMatcher(self.encoder, config.similarity_threshold)
        self._edge_history: List[List[tuple[str, str, float]]] = []

    def build_routing(
        self,
        noemata: List[Noema],
        goal: str,
        context: "RoundContext",
    ) -> List[tuple[str, str]]:
        queries = [f"{noema.query_vector} {goal}" for noema in noemata]
        keys = [noema.key_vector for noema in noemata]

        adjacency = self.matcher.build_adjacency(queries, keys)

        edges = []
        noema_ids = [n.id for n in noemata]

        for k_idx in range(len(noemata)):
            row = adjacency[k_idx]
            if self.config.retain_top_k is not None:
                top_k_indices = np.argsort(row)[-self.config.retain_top_k :]
                for q_idx in top_k_indices:
                    if row[q_idx] >= self.config.similarity_threshold:
                        edges.append((noema_ids[q_idx], noema_ids[k_idx], row[q_idx]))
            else:
                for q_idx in range(len(noemata)):
                    if row[q_idx] >= self.config.similarity_threshold:
                        edges.append((noema_ids[q_idx], noema_ids[k_idx], row[q_idx]))

        self._edge_history.append(edges)
        return [(src, tgt) for src, tgt, _ in edges]

    def get_edge_history(self) -> List[List[tuple[str, str, float]]]:
        return self._edge_history
