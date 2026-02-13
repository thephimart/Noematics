# Dev Tasks

⚠️ If you are new to the project, start with `FIRST_STEPS.md`.
Tasks here assume familiarity with the core constraints.

## Task A — Hardening Pass

**Goal**: Transform philosophical principles into formal engineering constraints

### Implementation Plan

1. **Extract & Formalize Invariants**
   - Create `invariants.md` with 8 structural/temporal/interpretation invariants
   - Add formal mathematical notation for each
   - Include violation detection strategies

2. **Formalize Interpretation Mechanics**
   - Create `interpretation.md` with:
     - Pure function specification
     - Input/output types
     - Delta composition rules
     - Conflict resolution algorithm
   - Add reference pseudocode

3. **Tighten Language**
   - Audit all docs for terminology consistency
   - Enforce: noema (semantic), node (graph only), agent (with role), field, link
   - Remove metaphorical reuse

**Deliverable**: `invariants.md`, `interpretation.md`, updated `AGENTS.md`

---

## Task B — Minimal Core Spec

**Goal**: Define smallest runnable Noematics system ready for reference implementation

### Implementation Plan

1. **Define Core Interfaces** (in `src/noematics/core/interfaces.py`)
   - `NoemaProtocol` — id, query_vector, key_vector
   - `FieldProtocol` — noemata collection, links
   - `MessageProtocol` — sender, receiver, content, round
   - `RoutingProtocol` — get_targets(source_id) → List[str]
   - `NoemaAgentProtocol` — produce_message(), interpret()
   - `RuntimeProtocol` — run(goal, max_rounds)

2. **Define Execution Loop Interface**
   ```python
   class Runtime(Protocol):
       def run(self, goal: str, max_rounds: int) -> ExecutionResult: ...
   ```

3. **Create Reference Implementation**
   - `src/noematics/core/mic.py` — Under 200 LOC
   - Static routing (no semantic matching)
   - Simple message passing

4. **Write MIC Tests**
   - `tests/mic/test_minimal_core.py`
   - Verify message delivery, round execution

**Deliverable**: `src/noematics/core/interfaces.py`, `src/noematics/core/mic.py`, tests
