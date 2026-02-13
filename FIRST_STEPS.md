# Noematics — Focused First Steps

This file defines the **initial execution path** for Noematics.
If you are unsure what to work on next, start here and follow the steps in order.

This is not a roadmap.  
This is a *commit-order plan*.

---

For broader context and future work, see `dev_tasks.md`.
Do not skip steps here to work on later tasks.

---

## Phase 0 — Ground Rules (Read Once)

Before writing code:

- Do **not** add learning, optimization, or autonomy.
- Do **not** introduce LLM dependencies.
- Do **not** invent new terminology.
- Prefer explicit constraints over clever abstractions.
- If something feels philosophical, translate it into an invariant or interface.

If unsure, stop and write a doc, not code.

---

## Phase 1 — Make Meaning Constrainable (Docs Only)

**Objective**: Convert conceptual claims into enforceable constraints.

### Step 1.1 — Extract Invariants
Create `docs/invariants.md`.

Each invariant must include:
- Name
- Informal description
- Formal statement (math or logic)
- What constitutes a violation
- When it must be checked (creation, interpretation, runtime)

Target: **8–10 invariants max**.

Do not proceed until each invariant could plausibly be tested.

---

### Step 1.2 — Specify Interpretation Precisely
Create `docs/interpretation.md`.

Define interpretation as a function with:
- Explicit inputs
- Explicit outputs
- Allowed side effects (if any)
- Composition rules
- Conflict handling

Answer explicitly:
- Is interpretation pure?
- Are deltas allowed?
- Can interpretations commute?
- How are conflicts surfaced?

Include reference pseudocode.  
Avoid implementation detail.

---

### Exit Criteria (Phase 1)
You should be able to answer:

> “What would it mean for an implementation to be *incorrect*?”

If not, stop here and tighten the docs.

---

## Phase 2 — Minimal Implementable Core (MIC)

**Objective**: Define the smallest runnable Noematics system.

### Step 2.1 — Define Core Interfaces
Create `src/noematics/core/interfaces.py`.

Required protocols (no more, no less):

- `NoemaProtocol`
- `FieldProtocol`
- `MessageProtocol`
- `RoutingProtocol`
- `AgentProtocol`
- `RuntimeProtocol`

Rules:
- Interfaces only — no logic
- No inheritance trees
- No helper utilities

If an interface feels “optional”, remove it.

---

### Step 2.2 — Implement MIC Runtime
Create `src/noematics/core/mic.py`.

Constraints:
- ≤ 200 lines total
- Deterministic execution
- Static routing only
- No semantic matching
- No agents with internal state beyond perspective

Must support:
- Round-based execution
- Message passing
- Interpretation hook (even if trivial)

This file is the **reference reality check** for the entire framework.

---

### Step 2.3 — Write MIC Tests
Create `tests/mic/test_minimal_core.py`.

Tests must verify:
- Round progression
- Message delivery
- Interpretation invocation
- Invariant non-violation (even if mocked)

If a test requires mocking philosophy, the spec is wrong.

---

### Exit Criteria (Phase 2)

You can run:

```bash
pytest tests/mic
```

And observe:

- deterministic behavior
- inspectable state
- no magic

---

## Phase 3 — Only Then: DyTopo Instantiation

Only after MIC is stable:

- Add semantic routing
- Add query/key matching
- Add topology updates
- Add optional LLM-backed interpretation

If MIC breaks, revert.

---

## Anti-Goals (Enforced)

During first steps, do **NOT**:

- optimize
- generalize
- parallelize
- abstract for future use
- chase benchmarks

Correctness > clarity > power.

---

## If You’re Stuck

Ask, in order:

1. Is this required by an invariant?
2. Is this required by the MIC?
3. Can this be deferred?

If the answer is “no” three times, don’t build it.
