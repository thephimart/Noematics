> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Overview

This document identifies intentional extension points in the Noematics architecture.
These are locations where alternative implementations may be substituted
without violating system invariants or MIC semantics.

## Identified Extension Points

### LLM Backends
- Different providers
- Different invocation strategies
- Structured vs unstructured outputs

### Semantic Encoding
- Alternative embedding models
- Different similarity functions
- Threshold strategies

### Routing Strategies
- Alternative graph construction heuristics
- Static vs dynamic topology approaches

### Agent Roles
- New role definitions
- Specialized reasoning agents
- Tool-augmented agents

## Non-Extension Points

The following are not extension points:
- MIC execution order
- Invariant enforcement
- Failure handling semantics
