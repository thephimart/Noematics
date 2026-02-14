> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Testing Strategy

### Testing Pyramid

**Unit Tests (70%)**:
- Individual component testing
- Mock external dependencies
- Fast execution (< 1s per test)

**Integration Tests (20%)**:
- Component interaction testing
- Real LLM backends (test tokens)
- Database/file system interactions

**End-to-End Tests (10%)**:
- Complete workflow testing
- Performance benchmarking
- Paper result replication

### Test Categories

**Unit Tests**:
- `test_llm_integration.py` — LLM backend testing
- `test_semantic_matching.py` — Embedding and similarity
- `test_graph_construction.py` — Graph algorithms
- `test_message_routing.py` — Communication logic

**Integration Tests**:
- `test_agent_coordination.py` — Multi-agent workflows
- `test_noematics_framework.py` — End-to-end execution
- `test_performance.py` — Speed and scalability

**Benchmark Tests**:
- `test_paper_replication.py` — Validate against paper results
- `test_scalability.py` — Large-scale agent testing

### Performance Benchmarks

**Target Metrics**:
- Replicate paper results within 5% performance margin
- Sub-second graph construction time
- Test coverage >85%

**Metrics to Track**:
- Graph construction time: < 100ms for 10 agents
- Message routing latency: < 50ms per hop
- Total round time: < 5 seconds (excluding LLM calls)
- Memory usage: < 1GB for typical workloads
- Concurrent throughput: 50+ simultaneous frameworks

**Performance Assertions**:
- Average LLM latency < 5000ms
- P95 LLM latency < 10000ms
- Embedding throughput > 10 texts/second
- Similarity computation > 100 pairs/second

### Testing Examples

#### LLM Integration Tests

```python
# tests/unit/test_llm_integration.py
@pytest.mark.asyncio
async def test_openai_backend_success():
    backend = OpenAIBackend(api_key="test_key", model="gpt-3.5-turbo")
    
    with patch('noematics.llm.openai.AsyncOpenAI') as mock_openai:
        mock_response = AsyncMock()
        mock_response.choices = [AsyncMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_response.usage = {"prompt_tokens": 10, "completion_tokens": 5}
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        request = LLMRequest(prompt="Test prompt")
        response = await backend.generate(request)
        
        assert response.content == "Test response"
```

#### Semantic Matching Tests

```python
# tests/unit/test_semantic_matching.py
@pytest.mark.asyncio
async def test_semantic_matcher():
    encoder = SentenceTransformerEncoder()
    matcher = SemanticMatcher(encoder, threshold=0.3)
    
    queries = ["I need help with Python"]
    keys = ["I can provide Python help"]
    
    matches = await matcher.match_queries_to_keys(queries, keys)
    
    assert len(matches) > 0
    assert matches[0].similarity_score > matcher.threshold
```

#### Agent Coordination Tests

```python
# tests/integration/test_agent_coordination.py
@pytest.mark.asyncio
async def test_manager_agent_completion():
    manager = ManagerAgent(config, llm_backend)
    
    context = "Solve the problem: 2 + 2"
    result = await manager.execute(round_goal="Solve", context=context)
    
    assert result.agent_id == config.agent_id
    assert result.public_content is not None
```
