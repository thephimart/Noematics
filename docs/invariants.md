# Noematic Invariants

These properties **MUST** hold in all valid system states. They transform philosophical principles into engineering constraints.

---

## Structural Invariants

### 1. Field Membership

A noema MUST belong to exactly one field at any instant.

- **Formal**: `∀noema ∈ Noemata: |{f ∈ Fields : noema ∈ f}| = 1`
- **Violation**: Creates ambiguous authority and conflicting interpretations
- **Check at**: creation, field membership change

---

### 2. Graph Connectivity

Structural links MUST form a connected subgraph within a field at all stable execution points.

- **Formal**: `∀f ∈ Fields: subgraph(f.links) is connected`
- **Violation**: Isolated components cannot receive routed messages
- **Check at**: topology construction completion, after link modifications

---

### 3. Field Scope

All structural links within a field MUST stay within that field's boundary.

- **Formal**: `∀link ∈ f.links: link.source ∈ f ∧ link.target ∈ f`
- **Violation**: Cross-field links break isolation guarantees
- **Check at**: link creation

---

## Temporal Invariants

### 4. Causal Ordering

Temporal updates MUST be monotonic in causal order.

- **Formal**: `∀t1 < t2: state(t1) ⊆ state(t2) ∨ retraction(t2)` (monotonic growth, except for explicit retractions)
- **Exception**: Only explicit "retraction" operations may remove state
- **Violation**: Race conditions and inconsistent reads
- **Check at**: every state update

---

### 5. Round Atomicity

A round's interpretation MUST complete before the next round begins.

- **Formal**: `∀round r: interpret(r) happens-before interpret(r+1)`
- **Violation**: Message ordering ambiguity
- **Check at**: round transitions

---

## Interpretation Invariants

### 6. Interpretation Purity

Interpretation is a pure function — same input descriptors MUST produce same output deltas.

- **Formal**: `∀inputs: interpret(inputs) = f(inputs)` where `f` has no side effects
- **Note**: Inputs include noema state, field state, agent perspective, and round context.
- **Violation**: Non-deterministic system behavior
- **Check at**: implementation review, property-based testing

---

### 7. Topology Read-Only Interpretation

Interpretation MUST NOT mutate topology directly.

- **Formal**: `∀noema: interpret(noema).topology_delta = ∅`
- **Violation**: Breaks separation of concerns; routing logic polluted
- **Check at**: interpretation execution

---

### 8. Delta Composition

Multiple interpretations within the same field and round MUST commute.

- **Formal**: `interpret(a) ∘ interpret(b) = interpret(b) ∘ interpret(a)` (within field/round scope)
- **Violation**: Order-dependent results
- **Check at**: parallel interpretation scenarios

---

## Naming Conventions

| Term | Usage |
|------|-------|
| **noema** | Semantic unit with query/key vectors — the fundamental atomic entity |
| **node** | Network/graph vertex (use only in graph/network contexts) |
| **agent** | Entity with perspective/agency — MUST have a role and execute tasks |
| **field** | Collection of noemata with shared topology — NOT "cluster" or "group" |
| **link** | Directed edge between noemata — NOT "edge", "connection", "wire" |
