> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Execution Layers Overview

Noematics execution is structured into layered concerns. Each layer builds strictly on the guarantees of the layer below.

### Layer Structure

1. **Minimal Implementable Core (MIC)**
   - Deterministic execution substrate
   - Core state machine and message passing
   - Defined in `docs/mic.md`

2. **Coordination Layer**
   - Round synchronization
   - Barrier-based completion detection
   - Message transport along established graph edges

3. **Semantic Routing Layer**
   - Query/key descriptor generation
   - Embedding-based similarity computation
   - Dynamic graph topology construction

4. **Agent Reasoning Layer**
   - Role-based execution
   - Context management
   - Structured output handling

5. **Orchestration & Termination Layer**
   - Global state aggregation
   - Completion detection
   - Workflow control and halting decisions

### Layer Responsibilities

| Layer | Responsibility | Cannot Access |
|-------|---------------|---------------|
| MIC | Core execution, state management | Above layers |
| Coordination | Synchronization, routing | Agent reasoning |
| Semantic Routing | Graph construction | Termination logic |
| Agent Reasoning | Task execution | None above |
| Orchestration | Goal setting, completion | Below layers (via interfaces) |

### Determinism Guarantees

- **MIC**: Full determinism under identical initial state
- **Coordination**: Deterministic message ordering
- **Semantic Routing**: Non-deterministic (depends on embedding model)
- **Agent Reasoning**: Non-deterministic (depends on LLM)
- **Orchestration**: Semi-deterministic (depends on agent outputs)

### Failure Propagation

Failures propagate upward only. A failure in a lower layer cannot be recovered by a higher layer.

- MIC failures halt execution immediately
- Coordination failures trigger retry or abort
- Semantic routing failures use fallback thresholds
- Agent reasoning failures propagate to orchestration
- Orchestration failures terminate the run

### What Cannot Cross Layer Boundaries

- MIC cannot depend on semantic routing
- Coordination cannot access LLM outputs directly
- Semantic routing cannot make termination decisions
- Agent reasoning cannot modify graph topology
- Orchestration cannot bypass agent execution
