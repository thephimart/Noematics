from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class Noema:
    id: str
    query_vector: str
    key_vector: str


@dataclass(frozen=True)
class Field:
    id: str
    noemata: List[Noema]
    links: List[tuple[str, str]]


@dataclass(frozen=True)
class Message:
    sender_id: str
    receiver_id: Optional[str]
    content: str
    round_number: int


@dataclass(frozen=True)
class RoundContext:
    round_number: int
    goal: str
    messages: List[Message]


@dataclass(frozen=True)
class InterpretationInput:
    noema: Noema
    field_id: str
    received_messages: List[Message]
    round_context: RoundContext
    agent_id: Optional[str] = None


@dataclass(frozen=True)
class InterpretationDelta:
    noema_id: str
    state_updates: Dict[str, Any]


@dataclass(frozen=True)
class InterpretationResult:
    deltas: List[InterpretationDelta]
    messages_to_route: List[Message]


class InterpretationProtocol(Protocol):
    def interpret(self, inp: InterpretationInput) -> InterpretationResult:
        ...


class RoutingProtocol(Protocol):
    def get_targets(
        self,
        source_id: str,
        field_id: str,
        round_context: RoundContext,
    ) -> List[str]:
        ...


class AgentProtocol(Protocol):
    def perspective(self) -> Dict[str, Any]:
        ...


@dataclass
class ExecutionResult:
    rounds_completed: int
    total_messages: int
    final_states: Dict[str, Dict[str, Any]]


class RuntimeProtocol(Protocol):
    def run(self, goal: str, max_rounds: int) -> ExecutionResult:
        ...
