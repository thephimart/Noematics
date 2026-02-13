from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Noema:
    id: str
    query_vector: str
    key_vector: str
    private_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Field:
    id: str
    noemata: List[Noema]
    links: List[tuple[str, str]]


@dataclass
class Message:
    sender_id: str
    receiver_id: str
    content: str
    round_number: int


@dataclass
class RoundContext:
    round_number: int
    goal: str
    messages: List[Message]


class RoutingProtocol(Protocol):
    def get_targets(self, source_id: str) -> List[str]:
        ...


class AgentProtocol(Protocol):
    def produce_message(self, context: RoundContext) -> Message:
        ...

    def interpret(self, received: List[Message], context: RoundContext) -> None:
        ...


@dataclass
class ExecutionResult:
    rounds_completed: int
    total_messages: int
    final_states: Dict[str, Dict[str, Any]]


class RuntimeProtocol(Protocol):
    def run(self, goal: str, max_rounds: int) -> ExecutionResult:
        ...
