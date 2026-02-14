> This document is descriptive and non-normative.
> It does not define required Noematics behavior.

## Agent Implementations

### Worker Agent

```python
class WorkerAgent(Agent):
    async def execute(self, round_goal: str, context: str) -> AgentMessage:
        full_prompt = self.build_context_prompt(round_goal, context)
        response = await self.generate_response(full_prompt, json_mode=True)
        
        query, key = self.extract_descriptors(response)
        
        message = AgentMessage(
            public_content=response,
            private_content={"role": self.config.role},
            query_vector=query,
            key_vector=key,
            agent_id=self.config.agent_id,
            round_number=0,
            timestamp=datetime.now()
        )
        
        self.last_response = response
        return message
```

### Manager Agent

```python
class ManagerAgent(Agent):
    async def execute(self, round_goal: str, context: str) -> AgentMessage:
        assessment_prompt = self.build_assessment_prompt(context)
        assessment = await self.generate_response(assessment_prompt, json_mode=True)
        
        try:
            assessment_data = json.loads(assessment)
            is_complete = assessment_data.get("is_complete", False)
            next_goal = assessment_data.get("next_goal", round_goal)
        except json.JSONDecodeError:
            is_complete = False
            next_goal = round_goal
        
        message = AgentMessage(
            public_content=assessment,
            private_content={"is_complete": is_complete, "next_goal": next_goal},
            query_vector="Need to assess completion status",
            key_vector="Can provide goal setting and completion assessment",
            agent_id=self.config.agent_id,
            round_number=0,
            timestamp=datetime.now()
        )
        
        self.last_response = assessment
        return message
```

### Agent Factory Implementation

```python
class AgentFactory:
    AGENT_REGISTRY: Dict[str, Type[Agent]] = {
        "developer": DeveloperAgent,
        "researcher": ResearcherAgent,
        "tester": TesterAgent,
        "designer": DesignerAgent,
        "problem_parser": ProblemParserAgent,
        "solver": SolverAgent,
        "verifier": VerifierAgent,
    }
    
    @classmethod
    def create_agent(
        cls, 
        role: str, 
        agent_id: str, 
        llm_backend: LLMBackend,
        **kwargs
    ) -> Agent:
        if role not in cls.AGENT_REGISTRY:
            raise ValueError(f"Unknown role: {role}")
        
        config = AgentConfig(agent_id=agent_id, role=role, **kwargs)
        return cls.AGENT_REGISTRY[role](config, llm_backend)
```
