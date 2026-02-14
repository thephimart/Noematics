# DyTopo as a Reference Instantiation

> This document describes DyTopo as a non-authoritative reference instantiation within the Noematics framework.
> It demonstrates one possible way semantic matching can drive topology evolution while preserving Noematics invariants.

## Status of This Document
- This document is **descriptive**, not prescriptive
- Deviations are allowed
- Noematics correctness does NOT depend on DyTopo
- Authority for execution lies with the MIC and invariants

---

## Why DyTopo Was Chosen

DyTopo was selected because it:
- cleanly separates semantic similarity from execution order
- exposes topology mutation as a first-class operation
- makes semantic convergence and divergence observable
- aligns naturally with Noematics’ invariant constraints

DyTopo is illustrative — not optimal, exhaustive, or required.

---

## Mapping DyTopo Concepts to Noematics

| DyTopo Concept | Noematics Concept | Notes |
|----------------|------------------|------|
| query / key vectors | noema semantic state | One possible representation |
| routing update | topology mutation | Constrained, non-interpretive |
| agent | perspective anchor | Not autonomous |

---

## Execution Flow (High-Level)

1. MIC executes a round
2. Interpretation produces semantic updates
3. DyTopo-style matching computes similarity
4. Topology is updated *between* rounds
5. Invariants are checked

DyTopo does not alter MIC execution semantics.

---

## Semantic Matching Strategy

- Vector similarity (e.g., cosine)
- Threshold-based edge creation/removal
- Stateless matching per round

This strategy is optional and replaceable.

---

## Topology Mutation Rules

DyTopo:
- mutates links only
- does not mutate noemata
- preserves field membership
- obeys invariant constraints

Violations must abort execution.

---

## Observability and Traces

DyTopo enables inspection of:
- emerging communication clusters
- semantic drift over rounds
- convergence vs fragmentation patterns

These are diagnostic signals, not guarantees.

---

## Limitations of DyTopo

- Scaling cost with dense graphs
- Fixed similarity metrics
- Limited expressiveness of vector semantics
- No built-in learning

---

## When NOT to Use DyTopo

- Symbolic reasoning systems
- Fixed-topology protocols
- Hard real-time constraints
- Non-semantic routing problems

---

## Relationship to the Original Paper

- Conceptual lineage acknowledged
- Implementation is independent
- Several simplifications applied
- No claims of equivalence or optimality
