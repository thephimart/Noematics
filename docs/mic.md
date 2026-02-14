# Operational Semantics of the Minimal Implementable Core (MIC)

## Purpose

> This document specifies how the Minimal Implementable Core executes, independent of any particular semantic routing or learning strategy.
>
> It is authoritative for execution order, failure modes, and determinism guarantees of the MIC.

## Scope and Non-Goals
- What MIC includes
- What MIC explicitly excludes
- Relationship to invariants and interpretation specs

## Conceptual Role of the MIC
- Why MIC exists
- What it proves about Noematics
- How it constrains higher layers

## Core Entities
- Noema
- Field
- Message
- Agent (as perspective anchor, not decision-maker)
- Runtime

(Reference interfaces only; no redefinition)

## Execution Model Overview
- Discrete rounds
- Message passing lifecycle
- Separation of interpretation and topology

## Execution Phases (Per Round)
1. Message production
2. Routing (static in MIC)
3. Message delivery
4. Interpretation
5. State update
6. Invariant validation

## Ordering Guarantees
- Temporal ordering
- Causal traceability
- Determinism assumptions

## Invariant Enforcement Points
- When invariants are checked
- Failure behavior
- Relationship to test coverage

## Reference Implementation Notes
- Mapping to `src/noematics/core/mic.py`
- Design constraints (e.g. <200 LOC)
- Why certain shortcuts are allowed

## What MIC Enables
- Extension paths
- Replacement paths
- Research surface unlocked by MIC

## What MIC Does NOT Decide
- Learning
- Semantic similarity metrics
- Topology mutation rules
- Agent autonomy
