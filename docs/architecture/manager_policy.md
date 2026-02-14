> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Manager Policy

### Completion Status

```python
class CompletionStatus(Enum):
    UNKNOWN = "unknown"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"
```

### Global State

```python
@dataclass
class GlobalState:
    round_context: str
    public_messages: List[str]
    execution_order: List[int]
    round_number: int
```

### Policy Interface

```python
class ManagerPolicy:
    def __init__(
        self,
        success_threshold: float,
        max_rounds: int,
        domain: str
    ):
        """Initialize policy with threshold and round limits"""
        
    async def evaluate(
        self,
        global_state: GlobalState,
        agent_outputs: Dict[str, Dict]
    ) -> ManagerDecision:
        """
        Evaluate global state and agent outputs to determine:
        - whether execution should halt
        - what the next round goal should be
        - confidence in the current state
        """
```

### Decision Output

```python
@dataclass
class ManagerDecision:
    should_halt: bool
    next_goal: str
    completion_status: CompletionStatus
    confidence: float
```
