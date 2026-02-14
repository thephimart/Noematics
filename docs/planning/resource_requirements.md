> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Resource Requirements

### Scale Targets

- Support 4+ LLM backends (OpenAI, external OpenAI-compatible, Anthropic, Google, etc.)
- Handle 10+ concurrent agents

### Personnel

**Core Team (3 people)**:
- **Lead Developer**: Architecture and core components
- **ML Engineer**: LLM integration and semantic systems
- **Full-Stack Developer**: Visualization, testing, deployment

**Support Roles**:
- **DevOps Engineer**: CI/CD, infrastructure (part-time)
- **QA Engineer**: Testing strategy (part-time)

### Infrastructure

**Development Environment**:
- **Compute**: Standard development machine (no local GPU required)
- **External APIs**: Multiple endpoint configurations for model serving (llama.cpp server, LM Studio, etc.)
- **Storage**: 100GB for models and data
- **Network**: High bandwidth for API calls

**Production Environment**:
- **Container Registry**: Docker Hub/AWS ECR
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack or similar

### Budget Estimates

**Cloud Services**:
- LLM API calls: $500-1000/month
- GPU instances: $200-400/month
- Storage and networking: $100-200/month

**Software Licenses**:
- Development tools: $100-200/month
- Monitoring/observability: $50-100/month
