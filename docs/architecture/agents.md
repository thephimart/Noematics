> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Agent System

### Agent Configuration Shape

```python
@dataclass
class AgentConfig:
    agent_id: str
    role: str
    llm_model: str
    temperature: float
    max_tokens: int
    memory_limit: int
    timeout_seconds: int
```

### Abstract Agent Interface

```python
class Agent(ABC):
    @abstractmethod
    async def execute(self, round_goal: str, context: str) -> AgentMessage:
        """Execute agent task and return message"""
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent"""
```

### Role Taxonomy

Agents are categorized by their function in the workflow:

- **Worker Agents**: Execute tasks and produce outputs
  - Developer: Code generation
  - Tester: Test generation
  - Designer: Architecture/design
  - Researcher: Information gathering
  - Solver: Problem solving
  - Verifier: Solution validation

- **Manager Agent**: Orchestrates workflow and detects completion

### Factory Pattern

Agents are instantiated via a factory that maps role names to agent implementations:

```python
class AgentFactory:
    AGENT_REGISTRY: Dict[str, Type[Agent]]
    
    @classmethod
    def create_agent(cls, role: str, agent_id: str, llm_backend: LLMBackend, **kwargs) -> Agent:
        """Create agent by role"""
```

See: `docs/reference/examples/agents_example.md`
