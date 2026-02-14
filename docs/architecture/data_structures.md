> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Core Data Structures

```python
@dataclass
class AgentMessage:
    """Core message structure for agent communication (per paper Section 3.1)
    
    Each agent outputs:
    - public message: visible to Manager, recorded for analysis
    - private message: routed to out-neighbors in G(t)
    - query descriptor: what information the agent needs
    - key descriptor: what information the agent can provide
    """
    agent_id: str
    round_number: int
    public_content: str
    private_content: str
    query_vector: str
    key_vector: str
    timestamp: datetime

@dataclass
class RoutedMessage:
    """Private message routed to a specific recipient"""
    content: str
    source_agent_id: str
    target_agent_id: str
    round_number: int
    similarity_score: float

@dataclass
class CommunicationGraph:
    """Dynamic communication topology"""
    adjacency_matrix: np.ndarray
    execution_order: List[int]
    similarity_matrix: np.ndarray
    threshold: float
    round_number: int
    
@dataclass
class AgentState:
    """Agent context and memory"""
    agent_id: str
    role: str
    context_history: List[str]
    message_history: List[AgentMessage]
    current_context: str
    last_response: Optional[str]
```
