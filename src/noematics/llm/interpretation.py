from typing import Protocol, List, Any, Optional
from dataclasses import dataclass
from noematics.core import Noema, Message, RoundContext


@dataclass
class InterpretationDelta:
    query_delta: str
    key_delta: str
    field_membership: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LLMInterpretationBackend(Protocol):
    async def interpret(
        self,
        noema: Noema,
        received_messages: List[Message],
        context: RoundContext,
    ) -> InterpretationDelta:
        ...


class StubLLMBackend:
    async def interpret(
        self,
        noema: Noema,
        received_messages: List[Message],
        context: RoundContext,
    ) -> InterpretationDelta:
        msg_contents = [m.content for m in received_messages]
        return InterpretationDelta(
            query_delta=f"Updated from {len(received_messages)} messages",
            key_delta=f"Based on context: {context.goal}",
            metadata={"backend": "stub"},
        )


def create_llm_backend(backend_type: str = "stub") -> LLMInterpretationBackend:
    if backend_type == "stub":
        return StubLLMBackend()
    raise ValueError(f"Unknown backend type: {backend_type}")
