> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Semantic Routing

### Semantic Encoder Interface

```python
class SemanticEncoder(ABC):
    @abstractmethod
    async def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings"""
        
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Get dimension of embeddings"""
```

### Similarity Matcher Interface

```python
class SemanticMatcher:
    def __init__(self, encoder: SemanticEncoder, threshold: float):
        """Initialize matcher with encoder and similarity threshold"""
        
    async def match_queries_to_keys(
        self, 
        queries: List[str], 
        keys: List[str]
    ) -> List[MatchResult]:
        """Match query descriptors to key descriptors"""
        
    async def build_adjacency_matrix(
        self, 
        queries: List[str], 
        keys: List[str],
        agent_count: int
    ) -> np.ndarray:
        """Build directed adjacency matrix for communication graph"""

@dataclass
class MatchResult:
    query_idx: int
    key_idx: int
    similarity_score: float
    query_text: str
    key_text: str
```

### Concept

Semantic routing matches agent query descriptors (what an agent needs) against key descriptors (what an agent provides) to construct a dynamic communication graph. Agents whose queries are semantically similar to others' keys receive messages from those agents.

See: `docs/reference/examples/semantic_routing_example.md` for concrete implementations
