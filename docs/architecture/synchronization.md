> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Synchronization & Message Broker

### Synchronization Barrier

Coordinates round-level execution to ensure all agents complete before proceeding.

```python
class SynchronizationBarrier:
    def __init__(self, timeout: float):
        """Initialize barrier with timeout"""
        
    async def initialize_round(self, round_number: int, agent_ids: List[str]):
        """Initialize barrier state for new round"""
        
    async def wait_for_agent(self, agent_id: str) -> bool:
        """Signal agent completion and wait for others"""
```

### Message Aggregator

Aggregates messages from multiple sources for each agent.

```python
class MessageAggregator:
    def __init__(self, max_in_degree: int):
        """Initialize with maximum incoming messages per agent"""
        
    def aggregate_messages(
        self,
        public_message: str,
        private_messages: List[RoutedMessage],
        execution_order: List[int]
    ) -> str:
        """Aggregate public and private messages"""
        
    def build_execution_order(self, adjacency_matrix: np.ndarray) -> List[int]:
        """Build topological execution order from graph"""
```

### Round Execution State

```python
@dataclass
class RoundExecutionState:
    round_number: int
    agent_ids: List[str]
    pending_agents: Set[str]
    completed_agents: Set[str]
    failed_agents: Set[str]
```

### Concepts

- **Barrier**: Ensures all agents finish their single-pass inference before topology induction
- **Aggregation**: Combines public messages with private routed messages, ordered by relevance
- **Execution Order**: Determines agent processing order based on graph topology (DAG or cyclic)

See: `docs/reference/examples/synchronization_example.md` for concrete implementations
