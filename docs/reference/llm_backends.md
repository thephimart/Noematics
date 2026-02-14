> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## LLM Backend Implementations

### OpenAI Backend

```python
class OpenAIBackend(LLMBackend):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.rate_limiter = RateLimiter(tokens_per_minute=10000)
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        async with self.rate_limiter:
            start_time = time.time()
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": request.prompt}],
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                stop=request.stop_sequences,
                response_format={"type": "json_object"} if request.json_mode else None
            )
            latency = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.choices[0].message.content,
                usage=response.usage.dict(),
                model=response.model,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency
            )
```

### External API Backend

```python
class ExternalAPIBackend(LLMBackend):
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        model: str = "default",
        timeout: float = 60.0,
        headers: Optional[dict] = None
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.default_headers = {
            "Content-Type": "application/json",
            **(headers or {})
        }
        if api_key:
            self.default_headers["Authorization"] = f"Bearer {api_key}"
        
    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": request.prompt}],
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
        }
        if request.stop_sequences:
            payload["stop"] = request.stop_sequences
        if request.json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.default_headers
            )
            response.raise_for_status()
            data = response.json()
            
        latency = (time.time() - start_time) * 1000
        
        choice = data["choices"][0]
        return LLMResponse(
            content=choice["message"]["content"],
            usage=data.get("usage", {}),
            model=data.get("model", self.model),
            finish_reason=choice.get("finish_reason", "stop"),
            latency_ms=latency
        )
```

### Retry Logic

```python
class LLMError(Exception):
    """Base exception for LLM operations"""
    pass

class RateLimitError(LLMError):
    """Rate limit exceeded"""
    pass

class TokenLimitError(LLMError):
    """Token limit exceeded"""
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=(lambda e: isinstance(e, (RateLimitError, ConnectionError)))
)
async def robust_llm_call(
    backend: LLMBackend,
    request: LLMRequest,
    timeout: float = 30.0
) -> LLMResponse:
    """Robust LLM call with retry logic and timeout"""
    try:
        return await asyncio.wait_for(backend.generate(request), timeout=timeout)
    except asyncio.TimeoutError:
        raise LLMError(f"Request timed out after {timeout} seconds")
    except Exception as e:
        if "rate limit" in str(e).lower():
            raise RateLimitError(f"Rate limit exceeded: {e}")
        elif "token" in str(e).lower() and "limit" in str(e).lower():
            raise TokenLimitError(f"Token limit exceeded: {e}")
        else:
            raise LLMError(f"LLM call failed: {e}")
```

### Configuration

```python
class LLMConfig(BaseSettings):
    """Configuration for LLM backends"""
    
    default_backend: str = Field(default="openai", env="DYTOPO_LLM_BACKEND")
    max_tokens: int = Field(default=2048, env="DYTOPO_MAX_TOKENS")
    temperature: float = Field(default=0.7, env="DYTOPO_TEMPERATURE")
    timeout_seconds: int = Field(default=30, env="DYTOPO_TIMEOUT")
    
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    external_api_url: str = Field(default="http://localhost:8080", env="EXTERNAL_API_URL")
    external_api_key: Optional[str] = Field(default=None, env="EXTERNAL_API_KEY")
    external_api_model: str = Field(default="llama-2-7b", env="EXTERNAL_API_MODEL")
    external_api_timeout: float = Field(default=60.0, env="EXTERNAL_API_TIMEOUT")
    
    requests_per_minute: int = Field(default=60, env="DYTOPO_RPM")
    tokens_per_minute: int = Field(default=10000, env="DYTOPO_TPM")
```
