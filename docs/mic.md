# Operational Semantics of the Minimal Implementable Core (MIC)

## Purpose

> This document specifies how the Minimal Implementable Core (MIC) executes, independent of any particular semantic routing, learning strategy, or agent autonomy model.
>
> It is authoritative for execution order, determinism guarantees, invariant enforcement points, and failure behavior of the MIC.

The MIC establishes the smallest end-to-end executable substrate of Noematics. Any Noematics-compliant higher-level system MUST admit a reduction to MIC semantics.

---

## Scope and Non-Goals

The MIC intentionally includes only the minimum machinery required to execute a Noematics system while preserving semantic explicitness and invariants.

### Included

| Component | Rationale |
|---------|-----------|
| Noema data structure | Core semantic unit |
| Static field | Simplest topology |
| Static routing | Avoids semantic matching and learning |
| Round execution loop | Defines operational semantics |
| Message passing | Fundamental communication primitive |
| Invariant validation | Semantic safety guarantees |

### Explicitly Excluded

| Component | Reason |
|---------|--------|
| Agent autonomy | Higher-layer concern |
| Semantic encoding | Not required for MIC |
| Learning or adaptation | Post-MIC |
| Dynamic topology mutation | Deferred |
| Goal management | External orchestration |
| Visualization | Non-semantic |

The MIC MUST remain runnable without embeddings, LLMs, or optimization strategies.

---

## Conceptual Role of the MIC

The MIC exists to:

- Prove that Noematics is executable without semantic heuristics
- Establish a deterministic baseline for reasoning about meaning under change
- Provide a reference execution model against which extensions can be validated

The MIC constrains higher layers by fixing:
- Execution order
- Message lifecycle
- Interpretation timing
- Invariant enforcement points

Any extension that violates these constraints is **not** a Noematics-compliant system.

---

## Core Entities

The MIC operates over the following entities, as defined in the core interfaces:

- **Noema** — a stateful semantic unit
- **Field** — a collection of noemata and links
- **Message** — a directed semantic transmission
- **Agent** — a perspective anchor bound to a noema (not a decision-maker)
- **Runtime** — the execution orchestrator

This document references interfaces only and does not redefine data structures.

---

## Execution Model Overview

Execution proceeds in **discrete, synchronous rounds**.

- All message production precedes all interpretation within a round
- Routing is topology-driven, not interpretive
- Interpretation does not mutate topology in the MIC
- All invariant checks occur before advancing rounds

Interpretation and topology are strictly separated concerns.

---

## Execution Phases (Per Round)

Each round proceeds through the following phases **in strict order**:

1. **Message Production**  
   Each noema produces zero or more outbound messages based solely on its local state and the current round context.

2. **Routing**  
   Messages are routed according to a static topology. No semantic similarity or dynamic edge creation occurs.

3. **Delivery**  
   Routed messages are delivered atomically. No interpretation may begin until delivery is complete.

4. **Interpretation**  
   Each noema interprets all messages addressed to it for the current round.

5. **State Update**  
   Interpretation may update local noema state.

6. **Invariant Validation**  
   All declared invariants are checked before advancing to the next round.

Failure at any phase aborts execution.

---

## Ordering Guarantees

The MIC guarantees:

- **Temporal ordering**: rounds are totally ordered
- **Phase ordering**: phases do not interleave
- **Causal traceability**: every state update is attributable to prior messages
- **Determinism**: given identical initial state and routing, execution is repeatable

Concurrency, asynchrony, or partial delivery are explicitly out of scope.

---

## Invariant Enforcement Points

- Unless otherwise specified, invariants are checked at the end of each round
- Violations MUST halt execution
- No partial state rollback is required at MIC level
- Test coverage MUST exercise invariant failure paths

Invariant definitions are normatively specified in `docs/invariants.md`.

---

## Reference Implementation Notes

A non-authoritative reference implementation exists at:

> src/noematics/core/mic.py


Design constraints of the reference implementation:

- Minimal complexity
- Under ~200 LOC
- No semantic shortcuts beyond those permitted by this document

The reference implementation is illustrative. Conformance is determined by behavior, not code structure.

---

## What the MIC Enables

The MIC unlocks:

- Replaceable routing strategies
- Pluggable interpretation mechanisms
- Formal reasoning about semantic drift
- Controlled experimentation with topology mutation
- Deterministic test harnesses for higher layers

---

## What the MIC Does NOT Decide

The MIC explicitly does **not** decide:

- Learning rules
- Semantic similarity metrics
- Topology mutation policies
- Agent autonomy or strategy
- Optimization criteria

These belong to layers built *on top of* the MIC.

---

## Illustrative Architecture (Non-Normative)

```
┌───────────────────────────────────────────────────┐
│                     Minimal Noematics             │
├───────────────────────────────────────────────────┤
│                                                   │
│   ┌─────────┐     ┌─────────┐    ┌─────────┐      │
│   │ Noema A │ ──▶│ Noema B  │──▶│ Noema C │      │
│   └─────────┘     └─────────┘    └─────────┘      │
│        │              │              │            │
│        ▼              ▼              ▼            │
│   ┌─────────────────────────────────────────┐     │
│   │           Static Routing Table          │     │
│   │     (predefined edges, no matching)     │     │
│   └─────────────────────────────────────────┘     │
│                      │                            │
│                      ▼                            │
│   ┌─────────────────────────────────────────┐     │
│   │           Round Execution Loop           │    │
│   │  Produce → Route → Deliver → Interpret   │    │
│   │  → Update → Validate                     │    │
│   └─────────────────────────────────────────┘     │
│                                                   │
└───────────────────────────────────────────────────┘
```

> This diagram is illustrative and does not constrain implementations.
