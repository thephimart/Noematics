# Noematics

> "Noematics is a framework for modeling how noēmata evolve over dynamic topologies"

A Python implementation of the DyTopo framework for multi-agent reasoning with dynamic communication topologies.

## Overview

Noematics implements the DyTopo algorithm from the paper:

**DyTopo: Dynamic Topology Routing for Multi-Agent Reasoning via Semantic Matching**  
https://arxiv.org/abs/2602.06039

The framework enables multi-agent systems to dynamically rewire their communication graph at each round based on semantic matching between agents' query (need) and key (offer) descriptors.

## Features

- Dynamic topology reconstruction per round
- Semantic key-query matching for intelligent routing
- Manager-guided workflow orchestration
- Support for multiple LLM backends (OpenAI-compatible APIs)
- Interpretable coordination traces through evolving graphs

COMING SOON

## License

**MIT License — use it, fork it, break it, improve it.**

This implementation is licensed under the MIT License.

The original DyTopo paper is available on arXiv and is copyright to the authors. This implementation is an independent effort and is not affiliated with or endorsed by the paper authors.

## Citation

If you use this implementation, please cite the original paper:

```bibtex
@article{lu2026dytopo,
  title={DyTopo: Dynamic Topology Routing for Multi-Agent Reasoning via Semantic Matching},
  author={Lu, Yuxing and Hu, Yucheng and Zhao, Xukai and Cao, Jiuxin},
  journal={arXiv preprint arXiv:2602.06039},
  year={2026}
}
```
