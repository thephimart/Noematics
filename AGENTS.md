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
pytest --cov=src/noematics --cov-report=html       # With coverage
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
- Use absolute imports: `from noematics.agents.base import Agent`
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

### Noematic Terminology
| Term | Usage |
|------|-------|
| **noema** | Semantic unit with query/key vectors — the fundamental atomic entity |
| **node** | Network/graph vertex (use only in graph/network contexts) |
| **agent** | Entity with perspective/agency — MUST have a role and execute tasks |
| **field** | Collection of noemata with shared topology — NOT "cluster" or "group" |
| **link** | Directed edge between noemata — NOT "edge", "connection", "wire" |

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

## Project Documentation

### Documentation Hierarchy

| File | Role | Properties |
|------|------|------------|
| **FIRST_STEPS.md** | Execution on-ramp — "What do I do right now, in what order?" | Linear, opinionated, prescriptive, short, cannot branch |
| **dev_tasks.md** | Maintainer control surface — "What work exists, what's blocked?" | Non-linear, can grow, can reference future phases, scope pressure management |
| **implementation_plan.md** | Normative spec — "What does it mean for implementation to be correct?" | Almost never changes casually |
| **docs/invariants.md** | Formal system invariants — structural, temporal, interpretation | 8 invariants with formal statements |
| **docs/interpretation.md** | Mechanical interpretation specification | Pseudocode, data structures, conflict resolution |

### Quick Reference

- **FIRST_STEPS.md** — Keep frozen and ruthless. This is the strict commit-order plan. Do not skip steps.
- **dev_tasks.md** — Let breathe and evolve. Broad context for future work.
- **implementation_plan.md** — The authoritative technical specification.
- **docs/invariants.md** — Required invariants all implementations must preserve.
- **docs/interpretation.md** — How interpretation works mechanically.

### Additional Resources

- **README.md** — Project overview and motivation

---

## Project Structure
```
src/noematics/
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
from noematics.agents.factory import AgentFactory
from noematics.llm.openai import OpenAIBackend

backend = OpenAIBackend(api_key=os.getenv("OPENAI_API_KEY"))
agent = AgentFactory.create_agent(role="developer", agent_id="dev_1", llm_backend=backend)
```

### Running a Task
```python
import asyncio
from noematics.core.framework import NoematicsFramework

async def main():
    framework = NoematicsFramework(config)
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
