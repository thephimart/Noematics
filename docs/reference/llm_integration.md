> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## LLM Integration

### Core Interface

```python
class LLMBackend(ABC):
    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response from LLM"""
        
    @abstractmethod
    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        
    @abstractmethod
    def validate_configuration(self) -> bool:
        """Validate backend configuration"""
        
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
```

### Request/Response Shapes

```python
@dataclass
class LLMRequest:
    prompt: str
    max_tokens: int
    temperature: float
    stop_sequences: Optional[List[str]]
    json_mode: bool

@dataclass
class LLMResponse:
    content: str
    usage: Dict[str, int]
    model: str
    finish_reason: str
    latency_ms: float
```

### Error Categories

- **LLMError**: Base exception for LLM operations
- **RateLimitError**: Rate limit exceeded
- **TokenLimitError**: Token limit exceeded

See: `docs/reference/examples/llm_backends.md` for concrete implementations
