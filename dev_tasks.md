# Dev Tasks

⚠️ If you are new to the project, start with `FIRST_STEPS.md`.
Tasks here assume familiarity with the core constraints.

## Task A — Hardening Pass

**Goal**: Transform philosophical principles into formal engineering constraints

### Implementation Plan

1. **Extract & Formalize Invariants**
   - Create `docs/invariants.md` with 8 structural/temporal/interpretation invariants
   - Add formal mathematical notation for each
   - Include violation detection strategies

2. **Formalize Interpretation Mechanics**
   - Create `docs/interpretation.md` with:
     - Pure function specification
     - Input/output types
     - Delta composition rules
     - Conflict resolution algorithm
   - Add reference pseudocode

3. **Tighten Language**
   - Audit all docs for terminology consistency
   - Enforce: noema (semantic), node (graph only), agent (with role), field, link
   - Remove metaphorical reuse

**Deliverable**: `docs/invariants.md`, `docs/interpretation.md`

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

## Tasks A & B Complete

---

## Task C — Post-MIC Direction (Decision Recorded)

**Status**: MIC implemented, tests passing, documentation hardened.

The architecture now supports the following *explicit* next steps.
No other development is considered in-scope without revisiting this decision.

### Valid Directions

1. **Freeze & Validate**
   - Write adversarial tests
   - Attempt to violate invariants
   - Stress MIC under edge conditions

2. **Extend Interpretation**
   - Add richer delta structures
   - Introduce multiple interpretation strategies
   - Preserve interpretation purity (no topology mutation)

3. **Add a Second Topology Strategy**
   - Non-DyTopo routing/topology
   - Demonstrate framework generality
   - Require zero changes to MIC

4. **Stop (Selected)**
   - MIC, DyTopo adapter, and documentation are stable
   - No further development until a new motivating question emerges
   - Revisit only with a concrete, scoped objective

**Current status**: paused by design.

> This file is intentionally frozen unless Task C is revisited with a new scoped objective.

## Sanity Checklist Verification — 2026-02-15

An external verification pass (Codex) evaluated the repository against the
9-point “one-screen sanity checklist”.

**Result**: 9/9 checks pass.

Summary:
- Normative authority is unambiguous
- MIC is the semantic anchor
- Architecture vs reference separation is clean
- Planning documents are non-normative
- Terminology is consistent and single-source
- Document tree matches mental model
- Dead ends are intentional and preserved
- No file misrepresents its authority
- Project can stop here without loss of coherence

This verification confirms the repository is in a stable, reviewable state.
