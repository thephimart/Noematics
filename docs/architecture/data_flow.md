> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Overview

This document describes the high-level flow of information through a Noematics execution.
It does not define execution order, timing guarantees, or failure semantics.

## Primary Data Artifacts

- Task context
- Round goals
- Agent descriptors (queries / keys)
- Messages
- Aggregated results

## Conceptual Flow

1. Task context initialization
2. Round goal derivation
3. Descriptor generation by agents
4. Graph construction based on descriptors
5. Message propagation along graph edges
6. Context update
7. Termination detection
