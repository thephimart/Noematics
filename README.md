# Noematics

> **Noematics is a framework for modeling how noēmata—structured units of meaning—evolve over dynamic interaction topologies.**

Noematics is a systems framework for representing, updating, and interpreting meaning as a first-class, stateful structure embedded in evolving communication graphs. It is designed for multi-agent and distributed systems where *what is meant* changes over time, across perspectives, and under structural drift.

Unlike conventional graph, agent, or routing frameworks, Noematics treats **meaning itself**—not messages, tokens, or policies—as the core object of computation.

---

## Why Noematics Exists

Most multi-agent and graph-based systems implicitly assume that meaning is:
- static,
- globally shared,
- or reducible to labels, embeddings, or messages.

In practice, meaning is:
- **stateful** (it accumulates history),
- **perspectival** (different agents interpret differently),
- and **structurally constrained** (it evolves within topologies that themselves change).

Noematics exists to make these properties *explicit, inspectable, and enforceable*.

---

## What Makes Noematics Different

Noematics is **not** just a graph model, agent framework, or semantic routing trick.

It introduces:

- **Noēmata as first-class entities**  
  Structured, stateful units of meaning—not labels or metadata.

- **Explicit separation of topology and interpretation**  
  Communication structure provides constraints; interpretation provides transformation.

- **Invariant-preserving evolution**  
  Meaning changes over time, but within formally stated system invariants.

- **Observer-relative semantics without unconstrained subjectivity**  
  Perspectives are bounded, parameterized, and comparable.

- **Dynamic topology as substrate, not controller**  
  Structural change shapes meaning without dictating it.

---

## Conceptual Core

At the heart of Noematics are four ideas:

- **Noema**  
  A structured semantic unit representing *what is meant* by an entity or relation.

- **Noematic Field**  
  A bounded collection of noēmata evolving under shared invariants.

- **Interpretation**  
  A constrained transformation mapping structure + perspective → semantic update.

- **Dynamic Topology**  
  A mutable interaction graph that conditions, but does not replace, interpretation.

Agents in Noematics are **not autonomous decision-makers**; they are **bounded sources of perspective** used to parameterize interpretation.

---

## Relationship to DyTopo

Noematics is a **general framework**.  
DyTopo-style semantic routing is provided as a **reference instantiation**.

Specifically, this repository includes an implementation of:

> **DyTopo: Dynamic Topology Routing for Multi-Agent Reasoning via Semantic Matching**  
> Lu et al., arXiv:2602.06039

In Noematics terms, DyTopo demonstrates how:
- query–key semantic matching can drive topology updates,
- interpretation can guide communication structure,
- and coordination traces can be inspected through evolving graphs.

DyTopo is *one possible realization*, not the limit of the framework.

---

## Core Properties (Non-Negotiable)

Noematics enforces system-level constraints, including:

- Noēmata belong to exactly one noematic field at any instant.
- Interpretation cannot directly mutate topology.
- Structural drift must preserve declared invariants.
- Semantic updates are temporally ordered and causally traceable.
- Perspective divergence is observable, not hidden.

These properties are specified formally in the implementation plan.

---

## Minimal Implementable Core (MIC)

The framework defines a **Minimal Implementable Core** to ensure that Noematics is runnable, testable, and useful *without*:

- learning,
- large language models,
- autonomous agents,
- or external orchestration systems.

The MIC supports:
- noema creation and mutation,
- invariant checking,
- interpretation execution,
- and topology-conditioned evolution.

Everything else is layered on top.

---

## Reference Capabilities

Built on top of the core framework, this repository includes:

- DyTopo-style semantic routing
- Dynamic topology reconstruction per round
- Multi-agent communication graphs
- Optional LLM-backed interpretation
- Interpretable coordination traces

These are **examples**, not requirements.

---

## What Noematics Is *Not*

To prevent scope creep and misinterpretation:

- ❌ Not a general intelligence system  
- ❌ Not a symbolic logic engine  
- ❌ Not an agent policy framework  
- ❌ Not an LLM orchestration toolkit  
- ❌ Not a theory of consciousness  

Noematics is about **semantic structure under change**, nothing more.

---

## Documentation

- **Implementation Plan** — Full technical specification, invariants, and MIC  
  [`implementation_plan.md`](implementation_plan.md)

- **Developer Guidelines**  
  [`AGENTS.md`](AGENTS.md)

- **License**  
  [`LICENSE`](LICENSE)

---

## Project Status

The current focus is:
- specification hardening,
- reference implementation of the MIC,
- and validation of invariant-preserving evolution.

Public APIs should be considered experimental.

---

## License

**MIT License — use it, fork it, break it, improve it.**

This repository is licensed under the MIT License.

The DyTopo paper is copyright © its authors.
This implementation is independent and not affiliated with or endorsed by them.

---

## Citation

Noematics builds on ideas introduced in the DyTopo paper.  
If you use DyTopo-style routing, please cite:

```bibtex
@article{lu2026dytopo,
  title={DyTopo: Dynamic Topology Routing for Multi-Agent Reasoning via Semantic Matching},
  author={Lu, Yuxing and Hu, Yucheng and Zhao, Xukai and Cao, Jiuxin},
  journal={arXiv preprint arXiv:2602.06039},
  year={2026}
}
