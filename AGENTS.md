# Noematics

> "Noematics is a framework for modeling how noēmata evolve over dynamic topologies"

Based on the DyTopo paper: https://arxiv.org/html/2602.06039v1

---

# AGENTS.md - Agent Coding Guidelines

This file provides guidelines for agents operating in this repository.

---

## Build, Lint, and Test Commands

### Development Setup
```bash
poetry install          # Install dependencies
poetry shell           # Activate virtual environment
pre-commit install     # Install pre-commit hooks
```

### Running Tests
```bash
pytest                             # Run all tests
pytest tests/unit/test_agent_system.py              # Single test file
pytest tests/unit/test_agent_system.py::TestAgentBase::test_agent_initialization  # Single test
pytest --cov=src/dytopo --cov-report=html       # With coverage
pytest -k "test_semantic"                       # Pattern matching
pytest -v                                       # Verbose mode
pytest -s                                       # Disable stdin capture
pytest tests/integration/                        # Integration tests only
```

### Linting and Formatting
```bash
black src/ tests/                              # Format code
black --check src/ tests/                      # Check without applying
mypy src/                                      # Type checking
mypy --strict src/                             # Strict mode
pre-commit run --all-files                    # Run all linters
```

---

## Code Style Guidelines

### Imports
- Use absolute imports: `from dytopo.agents.base import Agent`
- Sort: standard library → third-party → local
- Never use wildcard imports (`from x import *`)

### Formatting (Black)
- Line length: 100 characters
- Run Black before committing

### Types
- Use type hints for all signatures
- Use `Optional[X]` instead of `X | None` (Python 3.9 compatibility)
- Use `List`, `Dict`, `Tuple` from typing
- Use `@dataclass` for simple data containers

### Naming Conventions
- **Classes**: `CamelCase` (e.g., `AgentMessage`, `SemanticMatcher`)
- **Functions/methods**: `snake_case` (e.g., `build_communication_graph`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_ROUNDS`)
- **Private attributes**: `_leading_underscore` (e.g., `_internal_state`)

### Error Handling
- Use custom exceptions for domain-specific errors
- Never use bare `except:`
- Use `raise NewError("msg") from original_error` for context
- Log errors before raising

### Async Code
- Use `async`/`await` consistently
- Use `asyncio.gather()` for concurrent operations
- Use `asyncio.create_task()` for fire-and-forget
- Use `asyncio.timeout()` or `asyncio.wait_for()` for timeouts
- Never block the event loop with sync I/O

### Testing
- Use `pytest` with `pytest-asyncio` for async tests
- Name tests: `test_<method>_<expected_behavior>`
- Mock external dependencies (LLM APIs, file I/O)
- Test both success and failure paths

### Documentation
- Use Google-style docstrings
- Document all public APIs
- Include type hints in docstrings

---

## Project Structure
```
src/dytopo/
├── core/          # Framework and types
├── agents/        # Agent implementations
├── llm/           # LLM backend integrations
├── semantic/      # Semantic matching
├── graph/         # Graph construction
├── sync/          # Synchronization
├── viz/           # Visualization
└── monitoring/    # Logging and metrics
```

### Configuration
- Use Pydantic `BaseSettings` for configuration
- Support environment variables with `env` field
- Store secrets in env vars, never in code

---

## Common Patterns

### Creating an Agent
```python
from dytopo.agents.factory import AgentFactory
from dytopo.llm.openai import OpenAIBackend

backend = OpenAIBackend(api_key=os.getenv("OPENAI_API_KEY"))
agent = AgentFactory.create_agent(role="developer", agent_id="dev_1", llm_backend=backend)
```

### Running a Task
```python
import asyncio
from dytopo.core.framework import DyTopoFramework

async def main():
    framework = DyTopoFramework(config)
    result = await framework.solve(task="Your task", agent_roles=["developer", "tester"], max_rounds=5)
    print(result.final_answer)

asyncio.run(main())
```

---

## Key Dependencies
- `torch`, `transformers`, `sentence-transformers` - ML/NLP
- `openai`, `httpx` - LLM backends
- `networkx`, `scipy`, `numpy` - Graph processing
- `pydantic` - Data validation
- `pytest`, `pytest-asyncio` - Testing
- `black`, `mypy`, `flake8` - Code quality

---

## Notes for Agents
- Run `pytest` before committing
- Run `black src/` before submitting
- Check type safety with `mypy src/`
- Use logging instead of print statements
- Follow existing code patterns in the repository
